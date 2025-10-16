"""
Helpers for managing refresh-token cookies.
"""

from typing import ClassVar, NoReturn

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView


def set_refresh_cookie(response: Response, refresh_token: str) -> None:
    """
    Set an HTTP-only refresh token cookie on the provided HTTP response.

    Args:
        response:      Response object to mutate by setting a cookie.
        refresh_token: Token string to set as the cookie value.

    """

    response.set_cookie(
        key=settings.JWT_REFRESH_COOKIE_NAME,
        value=refresh_token,
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
        httponly=True,
        secure=settings.JWT_COOKIE_SECURE,
        samesite=settings.JWT_COOKIE_SAMESITE,
        domain=getattr(settings, "JWT_COOKIE_DOMAIN", None),
        path=getattr(settings, "JWT_COOKIE_PATH", "/"),
    )


def clear_refresh_cookie(response: Response) -> None:
    """
    Remove the refresh-token cookie from the provided HTTP response.

    Args:
        response: HTTP response object to mutate.

    """

    response.delete_cookie(
        key=settings.JWT_REFRESH_COOKIE_NAME,
        domain=getattr(settings, "JWT_COOKIE_DOMAIN", None),
        path=getattr(settings, "JWT_COOKIE_PATH", "/"),
    )


class CookieTokenRefreshView(TokenRefreshView):
    """
    Token refresh view that supports cookie-based refresh tokens.
    """

    permission_classes: ClassVar[list[type[AllowAny]]] = [AllowAny]

    def post(
        self,
        request: Request,
        *args,  # noqa: ANN002, ARG002
        **kwargs,  # noqa: ANN003, ARG002
    ) -> NoReturn:
        """
        Handle POST requests to obtain or refresh tokens using a serializer.

        Args:
            request:  DRF Request containing the JSON payload and cookies.
            *args:    Additional positional arguments (unused).
            **kwargs: Additional keyword arguments (unused).

        Returns:
            Response: Serializer's validated data with status 200.

        Raises:
            InvalidToken:    If token validation fails with a TokenError.
            ValidationError: If serializer validation fails for other reasons.

        """

        data = request.data.copy()  # type: ignore[reportAttributeAccessIssue]
        if "refresh" not in data or not data["refresh"]:
            data["refresh"] = request.COOKIES.get(settings.JWT_REFRESH_COOKIE_NAME, "")

        serializer = self.get_serializer(data=data)
        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e

        resp = Response(serializer.validated_data, status=200)

        new_refresh = serializer.validated_data.get("refresh")
        if new_refresh:
            set_refresh_cookie(resp, new_refresh)

        return resp
