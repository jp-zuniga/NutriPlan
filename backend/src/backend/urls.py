"""
URL configuration for Django project.
"""

from django.contrib import admin
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import include, path


def root(_request: HttpRequest) -> HttpResponse:
    """
    Handles requests to root URL.
    """

    return HttpResponse("Nutriplan API is running. See /api/ for endpoints.")


def whoami(request: HttpRequest) -> JsonResponse:
    request.session["ping"] = "pong"
    return JsonResponse(
        {
            "is_auth": request.user.is_authenticated,
            "user": getattr(request.user, "username", None),
            "has_sessionid_cookie": "sessionid" in request.COOKIES,
        }
    )


urlpatterns = [
    path("whoami/", whoami),
    path("", root),
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
]
