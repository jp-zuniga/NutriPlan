"""
User API: profile management and password change.
"""

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from nutriplan.serializers import ChangePasswordSerializer, UserProfileSerializer
from nutriplan.services import UserService

from .auth.utils import set_auth_cookies
from .permissions import UserAccessPermission

User = get_user_model()


class UserViewSet(ModelViewSet):
    """
    Viewset for managing user profiles.

    Routes:
      - GET /users

      - GET /users/{id}
      - PUT /users/{id}
      - PATCH /users/{id}
      - DELETE /users/{id}

      - GET /users/me
      - PUT /users/me
      - PATCH /users/me
      - POST /users/me/change-password

    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self) -> list[BasePermission]:
        """
        Determines and returns list of permissions based on current action.

        Returns:
            list: Instantiated permission classes.

        """

        if self.action in ("list", "destroy", "create"):
            return [IsAdminUser()]
        if self.action in ("retrieve", "update", "partial_update"):
            return [IsAuthenticated(), UserAccessPermission()]

        return [IsAuthenticated()]

    def get_queryset(self) -> QuerySet:  # type: ignore[incompatibleMethodOverride]
        """
        Return a queryset filtered by the current authenticated user.

        If the user is staff or not authenticated, returns the default queryset.

        Returns:
            QuerySet: Queryset appropiate for current user.

        """

        user = self.request.user
        if user and user.is_authenticated and not user.is_staff:
            return super().get_queryset().filter(pk=user.pk)

        return super().get_queryset()

    def create(self, request: Request, *args: list, **kwargs: dict) -> Response:  # noqa: ARG002
        """
        Handles attempts to create a user via this endpoint.

        This method overrides the default create behavior to prevent user creation
        through this view. Instead, it instructs clients to use the designated
        registration endpoint by returning a 405 Method Not Allowed response.

        Args:
            request: HTTP request object.
            args:    Variable length argument list.
            kwargs:  Arbitrary keyword arguments.

        Returns:
            Response: Object with a message and HTTP 405 status code.

        """

        msg = "POST"
        raise MethodNotAllowed(msg, detail="Use the registration endpoint.")

    @action(
        detail=False,
        methods=["get", "put", "patch"],
        url_path="me",
        permission_classes=[IsAuthenticated],
    )
    def me(self, request: Request) -> Response:
        """
        Handles retrieval and update of the authenticated user's information.

        If the request method is PUT/PATCH, updates user's data with provided payload.
        Validates input data and performs update operation.
        Return serialized data of authenticated user.

        Args:
            request: HTTP request containing user and data.

        Returns:
            Response: Object containing serialized user data.

        """

        if request.method in ("PUT", "PATCH"):
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=(request.method == "PATCH"),
            )
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        user = UserService.get_user_with_restrictions(request.user.id)
        res = Response(self.get_serializer(user).data)
        refresh = RefreshToken.for_user(user)
        set_auth_cookies(res, refresh)

        return res

    @action(
        detail=False,
        methods=["post"],
        url_path="me/change-password",
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request: Request) -> Response:
        """
        Handles a password change request for the authenticated user.

        Validates the provided data using ChangePasswordSerializer, updates
        user's password with the new value, and saves the change to the database.

        Args:
            request: HTTP request containing user and password data.

        Returns:
            Response: HTTP 204 response indicating successful password change.

        """

        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )

        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(
            serializer.validated_data[  # type: ignore[reportIndexIssue, reportOptionalSubscript]
                "new_password"
            ]
        )

        user.save(update_fields=["password"])
        return Response(status=HTTP_204_NO_CONTENT)
