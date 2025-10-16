"""
API endpoint for Google sign-in authentication.
"""

from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken

from nutriplan.models import Provider, SocialAccount
from nutriplan.serializers import UserProfileSerializer
from nutriplan.services.auth import google as google_service

from .cookies import set_refresh_cookie

CustomUser = get_user_model()


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
        data = google_service.verify_google_id_token(raw)
    except google_service.GoogleTokenError as e:
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
    resp = Response(
        {
            "user": UserProfileSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "created": created_user,
        },
        status=HTTP_201_CREATED if created_user else HTTP_200_OK,
    )

    set_refresh_cookie(resp, str(refresh))
    return resp
