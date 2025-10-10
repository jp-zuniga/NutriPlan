"""
Permission classes for review-related views.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

if TYPE_CHECKING:
    from rest_framework.request import Request

    from nutriplan.models import Review
    from nutriplan.views import ReviewViewSet


class ReviewAccessPermission(BasePermission):
    """
    Only owners or admins can read/modify their collections.
    """

    def has_object_permission(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        request: Request,
        view: ReviewViewSet,  # noqa: ARG002
        obj: Review,
    ) -> bool:
        """
        Determine whether requesting user has object-level access to a given Review.

        Args:
            request: Request containing the authenticated user.
            view:    Viewset handling the request.
            obj:     Instance for which access is being checked.

        Returns:
            bool: True if user is authorized, otherwise False.

        """

        user = request.user
        return bool(
            user and user.is_authenticated and (user.is_staff or obj.user.id == user.id)
        )
