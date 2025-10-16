"""
API endpoint for user registration.
"""

from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken

from nutriplan.serializers import UserProfileSerializer, UserRegistrationSerializer

CustomUser = get_user_model()


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
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
