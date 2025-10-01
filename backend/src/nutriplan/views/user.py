"""
User API: profile management and password change.
"""

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAdminUser, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.viewsets import ModelViewSet

from nutriplan.serializers.user import ChangePasswordSerializer, UserProfileSerializer

User = get_user_model()


class IsSelfOrAdmin(BasePermission):
    """
    Admins can access any user; regular users can only access their own object.
    """

    def has_object_permission(self, request: Request, obj: User) -> bool:  # type: ignore[incompatibleMethodOverride]
        """
        Determine whether the requesting user has permission to access the given object.

        Args:
            request: HTTP request containing user information.
            obj: object for which permission is being checked.

        Returns:
            bool: True if user is authenticated and owns the object; False otherwise.

        """

        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or obj.pk == request.user.pk)
        )


class UserViewSet(ModelViewSet):
    """
    Viewset for managing user profiles.

    Routes:
      - GET /api/users
      - GET /api/users/{id}
      - PUT /api/users/{id}
      - PATCH /api/users/{id}
      - DELETE /api/users/{id}
      - GET /api/users/me
      - PUT /api/users/me
      - PATCH /api/users/me
      - POST /api/users/me/change-password

    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer

    def get_permissions(self) -> list[BasePermission]:
        """
        Determines and returns list of permissions based on current action.

        Returns:
            list: instantiated permission classes.

        """

        if self.action in ("list", "destroy", "create"):
            return [IsAdminUser()]
        if self.action in ("retrieve", "update", "partial_update"):
            return [IsAuthenticated(), IsSelfOrAdmin()]

        return [IsAuthenticated()]

    def get_queryset(self) -> QuerySet:  # type: ignore[incompatibleMethodOverride]
        """
        Returns a queryset filtered by the current authenticated user.

        If the user is staff or not authenticated, returns the default queryset.

        Returns:
            QuerySet: queryset appropiate for current user.

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
            args: Variable length argument list.
            kwargs: Arbitrary keyword arguments.

        Returns:
            Response: response object with a message and HTTP 405 status code.

        """

        return Response(
            {"detail": "Use the registration endpoint."},
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )

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
        Returns serialized data of authenticated user.

        Args:
            request: HTTP request containing user and data.

        Returns:
            Response: object containing serialized user data.

        """

        if request.method in ("PUT", "PATCH"):
            serializer = self.get_serializer(
                request.user,
                data=request.data,
                partial=(request.method == "PATCH"),
            )

            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

        return Response(self.get_serializer(request.user).data)

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
