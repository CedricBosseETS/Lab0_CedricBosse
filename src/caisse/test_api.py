# src/caisse/test_api.py

from django.test import TestCase
from django.conf import settings

class APIMagasinsTest(TestCase):
    def test_get_magasins(self):
        response = self.client.get(
            "/api/magasins/",
            HTTP_AUTHORIZATION=f"Token {settings.AUTH_STATIC_TOKEN}"
        )
        self.assertEqual(response.status_code, 200)

    def test_unauthorized(self):
        response = self.client.get("/api/magasins/")
        self.assertEqual(response.status_code, 401)
