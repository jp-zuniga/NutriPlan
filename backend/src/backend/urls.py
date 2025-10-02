"""
URL configuration for Django project.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
]
