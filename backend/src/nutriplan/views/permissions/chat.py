"""
Permissions for chat threads/messages.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from rest_framework.permissions import BasePermission

if TYPE_CHECKING:
    from rest_framework.request import Request

    from nutriplan.models import ChatThread
    from nutriplan.views import ChatThreadViewSet


class ChatAccessPermission(BasePermission):
    """
    Owner or admin can access the thread.
    """

    def has_object_permission(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        request: Request,
        view: ChatThreadViewSet,  # noqa: ARG002
        obj: ChatThread,
    ) -> bool:
        user = request.user
        return bool(
            user
            and user.is_authenticated
            and (user.is_staff or obj.owner_id == user.id)  # type: ignore[reportAttributeAccessIssue]
        )
