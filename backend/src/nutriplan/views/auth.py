"""
Authentication and user management views for backend.

This module provides endpoints for user registration, login, and profile retrieval.
"""

from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken

from nutriplan.models import Provider, SocialAccount
from nutriplan.serializers import UserProfileSerializer, UserRegistrationSerializer
from nutriplan.services import UserService
from nutriplan.services.auth import GoogleTokenError, verify_google_id_token

CustomUser = get_user_model()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
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


@api_view(["POST"])
@permission_classes([AllowAny])
def google_sign_in(request: Request) -> Response:
    """
    Handles Google sign-in authentication flow.

    Args:
        request: HTTP request object containing `id_token` in its data.

    Returns:
        Response: Object containing:
            - `user`:    Serialized user profile data.
            - `refresh`: JWT refresh token.
            - `access`:  JWT access token.
            - `created`: Boolean indicating if a new user was created.
                - HTTP 400 if `id_token` is missing or invalid.
                - HTTP 201 if a new user was created, otherwise HTTP 200.

    """

    raw = (request.data or {}).get("id_token")  # type: ignore[reportAttributeAccessIssue]
    if not raw:
        return Response({"error": "id_token requerido."}, status=HTTP_400_BAD_REQUEST)

    try:
        data = verify_google_id_token(raw)
    except GoogleTokenError as e:
        return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

    email = data["email"]
    sub = data["sub"]
    name = data.get("name", "")
    picture = data.get("picture", "")

    parts = name.split()
    first_name = parts[0] if parts else ""
    last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

    sa = (
        SocialAccount.objects.select_related("user")
        .filter(provider=Provider.GOOGLE, provider_user_id=sub)
        .first()
    )

    created_user = False
    if sa:
        user = sa.user
        fields = []

        if picture and getattr(sa, "avatar_url", "") != picture:
            sa.avatar_url = picture
            fields.append("avatar_url")
        if name and getattr(sa, "display_name", "") != name:
            sa.display_name = name
            fields.append("display_name")
        if email and getattr(sa, "email", "") != email:
            sa.email = email
            fields.append("email")
        if fields:
            sa.last_login_at = timezone.now()
            fields.append("last_login_at")
            sa.save(update_fields=fields)
    else:
        user = CustomUser.objects.filter(email__iexact=email).first()
        if not user:
            user = CustomUser.objects.create_user(
                email=email,
                password=None,
                first_name=first_name,
                last_name=last_name,
            )  # type: ignore[reportCallIssue]

            user.set_unusable_password()
            user.save(update_fields=["password"])
            created_user = True

        sa = SocialAccount.objects.create(
            user=user,
            provider=Provider.GOOGLE,
            provider_user_id=sub,
            email=email,
            display_name=name,
            avatar_url=picture,
        )

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "user": UserProfileSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "created": created_user,
        },
        status=HTTP_201_CREATED if created_user else HTTP_200_OK,
    )


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

    email = request.data.get("email").strip().lower() or ""  # type: ignore[reportAttributeAccessIssue]
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
    return Response(
        {
            "user": UserProfileSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    )


@api_view(["POST"])
@permission_classes([AllowAny])
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
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        refresh = RefreshToken.for_user(user)  # type: ignore[reportArgumentType]
        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
