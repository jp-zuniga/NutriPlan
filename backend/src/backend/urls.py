"""
URL configuration for Django project.
"""

from django.contrib.admin import site
from django.urls import URLResolver, include, path, re_path

urlpatterns: list[URLResolver] = [
    path("", include("nutriplan.urls")),
    re_path(r"^admin/?", site.urls),
]
