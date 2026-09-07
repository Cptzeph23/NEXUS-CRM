from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from crmApp.models import Company, Contact, Lead


class CRMViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="viewtest",
            password="testpass123",
        )

        self.client.login(
            username="viewtest",
            password="testpass123",
        )

    def test_dashboard_requires_login(self):
        self.client.logout()

        response = self.client.get(
            reverse("dashboard")
        )

        self.assertIn(
            response.status_code,
            [302, 403],
        )

    def test_company_list_loads(self):
        response = self.client.get(
            reverse("companies")
        )

        self.assertEqual(response.status_code, 200)

    def test_contact_list_loads(self):
        response = self.client.get(
            reverse("contacts")
        )

        self.assertEqual(response.status_code, 200)

    def test_lead_list_loads(self):
        response = self.client.get(
            reverse("leads")
        )

        self.assertEqual(response.status_code, 200)