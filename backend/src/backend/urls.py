"""
URL configuration for Django project.
"""

from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.urls import include, path


def root(_request: HttpRequest) -> HttpResponse:
    """
    Handles requests to root URL.
    """

    return HttpResponse("Nutriplan API is running. See /api/ for endpoints.")


urlpatterns = [
    path("", root),
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
]
