"""
API endpoint for user login authentication.
"""

from django.contrib.auth import authenticate, get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.tokens import RefreshToken

from nutriplan.serializers import UserProfileSerializer

from .cookies import set_refresh_cookie

CustomUser = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request: Request) -> Response:
    """
    Authenticate a user and return JWT tokens upon successful login.

    Args:
        request: HTTP request object containing `username` and `password` in its data.

    Returns:
        Response:
            - On success: Serialized user profile, refresh token, and access token.
            - On failure: Error message and appropriate HTTP status code.

    """

    email = request.data.get("email", "").strip().lower() or ""  # type: ignore[reportAttributeAccessIssue]
    password = request.data.get("password")  # type: ignore[reportAttributeAccessIssue]

    if not email or not password:
        return Response({"error": "Email y contraseña son requeridos."}, status=400)

    user = authenticate(
        request,  # type: ignore[reportArgumentType]
        **{CustomUser.USERNAME_FIELD: email},
        password=password,
    )

    if user is None:
        return Response({"error": "Credenciales inválidas."}, status=401)

    refresh = RefreshToken.for_user(user)
    resp = Response(
        {
            "user": UserProfileSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=HTTP_200_OK,
    )

    set_refresh_cookie(resp, str(refresh))
    return resp
