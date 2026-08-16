
from django.contrib import admin
from django.urls import path
from crmApp import views

urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "",
        views.home,
        name="dashboard"
    ),

    path(
        "leads/",
        lambda request: views.module_placeholder(
            request,
            "Leads"
        ),
        name="leads"
    ),

    path(
        "contacts/",
        lambda request: views.module_placeholder(
            request,
            "Contacts"
        ),
        name="contacts"
    ),

    path(
        "companies/",
        lambda request: views.module_placeholder(
            request,
            "Companies"
        ),
        name="companies"
    ),

    path(
        "deals/",
        lambda request: views.module_placeholder(
            request,
            "Deals"
        ),
        name="deals"
    ),

    path(
        "activities/",
        lambda request: views.module_placeholder(
            request,
            "Activities"
        ),
        name="activities"
    ),

    path(
        "tasks/",
        lambda request: views.module_placeholder(
            request,
            "Tasks"
        ),
        name="tasks"
    ),

    path(
        "reports/",
        lambda request: views.module_placeholder(
            request,
            "Reports"
        ),
        name="reports"
    ),

    path(
        "calendar/",
        lambda request: views.module_placeholder(
            request,
            "Calendar"
        ),
        name="calendar"
    ),

    path(
        "settings/",
        lambda request: views.module_placeholder(
            request,
            "Settings"
        ),
        name="settings"
    ),

]
