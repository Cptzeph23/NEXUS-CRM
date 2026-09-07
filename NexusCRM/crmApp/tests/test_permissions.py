from django.contrib.auth.models import User
from django.test import TestCase

from crmApp.models import Note
from crmApp.permissions import (
    can_manage_notes,
    can_view_note,
    can_edit_note,
    can_delete_note,
)


class NotePermissionTest(TestCase):

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin_test",
            password="testpass123",
        )

        self.sales = User.objects.create_user(
            username="sales_test",
            password="testpass123",
        )

        self.viewer = User.objects.create_user(
            username="viewer_test",
            password="testpass123",
        )

        self.admin.profile.role = "admin"
        self.admin.profile.save()

        self.sales.profile.role = "sales"
        self.sales.profile.save()

        self.viewer.profile.role = "viewer"
        self.viewer.profile.save()

        self.note = Note.objects.create(
            title="Sales Note",
            content="Test content",
            created_by=self.sales,
        )

    def test_admin_can_manage_notes(self):
        self.assertTrue(
            can_manage_notes(self.admin)
        )

    def test_sales_can_manage_notes(self):
        self.assertTrue(
            can_manage_notes(self.sales)
        )

    def test_viewer_cannot_manage_notes(self):
        self.assertFalse(
            can_manage_notes(self.viewer)
        )

    def test_all_roles_can_view_note(self):
        self.assertTrue(
            can_view_note(self.viewer, self.note)
        )

    def test_sales_can_edit_own_note(self):
        self.assertTrue(
            can_edit_note(self.sales, self.note)
        )

    def test_viewer_cannot_edit_note(self):
        self.assertFalse(
            can_edit_note(self.viewer, self.note)
        )

    def test_viewer_cannot_delete_note(self):
        self.assertFalse(
            can_delete_note(self.viewer, self.note)
        )