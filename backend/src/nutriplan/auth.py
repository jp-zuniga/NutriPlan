"""
Authentication utilities for NutriPlan.
"""

from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token

USER = settings.AUTH_USER_MODEL


class CookieJWTAuthentication(JWTAuthentication):
    """
    Authenticate requests using JWT from authorization header or a cookie.
    """

    def authenticate(self, request: Request) -> tuple[USER, Token] | None:
        """
        Authenticate a request using either authorization header or cookies.

        Args:
            request: Incoming request to authenticate.

        Return:
            (CustomUser, Token): User and validated token.
            None:                No applicable credentials are provided.

        """

        # if self.get_header(request) is not None:
        #     return super().authenticate(request)

        raw_token = request.COOKIES.get(
            getattr(settings, "ACCESS_COOKIE_NAME", "access")
        )

        if not raw_token:
            return None

        validated = self.get_validated_token(raw_token)
        return self.get_user(validated), validated
