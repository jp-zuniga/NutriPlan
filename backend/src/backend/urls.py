"""
URL configuration for Django project.
"""

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.hashers import check_password
from django.db import connection
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.urls import include, path
from rest_framework.views import csrf_exempt

User = get_user_model()


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
def test_login(request: HttpRequest) -> JsonResponse:
    """
    Test endpoint.
    """

    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "POST only"}, status=405)

    u = request.POST.get("username", "")
    p = request.POST.get("password", "")

    try:
        obj = User.objects.get(username=u)
        exists = True
        pw_ok = check_password(p, obj.password)
    except User.DoesNotExist:
        exists = False
        pw_ok = False

    user = authenticate(request, username=u, password=p)
    if user:
        login(request, user)
        return JsonResponse({"ok": True, "user": user.username})

    return JsonResponse(
        {
            "ok": False,
            "why": "authenticate() returned None",
            "u": u,
            "len_p": len(p),
            "user_exists": exists,
            "password_matches_hash": pw_ok,
        },
        status=401,
    )


def debug_db(_request: HttpRequest) -> HttpResponseBadRequest | JsonResponse:
    """
    Otro test endpoint.
    """

    info = {
        "alias": connection.alias,
        "engine": connection.settings_dict.get("ENGINE"),
        "name": connection.settings_dict.get("NAME"),
        "host": connection.settings_dict.get("HOST"),
        "port": connection.settings_dict.get("PORT"),
        "user_model": str(User),
        "users_count": User.objects.count(),
        "allowed_hosts": settings.ALLOWED_HOSTS,
        "using_env_DATABASE_URL": bool(settings.DATABASES["default"].get("NAME")),
    }

    first = User.objects.order_by("id").values(
        "id", "username", "email", "is_staff", "is_superuser"
    )[:5]

    return JsonResponse({"db": info, "sample_users": list(first)})


urlpatterns = [
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
    path("debug/db/", debug_db),
    path("test-login/", test_login),
    path("whoami/", whoami),
]
