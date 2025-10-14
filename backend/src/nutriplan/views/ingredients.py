"""
Views for listing and retrieving ingredient data via the API.

Provides read-only endpoints for ingredients.
"""

from typing import ClassVar

from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.viewsets import ReadOnlyModelViewSet

from nutriplan.models import Ingredient
from nutriplan.serializers import IngredientSerializer


class IngredientViewSet(ReadOnlyModelViewSet):
    """
    Read-only API for listing/retrieving ingredients.

    Routes:
      - GET /ingredients
      - GET /ingredients/{id}.

    """

    filter_backends: ClassVar[list[type[BaseFilterBackend]]] = [
        SearchFilter,
        OrderingFilter,
    ]

    ordering_fields: ClassVar[list[str]] = [
        "name",
        "calories_per_100g",
        "protein_per_100g",
        "carbs_per_100g",
        "fat_per_100g",
    ]

    search_fields: ClassVar[list[str]] = ["name", "description"]
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all().order_by("name")
