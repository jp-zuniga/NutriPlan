"""
Views for handling category-related API endpoints.
"""

from typing import ClassVar

from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from nutriplan.models.category import Category
from nutriplan.serializers.category import CategorySerializer


class CategoryViewSet(ReadOnlyModelViewSet):
    """
    Read-only API for categories.

    Routes:
      - GET /api/categories
      - GET /api/categories/{id}

    """

    filter_backends: ClassVar[list[BaseFilterBackend]] = [SearchFilter, OrderingFilter]  # type: ignore[reportAssignmentType]
    ordering_fields: ClassVar[list[str]] = ["friendly_name", "name"]
    search_fields: ClassVar[list[str]] = ["name", "friendly_name", "description"]
    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("friendly_name", "name")
