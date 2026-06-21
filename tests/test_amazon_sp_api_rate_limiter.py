from unittest import TestCase
from unittest.mock import patch

from app.services import amazon_sp_api_client


class AmazonSpApiRateLimiterTest(TestCase):
    @patch.object(amazon_sp_api_client, "missing_connector_settings", return_value=[])
    def test_default_clients_share_reports_api_rate_limiter(self, _missing_settings):
        first = amazon_sp_api_client.AmazonSpApiClient()
        second = amazon_sp_api_client.AmazonSpApiClient()

        self.assertIs(
            first.rate_limiter,
            amazon_sp_api_client.SHARED_REPORTS_API_RATE_LIMITER,
        )
        self.assertIs(second.rate_limiter, first.rate_limiter)

    @patch.object(amazon_sp_api_client, "missing_connector_settings", return_value=[])
    def test_explicit_rate_limiter_is_preserved(self, _missing_settings):
        limiter = amazon_sp_api_client.AmazonSpApiRateLimiter(
            {"createReport": 90.0}
        )

        client = amazon_sp_api_client.AmazonSpApiClient(rate_limiter=limiter)

        self.assertIs(client.rate_limiter, limiter)
        self.assertEqual(client.rate_limiter.min_intervals["createReport"], 90.0)
