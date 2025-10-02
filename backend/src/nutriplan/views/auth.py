"""
Authentication and user management views for backend.

This module provides endpoints for user registration, login, and profile retrieval.
"""

from django.contrib.auth import authenticate, get_user_model
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from nutriplan.serializers import UserProfileSerializer, UserRegistrationSerializer
from nutriplan.services.user_service import UserService

CustomUser = get_user_model()


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request: Request) -> Response:
    """
    Register a new user with the provided data.

    Args:
        request: HTTP request containing user registration data.

    Returns:
        Response: A response containing the created user's profile and JWT tokens
                  if successful, or validation errors if registration fails.

    """

    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_user(request: Request) -> Response:
    """
    Authenticate a user and return JWT tokens upon successful login.

    Args:
        request: HTTP request object containing `username` and `password` in its data.

    Returns:
        Response:
            - On success: serialized user profile, refresh token, and access token.
            - On failure: error message and appropriate HTTP status code.

    """

    email = request.data.get("email") or ""  # type: ignore[reportAttributeAccessIssue]
    password = request.data.get("password")  # type: ignore[reportAttributeAccessIssue]

    if not email or not password:
        return Response({"error": "Email y contraseña son requeridos."}, status=400)

    user = authenticate(
        request,  # type: ignore[reportArgumentType]
        username=email,
        password=password,
    )

    if user is None:
        return Response({"error": "Credenciales inválidas."}, status=401)

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "user": UserProfileSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request: Request) -> Response:
    """
    Retrieve the authenticated user's profile along with their dietary restrictions.

    Args:
        request: HTTP request object containing the authenticated user.

    Returns:
        Response: object containing the serialized user profile data.

    """

    return Response(
        UserProfileSerializer(
            UserService.get_user_with_restrictions(request.user.id)
        ).data
    )
