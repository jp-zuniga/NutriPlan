"""
Logout endpoint for clearing the refresh-token cookie.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT

from nutriplan.views.auth.cookies import clear_refresh_cookie


@api_view(["POST"])
@permission_classes([AllowAny])
def logout_user(request: Request) -> Response:  # noqa: ARG001
    """
    Log out the current user by clearing the refresh-token cookie.

    Args:
        request (Request): Incoming HTTP request.

    Return:
        Response: HTTP 204 and Set-Cookie header that clears refresh token cookie.

    """

    resp = Response(status=HTTP_204_NO_CONTENT)
    clear_refresh_cookie(resp)
    return resp
