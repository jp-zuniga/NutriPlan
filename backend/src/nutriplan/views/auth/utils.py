"""
Utilities for managing authentication cookies using Django REST Framework and JWT.
"""

from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def _cookie_kwargs(max_age: int, path: str = "/") -> dict:
    return {
        "httponly": True,
        "secure": settings.COOKIE_SECURE,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": max_age,
        "path": path,
    }


def set_auth_cookies(response: Response, refresh_token: RefreshToken) -> None:
    access_max = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    refresh_max = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

    response.set_cookie(
        settings.ACCESS_COOKIE_NAME,
        str(refresh_token.access_token),
        **_cookie_kwargs(access_max, "/"),
    )

    response.set_cookie(
        settings.REFRESH_COOKIE_NAME,
        str(refresh_token),
        **_cookie_kwargs(refresh_max, "/auth/refresh"),
    )


def update_cookies_from_refresh_response(response: Response) -> None:
    access = response.data.get("access")  # type: ignore[reportOptionalMemberAccess]
    refresh = response.data.get("refresh")  # type: ignore[reportOptionalMemberAccess]

    if access:
        access_max = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
        response.set_cookie(
            settings.ACCESS_COOKIE_NAME,
            access,
            **_cookie_kwargs(access_max, "/"),
        )

    if refresh:
        refresh_max = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())
        response.set_cookie(
            settings.REFRESH_COOKIE_NAME,
            refresh,
            **_cookie_kwargs(refresh_max, "/auth/refresh"),
        )

    for k in ("access", "refresh"):
        response.data.pop(k, None)  # type: ignore[reportOptionalMemberAccess]
    if not response.data:
        response.data = {"ok": True}


def clear_auth_cookies(response: Response) -> None:
    response.delete_cookie(settings.ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(settings.REFRESH_COOKIE_NAME, path="/auth/refresh")
