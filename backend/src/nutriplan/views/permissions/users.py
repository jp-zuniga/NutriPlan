"""
Permission classes for user-related views.
"""

from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

CustomUser = get_user_model()


class UserAccessPermission(BasePermission):
    """
    Admins can access any user; regular users can only access their own object.
    """

    def has_object_permission(self, request: Request, obj: CustomUser) -> bool:  # type: ignore[incompatibleMethodOverride]
        """
        Determine whether the requesting user has permission to access the given object.

        Args:
            request: HTTP request containing user information.
            obj:     Object for which permission is being checked.

        Returns:
            bool: True if user is authenticated and owns the object; False otherwise.

        """

        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or obj.pk == request.user.pk)
        )
