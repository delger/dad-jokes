from unittest.mock import patch

from django.test import SimpleTestCase

from dad_jokes_project import settings


class SettingsTests(SimpleTestCase):
    def test_env_bool_parses_true_values(self):
        with patch.dict("os.environ", {"TEST_BOOL": "true"}):
            self.assertTrue(settings.env_bool("TEST_BOOL"))

    def test_env_bool_parses_false_values(self):
        with patch.dict("os.environ", {"TEST_BOOL": "false"}):
            self.assertFalse(settings.env_bool("TEST_BOOL", default=True))

    def test_env_bool_returns_default_for_missing_value(self):
        self.assertTrue(settings.env_bool("MISSING_TEST_BOOL", default=True))
        self.assertFalse(settings.env_bool("MISSING_TEST_BOOL", default=False))

    def test_whitenoise_middleware_is_enabled_after_security_middleware(self):
        self.assertEqual(
            settings.MIDDLEWARE[:2],
            [
                "django.middleware.security.SecurityMiddleware",
                "whitenoise.middleware.WhiteNoiseMiddleware",
            ],
        )

    def test_static_root_is_configured(self):
        self.assertEqual(settings.STATIC_URL, "static/")
        self.assertEqual(settings.STATIC_ROOT.name, "staticfiles")
