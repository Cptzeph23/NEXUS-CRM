from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from crmApp.models import Company, Lead


class CRMAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="apitest",
            password="testpass123",
        )

        self.token = Token.objects.create(
            user=self.user
        )

        self.company = Company.objects.create(
            name="API Test Company",
            industry="technology",
        )

        self.lead = Lead.objects.create(
            first_name="API",
            last_name="Lead",
            estimated_value=Decimal("2500.00"),
        )

    def authenticate(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

    def test_api_requires_authentication(self):
        response = self.client.get(
            "/api/v1/leads/"
        )

        self.assertEqual(
            response.status_code,
            401,
        )

    def test_authenticated_lead_list(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/leads/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_api_search(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/leads/?search=API"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_api_ordering(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/leads/?ordering=-estimated_value"
        )

        self.assertEqual(
            response.status_code,
            200,
        )

    def test_api_company_list(self):
        self.authenticate()

        response = self.client.get(
            "/api/v1/companies/"
        )

        self.assertEqual(
            response.status_code,
            200,
        )