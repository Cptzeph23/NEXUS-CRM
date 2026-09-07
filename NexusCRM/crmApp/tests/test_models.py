from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from crmApp.models import (
    Company,
    Contact,
    Lead,
    Pipeline,
    PipelineStage,
    Deal,
    Activity,
    Task,
    Note,
    Tag,
)


class CompanyModelTest(TestCase):

    def test_company_creation(self):
        company = Company.objects.create(
            name="Test Company",
            industry="technology",
        )

        self.assertEqual(str(company), "Test Company")


class ContactModelTest(TestCase):

    def test_contact_creation(self):
        contact = Contact.objects.create(
            first_name="John",
            last_name="Doe",
        )

        self.assertEqual(str(contact), "John Doe")


class LeadModelTest(TestCase):

    def test_lead_creation(self):
        lead = Lead.objects.create(
            first_name="Jane",
            last_name="Doe",
            estimated_value=Decimal("5000.00"),
        )

        self.assertEqual(str(lead), "Jane Doe")


class DealModelTest(TestCase):

    def setUp(self):
        self.pipeline = Pipeline.objects.create(
            name="Sales Pipeline"
        )

        self.stage = PipelineStage.objects.create(
            pipeline=self.pipeline,
            name="New",
            order=1,
        )

    def test_deal_creation(self):
        deal = Deal.objects.create(
            name="Test Deal",
            pipeline=self.pipeline,
            stage=self.stage,
            amount=Decimal("10000.00"),
        )

        self.assertEqual(str(deal), "Test Deal")


class ActivityModelTest(TestCase):

    def test_activity_creation(self):
        user = User.objects.create_user(
            username="activityuser",
            password="testpass123",
        )

        activity = Activity.objects.create(
            subject="Test Call",
            activity_type=Activity.TYPE_CALL,
            activity_date="2026-01-01T10:00:00Z",
            created_by=user,
        )

        self.assertEqual(str(activity), "Test Call")


class TaskModelTest(TestCase):

    def test_task_creation(self):
        user = User.objects.create_user(
            username="taskuser",
            password="testpass123",
        )

        task = Task.objects.create(
            title="Test Task",
            created_by=user,
        )

        self.assertEqual(str(task), "Test Task")


class NoteModelTest(TestCase):

    def test_note_creation(self):
        user = User.objects.create_user(
            username="noteuser",
            password="testpass123",
        )

        note = Note.objects.create(
            title="Test Note",
            content="Test note content",
            created_by=user,
        )

        self.assertEqual(str(note), "Test Note")


class TagModelTest(TestCase):

    def test_tag_creation(self):
        tag = Tag.objects.create(
            name="Important"
        )

        self.assertEqual(str(tag), "Important")