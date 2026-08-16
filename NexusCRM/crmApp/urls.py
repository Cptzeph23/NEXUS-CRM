
from django.contrib import admin
from django.contrib.admin import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
]
