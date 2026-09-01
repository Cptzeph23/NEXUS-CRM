
from django.contrib import admin
from django.urls import include, path

urlpatterns = [

    path('admin/', admin.site.urls),
    path('', include('crmApp.urls')),
    path("api/v1/", include("crmApp.api.urls")),
]

handler403 = "crmApp.views.permission_denied"
