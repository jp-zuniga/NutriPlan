"""
Utilities for managing authentication cookies using Django REST Framework and JWT.
"""

from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


def _cookie_kwargs(max_age: int, path: str = "/") -> dict:
    return {
        "httponly": settings.COOKIE_HTTPONLY,
        "secure": settings.COOKIE_SECURE,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": max_age,
        "path": path,
    }


def set_auth_cookies(response: Response, refresh_token: RefreshToken) -> None:
    """
    Set HTTP cookies for JWT authentication using a Simple JWT refresh token.

    Args:
        response:      DRF Response to which cookies will be added or overwritten.
        refresh_token: JWT refresh token used to generate the access cookie.

    """

    access_max = int(settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds())
    refresh_max = int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds())

    response.set_cookie(
        settings.ACCESS_COOKIE_NAME,
        str(refresh_token.access_token),
        domain=settings.COOKIE_DOMAIN,
        path=settings.COOKIE_PATH,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=access_max,
    )

    response.set_cookie(
        settings.REFRESH_COOKIE_NAME,
        str(refresh_token),
        domain=settings.COOKIE_DOMAIN,
        path=settings.COOKIE_PATH,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=refresh_max,
    )


def update_cookies_from_refresh_response(response: Response) -> None:
    """
    Update a DRF Response by moving JWT tokens from the body into cookies.

    Args:
        response: DRF Response object to mutate in place.

    """

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
            **_cookie_kwargs(refresh_max, "/"),
        )

    for k in ("access", "refresh"):
        response.data.pop(k, None)  # type: ignore[reportOptionalMemberAccess]
    if not response.data:
        response.data = {"ok": True}


def clear_auth_cookies(response: Response) -> None:
    """
    Clear authentication cookies from an HTTP response.

    Args:
        response: HTTP response object to mutate in place.

    """

    response.delete_cookie(settings.ACCESS_COOKIE_NAME, path="/")
    response.delete_cookie(settings.REFRESH_COOKIE_NAME, path="/")
