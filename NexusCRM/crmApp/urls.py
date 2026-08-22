
from django.contrib import admin
from django.urls import path
from crmApp import views

urlpatterns = [

    
    path("", views.dashboard, name="dashboard"),

    # Authentication URLs
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    #Dashboard and Home URLs
    path("home/", views.home, name="home"),
    
    # Leads
    path("leads/", views.lead_list, name="leads"),
    path("leads/create/", views.lead_create, name="lead_create"),
    path("leads/<int:pk>/", views.lead_detail, name="lead_detail"),
    path("leads/<int:pk>/edit/", views.lead_update, name="lead_update"),
    path("leads/<int:pk>/convert/", views.lead_convert,name="lead_convert"),
    path("leads/<int:pk>/delete/", views.lead_delete, name="lead_delete"),

    # Contacts

    path("contacts/", views.contact_list, name="contact_list"),

    path("contacts/create/", views.contact_create, name="contact_create"),

    path("contacts/<int:pk>/",views.contact_detail, name="contact_detail"),

    path("contacts/<int:pk>/edit/", views.contact_edit,name="contact_edit"),

    path("contacts/<int:pk>/delete/", views.contact_delete,name="contact_delete"),

   # Companies
    path(
        "companies/", views.company_list, name="company_list"),

    path("companies/create/", views.company_create, name="company_create"
    ),

    path("companies/<int:pk>/", views.company_detail, name="company_detail"),

    path("companies/<int:pk>/edit/", views.company_edit,name="company_edit"),

    path("companies/<int:pk>/delete/", views.company_delete,name="company_delete"),

    # Deals
    path("deals/", views.deal_list, name="deals"),
    path("deals/create/", views.deal_create, name="deal_create"),

    path("activities/", lambda request: views.module_placeholder(request, "Activities"), name="activities"),

    path("tasks/", lambda request: views.module_placeholder( request,"Tasks"), name="tasks"),

    path("reports/", lambda request: views.module_placeholder(request,"Reports"), name="reports"),

    path("calendar/", lambda request: views.module_placeholder(request, "Calendar"), name="calendar"),

    path("settings/", lambda request: views.module_placeholder(request, "Settings"), name="settings"),

    

]
