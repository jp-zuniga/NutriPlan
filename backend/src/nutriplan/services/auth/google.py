"""
Google OAuth token verification service.
"""

from __future__ import annotations

from typing import Any

from django.conf import settings
from django.core.exceptions import PermissionDenied
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token


class GoogleTokenError(PermissionDenied):
    """
    Exception raised when there is an error with Google OAuth token validation.

    This exception indicates that the provided Google OAuth token is invalid,
    expired, or otherwise cannot be used to authenticate the user.
    """


def verify_google_id_token(raw_id_token: str) -> dict[str, Any]:
    """
    Verifies and decodes a Google ID token, ensuring it's valid and extracts user info.

    Args:
        raw_id_token: Raw Google ID token as a string.

    Returns:
        dict[str, Any]: Dictionary containing user information extracted:
            - email:       User's email address.
            - sub:         User's unique Google subject ID.
            - name:        User's full name.
            - picture:     URL to the user's profile picture.
            - given_name:  User's given name.
            - family_name: User's family name.

    Raises:
        GoogleTokenError: If token is missing, invalid, not intended for this project,
                          issued by an invalid issuer, the email is not verified,
                          or the domain is not authorized.

    """

    if not raw_id_token:
        msg = "Token ausente."
        raise GoogleTokenError(msg)

    req = google_requests.Request()
    try:
        payload = id_token.verify_oauth2_token(raw_id_token, req)
    except Exception as e:
        msg = f"Token inválido: {e}"
        raise GoogleTokenError(msg) from e

    aud = payload.get("aud")
    iss = payload.get("iss")
    email = (payload.get("email") or "").strip().lower()
    email_verified = payload.get("email_verified") is True
    sub = payload.get("sub")
    hd = (payload.get("hd") or "").strip()

    if not settings.GOOGLE_CLIENT_ID or aud != settings.GOOGLE_CLIENT_ID:
        msg = "aud no corresponde a este proyecto."
        raise GoogleTokenError(msg)
    if iss not in ("https://accounts.google.com", "accounts.google.com"):
        msg = "iss inválido."
        raise GoogleTokenError(msg)
    if not email or not email_verified:
        msg = "Email no verificado en Google."
        raise GoogleTokenError(msg)
    if settings.GOOGLE_HD and hd.lower() != settings.GOOGLE_HD.lower():
        msg = "Dominio no autorizado."
        raise GoogleTokenError(msg)

    return {
        "email": email,
        "sub": sub,
        "name": payload.get("name") or "",
        "picture": payload.get("picture") or "",
        "given_name": payload.get("given_name") or "",
        "family_name": payload.get("family_name") or "",
    }
