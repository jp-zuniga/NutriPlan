"""
RBAC for Article: users view; staff create/edit; admins delete.
"""

from rest_framework.permissions import BasePermission


class ArticleWritePermission(BasePermission):
    """
    Allows create/update/partial_update for staff; denies others.
    """

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        user = request.user
        return bool(user and user.is_authenticated and user.is_staff)


class ArticleDeletePermission(BasePermission):
    """
    Allows destroy only for admins (superusers).
    """

    def has_permission(self, request, view) -> bool:  # type: ignore[override]
        user = request.user
        return bool(user and user.is_authenticated and user.is_superuser)
