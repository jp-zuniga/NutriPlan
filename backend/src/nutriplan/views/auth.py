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
    username = request.data.get("username")  # type: ignore[reportAttributeAccessIssue]
    password = request.data.get("password")  # type: ignore[reportAttributeAccessIssue]

    if not username or not password:
        return Response(
            {"error": "Username and password are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)
    if user:
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": UserProfileSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )
    return Response(
        {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def get_user_profile(request: Request) -> Response:
    user = UserService.get_user_with_restrictions(request.user.id)
    serializer = UserProfileSerializer(user)
    return Response(serializer.data)
