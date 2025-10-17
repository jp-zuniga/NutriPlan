"""
CRUD API for Articles with RBAC and auto-sync recipe references.
"""

from typing import ClassVar

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from nutriplan.models import Article
from nutriplan.serializers import ArticleSerializer

from .permissions import ArticleDeletePermission, ArticleWritePermission


class ArticleViewSet(ModelViewSet):
    """
    Articles endpoint.

    Routes:
      - GET    /articles
      - POST   /articles        (staff)
      - GET    /articles/{slug}
      - PUT    /articles/{slug} (staff)
      - PATCH  /articles/{slug} (staff)
      - DELETE /articles/{slug} (admin)
    """

    filter_backends: ClassVar[list[type[SearchFilter | OrderingFilter]]] = [
        SearchFilter,
        OrderingFilter,
    ]  # type: ignore[assignment]

    lookup_field: ClassVar[str] = "slug"
    ordering_fields: ClassVar[list[str]] = ["created_at", "updated_at", "title"]
    search_fields: ClassVar[list[str]] = ["title", "text", "slug", "author__email"]
    serializer_class = ArticleSerializer
    queryset = (
        Article.objects.select_related("author").prefetch_related("recipes").all()
    )

    def get_permissions(self) -> list[BasePermission]:
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        if self.action in ("create", "update", "partial_update"):
            return [IsAuthenticated(), ArticleWritePermission()]
        if self.action in ("destroy",):
            return [IsAuthenticated(), ArticleDeletePermission()]

        msg = "Unhandled action for permissions"
        raise RuntimeError(msg)
