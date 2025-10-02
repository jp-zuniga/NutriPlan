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
        return JsonResponse({"ok": False, "error": "POST only"}, status=405)
    u = request.POST.get("username", "")
    p = request.POST.get("password", "")
    user = authenticate(request, username=u, password=p)
    if not user:
        return JsonResponse(
            {
                "ok": False,
                "why": "authenticate() returned None",
                "u": u,
                "len_p": len(p),
            },
            status=401,
        )
    login(request, user)
    return JsonResponse({"ok": True, "user": user.username})


urlpatterns = [
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
    path("test-login/", test_login),
    path("whoami/", whoami),
]
