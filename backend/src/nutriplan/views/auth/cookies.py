"""
Helpers for managing refresh-token cookies.
"""

from typing import ClassVar

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.views import TokenRefreshView

from .utils import update_cookies_from_refresh_response


class RefreshCookieView(TokenRefreshView):
    """
    Token refresh view that supports cookie-based refresh tokens.
    """

    permission_classes: ClassVar[list[type[AllowAny]]] = [AllowAny]

    def post(
        self,
        request: Request,
        *args,  # noqa: ANN002
        **kwargs,  # noqa: ANN003
    ) -> Response:
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

        data = (
            request.data.copy()  # type: ignore[reportCallIssue]
            if hasattr(request.data, "copy")
            else dict(request.data)  # type: ignore[reportCallIssue]
        )

        if not data.get("refresh"):  # type: ignore[reportArgumentType]
            cookie_refresh = request.COOKIES.get(settings.REFRESH_COOKIE_NAME)
            if cookie_refresh:
                data["refresh"] = cookie_refresh  # type: ignore[reportArgumentType]

        request._full_data = data  # noqa: SLF001

        response = super().post(request, *args, **kwargs)
        if response.status_code == HTTP_200_OK and isinstance(response.data, dict):
            update_cookies_from_refresh_response(response)

        return response
