"""
URL configuration for Django project.
"""

from django.contrib import admin
from django.http import HttpRequest, JsonResponse
from django.urls import include, path


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
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
    path("whoami/", whoami),
]
