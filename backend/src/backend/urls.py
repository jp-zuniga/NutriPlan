"""
URL configuration for Django project.
"""

from django.contrib import admin
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.hashers import check_password
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
def test_login(request: HttpRequest) -> HttpResponseBadRequest | JsonResponse:
    """
    Test endpoint.
    """

    if request.method != "POST":
        return HttpResponseBadRequest("POST only.")

    u = request.POST.get("username", "")
    p = request.POST.get("password", "")

    # 1) existe el usuario y coincide la password?
    try:
        user_obj = User.objects.get(username=u)
        exists = True
        pw_matches = check_password(p, user_obj.password)
    except User.DoesNotExist:
        user_obj = None
        exists = False
        pw_matches = False

    # 2) test authenticate()
    user = authenticate(request, username=u, password=p)
    if user is not None and user.is_active and user.is_staff:
        login(request, user)
        return JsonResponse({"ok": True, "user": user.username})

    # 3) devolver test
    return JsonResponse({
        "ok": False,
        "why": "authenticate() returned None",
        "u": u,
        "len_p": len(p),
        "user_exists": exists,
        "password_matches_hash": pw_matches,
    }, status=401)


urlpatterns = [
    path("", include("nutriplan.urls")),
    path("admin/", admin.site.urls),
    path("test-login/", test_login),
    path("whoami/", whoami),
]
