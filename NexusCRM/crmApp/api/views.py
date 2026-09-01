from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter


from crmApp.models import (
    Company,
    Contact,
    Lead,
    Deal,
    Activity,
    Task,
    Note,
)

from .serializers import (
    CompanySerializer,
    ContactSerializer,
    LeadSerializer,
    DealSerializer,
    ActivitySerializer,
    TaskSerializer,
    NoteSerializer,
)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "industry",
        "owner",
    ]

    search_fields = [
        "name",
        "email",
        "phone",
        "city",
        "country",
    ]

    ordering_fields = [
        "name",
        "created_at",
        "updated_at",
    ]

    ordering = ["name"]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_fields = [
        "company",
        "owner",
        "status",
    ]

    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "mobile",
        "job_title",
        "city",
        "country",
    ]

    ordering_fields = [
        "first_name",
        "last_name",
        "created_at",
        "updated_at",
    ]

    ordering = ["first_name", "last_name"]


class LeadViewSet(viewsets.ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer