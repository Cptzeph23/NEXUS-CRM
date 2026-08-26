
from django.contrib import admin
from django.urls import path
from crmApp import views

urlpatterns = [

    #Dashboard and Home URLs
    path("", views.dashboard, name="dashboard"),
    path("home/", views.home, name="home"),

    # Authentication URLs
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    
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
    path("companies/", views.company_list, name="company_list"),
    path("companies/create/", views.company_create, name="company_create"),
    path("companies/<int:pk>/", views.company_detail, name="company_detail"),
    path("companies/<int:pk>/edit/", views.company_edit,name="company_edit"),
    path("companies/<int:pk>/delete/", views.company_delete,name="company_delete"),

    # Deals
    
    path("deals/", views.deal_list, name="deals"),
    path("deals/create/", views.deal_create, name="deal_create"),
    path("deals/<int:pk>/", views.deal_detail, name="deal_detail"),
    path("deals/<int:pk>/edit/", views.deal_edit, name="deal_edit"),
    path("deals/<int:pk>/delete/", views.deal_delete, name="deal_delete"),

    # Activities
    path("activities/", views.activity_list, name="activities"),
    path("activities/create/", views.activity_create, name="activity_create"),
    path("activities/<int:pk>/", views.activity_detail,name="activity_detail"),
    path("activities/<int:pk>/edit/", views.activity_edit,name="activity_edit"),
    path("activities/<int:pk>/delete/",views.activity_delete,name="activity_delete"),

    
    # Tasks
    path("tasks/", views.task_list, name="tasks"),
    path("tasks/create/", views.task_create, name="task_create"),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/<int:pk>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),

    # Notes
    path("notes/", views.note_list, name="notes"),
    path("notes/create/", views.note_create, name="note_create"),
    path("notes/<int:pk>/", views.note_detail, name="note_detail"),
    path("notes/<int:pk>/edit/", views.note_edit, name="note_edit"),
    path("notes/<int:pk>/delete/", views.note_delete, name="note_delete"),


    path("reports/", lambda request: views.module_placeholder(request,"Reports"), name="reports"),

    # Calendar
    path("calendar/", views.calendar, name="calendar"),
    path("calendar/create/", views.calendar_event_create,name="calendar_event_create"),
    path("calendar/<int:pk>/",views.calendar_event_detail,name="calendar_event_detail"),
    path("calendar/<int:pk>/edit/", views.calendar_event_edit,name="calendar_event_edit"),
    path("calendar/<int:pk>/delete/",views.calendar_event_delete,
    name="calendar_event_delete"),

    # Notifications
    path("notifications/", views.notification_list, name="notifications"),
    path("notifications/mark-all-read/",views.notification_mark_all_read,name="notification_mark_all_read"),
    path("notifications/<int:pk>/",views.notification_detail,name="notification_detail"),
    path("notifications/<int:pk>/read/", views.notification_mark_read,name="notification_mark_read"),

    

    path("settings/", lambda request: views.module_placeholder(request, "Settings"), name="settings"),

    

]
