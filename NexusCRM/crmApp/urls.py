
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
    

    path("leads/", lambda request: views.module_placeholder(request,"Leads"), name="leads"),

    path("contacts/", lambda request: views.module_placeholder(request, "Contacts"), name="contacts"),

   # Companies
    path(
        "companies/", views.company_list, name="company_list"),

    path("companies/create/", views.company_create, name="company_create"
    ),

    path("companies/<int:pk>/", views.company_detail, name="company_detail"),

    path("companies/<int:pk>/edit/", views.company_edit,name="company_edit"),

    path("companies/<int:pk>/delete/", views.company_delete,name="company_delete"),


    path("deals/", lambda request: views.module_placeholder(request,"Deals"), name="deals"),

    path("activities/", lambda request: views.module_placeholder(request, "Activities"), name="activities"),

    path("tasks/", lambda request: views.module_placeholder( request,"Tasks"), name="tasks"),

    path("reports/", lambda request: views.module_placeholder(request,"Reports"), name="reports"),

    path("calendar/", lambda request: views.module_placeholder(request, "Calendar"), name="calendar"),

    path("settings/", lambda request: views.module_placeholder(request, "Settings"), name="settings"),

]
