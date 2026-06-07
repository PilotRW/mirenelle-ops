import gzip
from dataclasses import dataclass
from datetime import date, datetime, time, timezone
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
    "UK": "A1F83G8C2ARO7P",
}

EU_MARKETPLACES: tuple[str, ...] = ("DE", "FR", "IT", "ES", "NL", "BE", "PL", "SE")

DONE_REPORT_STATUSES = {"DONE"}
FAILED_REPORT_STATUSES = {"CANCELLED", "FATAL"}


class AmazonSpApiConfigError(RuntimeError):
    pass


class AmazonSpApiError(RuntimeError):
    pass


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


def utc_day_start(value: date) -> str:
    return datetime.combine(value, time.min, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


def utc_next_day_start(value: date) -> str:
    return datetime.combine(value, time.max, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")


class AmazonSpApiClient:
    def __init__(self) -> None:
        missing = missing_connector_settings()
        if missing:
            raise AmazonSpApiConfigError(f"Amazon SP-API connector is missing settings: {', '.join(missing)}")
        self.endpoint = settings.AMAZON_SP_API_ENDPOINT.rstrip("/")
        self.region = settings.AMAZON_SP_API_REGION
        self._access_token: str | None = None

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
        marketplace_id = marketplace_id_for(marketplace)
        response = await client.post(
            f"{self.endpoint}/reports/2021-06-30/reports",
            headers=await self._sp_api_headers(client),
            json={
                "reportType": REPORT_TYPE_ALL_ORDERS_BY_ORDER_DATE,
                "marketplaceIds": [marketplace_id],
                "dataStartTime": utc_day_start(start_date),
                "dataEndTime": utc_next_day_start(end_date),
            },
        )
        self._raise_for_status(response, "createReport")
        report_id = response.json().get("reportId")
        if not report_id:
            raise AmazonSpApiError("createReport response did not include reportId.")
        return str(report_id)

    async def get_report(self, client: httpx.AsyncClient, report_id: str) -> dict[str, Any]:
        response = await client.get(
            f"{self.endpoint}/reports/2021-06-30/reports/{report_id}",
            headers=await self._sp_api_headers(client),
        )
        self._raise_for_status(response, "getReport")
        return response.json()

    async def get_report_document(self, client: httpx.AsyncClient, report_document_id: str) -> dict[str, Any]:
        response = await client.get(
            f"{self.endpoint}/reports/2021-06-30/documents/{report_document_id}",
            headers=await self._sp_api_headers(client),
        )
        self._raise_for_status(response, "getReportDocument")
        return response.json()

    async def download_document(self, client: httpx.AsyncClient, document: dict[str, Any]) -> bytes:
        url = document.get("url")
        if not url:
            raise AmazonSpApiError("getReportDocument response did not include a download URL.")
        response = await client.get(str(url))
        self._raise_for_status(response, "download report document")
        content = response.content
        compression_algorithm = str(document.get("compressionAlgorithm") or "").upper()
        if compression_algorithm == "GZIP":
            return gzip.decompress(content)
        if compression_algorithm:
            raise AmazonSpApiError(f"Unsupported report compression algorithm: {compression_algorithm}.")
        return content

    @staticmethod
    def _raise_for_status(response: httpx.Response, operation: str) -> None:
        if response.is_success:
            return
        try:
            detail = response.json()
        except ValueError:
            detail = response.text
        raise AmazonSpApiError(f"{operation} failed with HTTP {response.status_code}: {detail}")
