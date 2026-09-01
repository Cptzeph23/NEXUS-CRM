from rest_framework.routers import DefaultRouter

from .views import (
    CompanyViewSet,
    ContactViewSet,
    LeadViewSet,
    DealViewSet,
    ActivityViewSet,
    TaskViewSet,
    NoteViewSet,
)


router = DefaultRouter()

router.register(
    r"companies",
    CompanyViewSet,
    basename="api-companies",
)

router.register(
    r"contacts",
    ContactViewSet,
    basename="api-contacts",
)

router.register(
    r"leads",
    LeadViewSet,
    basename="api-leads",
)

router.register(
    r"deals",
    DealViewSet,
    basename="api-deals",
)

router.register(
    r"activities",
    ActivityViewSet,
    basename="api-activities",
)

router.register(
    r"tasks",
    TaskViewSet,
    basename="api-tasks",
)

router.register(
    r"notes",
    NoteViewSet,
    basename="api-notes",
)


urlpatterns = router.urls