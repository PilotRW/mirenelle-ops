import asyncio
import gzip
import random
import time
from dataclasses import dataclass
from datetime import date, datetime, time as datetime_time, timezone
from typing import Any

import httpx

from app.config.settings import settings
from app.ingestion.amazon_reports.order_reports import REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE


MARKETPLACE_IDS: dict[str, str] = {
    "DE": "A1PA6795UKMFR9",
    "FR": "A13V1IB3VIYZZH",
    "IT": "APJ6JRA9NG5V4",
    "ES": "A1RKKUPIHCS9HS",
    "NL": "A1805IZSGTT6HS",
    "BE": "AMEN7PMS3EDWL",
    "PL": "A1C3SOZRARQ6R3",
    "SE": "A2NODRKZP88ZB9",
    "IE": "A28R8C7NBKEWEA",
    "UK": "A1F83G8C2ARO7P",
}

EU_MARKETPLACES: tuple[str, ...] = ("DE", "FR", "IT", "ES", "NL", "BE", "PL", "SE", "IE")

DONE_REPORT_STATUSES = {"DONE"}
FAILED_REPORT_STATUSES = {"CANCELLED", "FATAL"}
DEFAULT_REPORTS_API_MIN_INTERVALS: dict[str, float] = {
    "createReport": 65.0,
    "getReport": 1.0,
    "getReports": 1.0,
    "getReportDocument": 1.0,
    "downloadReportDocument": 0.5,
}
RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


class AmazonSpApiConfigError(RuntimeError):
    pass


class AmazonSpApiError(RuntimeError):
    pass


class AmazonSpApiRateLimiter:
    def __init__(self, min_intervals: dict[str, float] | None = None) -> None:
        self.min_intervals = dict(DEFAULT_REPORTS_API_MIN_INTERVALS)
        if min_intervals:
            self.min_intervals.update(min_intervals)
        self._next_allowed_at: dict[str, float] = {}
        self._lock = asyncio.Lock()

    async def wait(self, operation: str) -> None:
        async with self._lock:
            now = time.monotonic()
            next_allowed_at = self._next_allowed_at.get(operation, now)
            if next_allowed_at > now:
                await asyncio.sleep(next_allowed_at - now)
                now = time.monotonic()
            self._next_allowed_at[operation] = now + self.min_intervals.get(operation, 1.0)

    def note_response(self, operation: str, response: httpx.Response) -> None:
        rate_limit = response.headers.get("x-amzn-RateLimit-Limit")
        if not rate_limit:
            return
        try:
            requests_per_second = float(rate_limit)
        except ValueError:
            return
        if requests_per_second <= 0:
            return
        self.min_intervals[operation] = max(
            self.min_intervals.get(operation, 0),
            1 / requests_per_second,
        )

    def backoff(self, operation: str, seconds: float) -> None:
        self._next_allowed_at[operation] = max(
            self._next_allowed_at.get(operation, 0),
            time.monotonic() + seconds,
        )


# All report sync services in this application process must share the same
# limiter. Otherwise simultaneous Orders, Returns, Inventory, Storage, and
# Reimbursements syncs can each satisfy their own limiter while collectively
# exceeding Amazon's operation quota.
SHARED_REPORTS_API_RATE_LIMITER = AmazonSpApiRateLimiter()


@dataclass(frozen=True)
class DownloadedReport:
    report_id: str
    report_document_id: str
    filename: str
    content: bytes
    processing_status: str


def connector_required_settings() -> dict[str, str | None]:
    return {
        "AMAZON_SP_API_REFRESH_TOKEN": settings.AMAZON_SP_API_REFRESH_TOKEN,
        "AMAZON_SP_API_LWA_CLIENT_ID": settings.AMAZON_SP_API_LWA_CLIENT_ID,
        "AMAZON_SP_API_LWA_CLIENT_SECRET": settings.AMAZON_SP_API_LWA_CLIENT_SECRET,
    }


def missing_connector_settings() -> list[str]:
    return [key for key, value in connector_required_settings().items() if not value]


def marketplace_id_for(code: str) -> str:
    marketplace_id = MARKETPLACE_IDS.get(code.upper())
    if not marketplace_id:
        supported = ", ".join(sorted(MARKETPLACE_IDS))
        raise AmazonSpApiConfigError(f"Unsupported marketplace {code}. Supported marketplaces: {supported}.")
    return marketplace_id


def marketplace_ids_for(code: str) -> list[str]:
    normalized = code.upper()
    if normalized == "EU":
        return [marketplace_id_for(marketplace) for marketplace in EU_MARKETPLACES]
    return [marketplace_id_for(normalized)]


