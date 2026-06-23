import unittest
from types import SimpleNamespace

from app.auth.middleware import build_dev_user, is_public_path, required_permission_for
from app.auth.permissions import has_permission, normalize_roles, permissions_for_roles
from app.auth.routes import user_from_claims
from app.config.settings import settings


class AuthTest(unittest.TestCase):
    def request(self, path: str, method: str = "GET"):
        return SimpleNamespace(url=SimpleNamespace(path=path), method=method)

    def test_role_groups_are_normalized_from_oidc_claims(self):
        user = user_from_claims(
            {
                "email": "operator@example.com",
                "name": "Operator",
                "groups": [
                    "/mirenelle/ops_operator",
                    "external:unknown",
                    "ops_finance",
                ],
            }
        )

        self.assertEqual(user["email"], "operator@example.com")
        self.assertEqual(user["roles"], ["ops_operator", "ops_finance"])
        self.assertIn("ops:operate", user["permissions"])
        self.assertIn("ops:finance", user["permissions"])
        self.assertNotIn("ops:configure", user["permissions"])

    def test_owner_permission_covers_all_app_permissions(self):
        permissions = permissions_for_roles(["owner"])

        self.assertTrue(has_permission(permissions, "ops:view"))
        self.assertTrue(has_permission(permissions, "ops:operate"))
        self.assertTrue(has_permission(permissions, "ops:finance"))
        self.assertTrue(has_permission(permissions, "ops:configure"))
        self.assertTrue(has_permission(permissions, "ops:any-future-permission"))

    def test_required_permission_by_route_area(self):
        self.assertIsNone(required_permission_for(self.request("/reports/summary", "HEAD")))
        self.assertEqual(required_permission_for(self.request("/reports/product-profitability")), "ops:finance")
        self.assertEqual(required_permission_for(self.request("/settings/fulfillment-costs")), "ops:view")
        self.assertEqual(required_permission_for(self.request("/settings/fulfillment-costs", "POST")), "ops:configure")
        self.assertEqual(required_permission_for(self.request("/inventory/items", "POST")), "ops:operate")
        self.assertEqual(required_permission_for(self.request("/inventory/items")), "ops:view")

    def test_public_paths_stay_public(self):
        self.assertTrue(is_public_path("/"))
        self.assertTrue(is_public_path("/auth/login"))
        self.assertTrue(is_public_path("/health"))
        self.assertFalse(is_public_path("/ui/"))

    def test_dev_user_falls_back_to_owner_when_roles_are_invalid(self):
        original_roles = settings.AUTH_DEV_ROLES
        original_user = settings.AUTH_DEV_USER
        try:
            settings.AUTH_DEV_USER = "dev-test@example.com"
            settings.AUTH_DEV_ROLES = "unknown-role"

            user = build_dev_user()

            self.assertEqual(user["email"], "dev-test@example.com")
            self.assertEqual(user["roles"], ["owner"])
            self.assertIn("ops:admin", user["permissions"])
        finally:
            settings.AUTH_DEV_ROLES = original_roles
            settings.AUTH_DEV_USER = original_user

    def test_normalize_roles_strips_provider_prefixes(self):
        self.assertEqual(
            normalize_roles(["/groups/ops_manager", "realm:ops_viewer", "ignored"]),
            ["ops_manager", "ops_viewer"],
        )


if __name__ == "__main__":
    unittest.main()
