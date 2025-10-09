"""
Permission classes for ownership verification.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

if TYPE_CHECKING:
    from rest_framework.request import Request

    from nutriplan.models import RecipeCollection
    from nutriplan.views import RecipeCollectionViewSet


class CollectionAccessPermission(BasePermission):
    """
    Only owners (or admins) can read/modify their collections.
    """

    def has_object_permission(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        request: Request,
        view: RecipeCollectionViewSet,  # noqa: ARG002
        obj: RecipeCollection,
    ) -> bool:
        """
        Verify ownership of requesting user.

        Args:
            request: HTTP request object.
            view:    View being accessed.
            obj:     RecipeCollection instance being accessed.

        Returns:
            bool: True if permission is granted, False otherwise.

        """

        user = request.user

        return (
            False
            if not user or not user.is_authenticated
            else bool(user.is_staff or obj.owner_id == user.id)  # type: ignore[reportAttributeAccessIssue]
        )