def utc_day_start(value: date) -> str:
    return datetime.combine(value, datetime_time.min, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def utc_next_day_start(value: date) -> str:
    return datetime.combine(value, datetime_time.max, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


class AmazonSpApiClient:
    def __init__(self, rate_limiter: AmazonSpApiRateLimiter | None = None) -> None:
        missing = missing_connector_settings()
        if missing:
            raise AmazonSpApiConfigError(f"Amazon SP-API connector is missing settings: {', '.join(missing)}")
        self.endpoint = settings.AMAZON_SP_API_ENDPOINT.rstrip("/")
        self.region = settings.AMAZON_SP_API_REGION
        self._access_token: str | None = None
        self.rate_limiter = rate_limiter or SHARED_REPORTS_API_RATE_LIMITER

    async def _lwa_access_token(self, client: httpx.AsyncClient) -> str:
        if self._access_token:
            return self._access_token

        response = await client.post(
            "https://api.amazon.com/auth/o2/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": settings.AMAZON_SP_API_REFRESH_TOKEN,
                "client_id": settings.AMAZON_SP_API_LWA_CLIENT_ID,
                "client_secret": settings.AMAZON_SP_API_LWA_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        self._raise_for_status(response, "LWA token")
        payload = response.json()
        access_token = payload.get("access_token")
        if not access_token:
            raise AmazonSpApiError("Amazon LWA token response did not include access_token.")
        self._access_token = str(access_token)
        return self._access_token

    async def _sp_api_headers(self, client: httpx.AsyncClient) -> dict[str, str]:
        access_token = await self._lwa_access_token(client)
        return {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "x-amz-access-token": access_token,
        }

    async def create_orders_report(
        self,
        client: httpx.AsyncClient,
        marketplace: str,
        start_date: date,
        end_date: date,
    ) -> str:
        return await self.create_report(
            client=client,
            marketplace=marketplace,
            report_type=REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE,
            start_date=start_date,
            end_date=end_date,
        )

    async def create_report(
        self,
        client: httpx.AsyncClient,
        marketplace: str,
        report_type: str,
        start_date: date,
        end_date: date,
    ) -> str:
        marketplace_ids = marketplace_ids_for(marketplace)
        response = await self._request_with_retries(
            client=client,
            operation="createReport",
            method="POST",
            url=f"{self.endpoint}/reports/2021-06-30/reports",
            headers=await self._sp_api_headers(client),
            json={
                "reportType": report_type,
                "marketplaceIds": marketplace_ids,
                "dataStartTime": utc_day_start(start_date),
                "dataEndTime": utc_next_day_start(end_date),
            },
        )
        report_id = response.json().get("reportId")
        if not report_id:
            raise AmazonSpApiError("createReport response did not include reportId.")
        return str(report_id)

    async def get_report(self, client: httpx.AsyncClient, report_id: str) -> dict[str, Any]:
        response = await self._request_with_retries(
            client=client,
            operation="getReport",
            method="GET",
            url=f"{self.endpoint}/reports/2021-06-30/reports/{report_id}",
            headers=await self._sp_api_headers(client),
        )
        return response.json()

    async def get_reports(
        self,
        client: httpx.AsyncClient,
        report_type: str,
        marketplace: str,
    ) -> list[dict[str, Any]]:
        params: list[tuple[str, str]] = [
            ("reportTypes", report_type),
            ("processingStatuses", "DONE"),
            ("pageSize", "10"),
        ]
        params.extend(
            ("marketplaceIds", marketplace_id)
            for marketplace_id in marketplace_ids_for(marketplace)
        )
        response = await self._request_with_retries(
            client=client,
            operation="getReports",
            method="GET",
            url=f"{self.endpoint}/reports/2021-06-30/reports",
            headers=await self._sp_api_headers(client),
            params=params,
        )
        return list(response.json().get("reports") or [])

    async def get_report_document(self, client: httpx.AsyncClient, report_document_id: str) -> dict[str, Any]:
        response = await self._request_with_retries(
            client=client,
            operation="getReportDocument",
            method="GET",
            url=f"{self.endpoint}/reports/2021-06-30/documents/{report_document_id}",
            headers=await self._sp_api_headers(client),
        )
        return response.json()

    async def download_document(self, client: httpx.AsyncClient, document: dict[str, Any]) -> bytes:
        url = document.get("url")
        if not url:
            raise AmazonSpApiError("getReportDocument response did not include a download URL.")
        response = await self._request_with_retries(
            client=client,
            operation="downloadReportDocument",
            method="GET",
            url=str(url),
            use_sp_api_throttle=False,
        )
        content = response.content
        compression_algorithm = str(document.get("compressionAlgorithm") or "").upper()
        if compression_algorithm == "GZIP":
            return gzip.decompress(content)
        if compression_algorithm:
            raise AmazonSpApiError(f"Unsupported report compression algorithm: {compression_algorithm}.")
        return content

    async def _request_with_retries(
        self,
        client: httpx.AsyncClient,
        operation: str,
        method: str,
        url: str,
        max_attempts: int = 5,
        use_sp_api_throttle: bool = True,
        **kwargs,
    ) -> httpx.Response:
        for attempt in range(1, max_attempts + 1):
            if use_sp_api_throttle:
                await self.rate_limiter.wait(operation)
            response = await client.request(method, url, **kwargs)
            if use_sp_api_throttle:
                self.rate_limiter.note_response(operation, response)
            if response.status_code not in RETRYABLE_STATUS_CODES or attempt == max_attempts:
                self._raise_for_status(response, operation)
                return response
            delay = self._retry_delay(response=response, attempt=attempt)
            if use_sp_api_throttle:
                self.rate_limiter.backoff(operation, delay)
            await asyncio.sleep(delay)
        raise AmazonSpApiError(f"{operation} failed after {max_attempts} attempts.")

    @staticmethod
    def _retry_delay(response: httpx.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                return min(300.0, max(1.0, float(retry_after)))
            except ValueError:
                pass
        return min(300.0, (2 ** attempt) + random.uniform(0, 1.5))

    @staticmethod
    def _raise_for_status(response: httpx.Response, operation: str) -> None:
        if response.is_success:
            return
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise AmazonSpApiError(f"{operation} failed with HTTP {response.status_code}: {detail}")
