"""The project's root URL configuration. Each app owns its own urls.py and we include it here."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("circles.urls")),
]
