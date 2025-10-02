"""
URL configuration for Django project.
"""

from django.contrib import admin
from django.contrib.auth import authenticate, login
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.urls import include, path
from rest_framework.views import csrf_exempt


def whoami(request: HttpRequest) -> JsonResponse:
    """
    Test endpoint.
    """

    request.session["ping"] = "pong"
    return JsonResponse(
        {
            "is_auth": request.user.is_authenticated,
            "user": getattr(request.user, "username", None),
            "has_sessionid_cookie": "sessionid" in request.COOKIES,
        }
    )


@csrf_exempt
def test_login(request: HttpRequest) -> HttpResponseBadRequest | JsonResponse:
    """
    Test endpoint.
    """

    if request.method != "POST":
        return HttpResponseBadRequest("POST only")
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None and user.is_active and user.is_staff:
        login(request, user)
        return JsonResponse({"ok": True, "user": user.username})
    return JsonResponse({"ok": False}, status=401)


urlpatterns = [
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
    path("test-login/", test_login),
    path("whoami/", whoami),
]
