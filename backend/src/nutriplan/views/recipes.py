"""
Read-only viewset for recipes, including search and filter capabilities.
"""

from typing import ClassVar

from django.db.models import Count, F, Prefetch, Q
from django.db.models.manager import BaseManager
from rest_framework import viewsets
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, BasePermission

from nutriplan.models.ingredient import Ingredient
from nutriplan.models.recipe import Recipe, RecipeImage, RecipeIngredient


def _parse_int_list(value: str | None) -> list[int]:
    if not value:
        return []
    out: list[int] = []

    for part in value.split(","):
        stripped_part = part.strip()
        if not stripped_part:
            continue
        try:
            out.append(int(stripped_part))
        except ValueError:
            continue
    return out


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for recipes with search and filters.

    Routes:
      - GET /api/recipes
      - GET /api/recipes/{name}

    """

    filter_backends: ClassVar[BaseFilterBackend] = [SearchFilter, OrderingFilter]  # type: ignore[reportAssignmentType]
    lookup_field: ClassVar[str] = "name"
    ordering: ClassVar[list[str]] = ["-created_at", "name"]
    ordering_fields: ClassVar[list[str]] = [
        "name",
        "prep_time",
        "cook_time",
        "servings",
        "calories_per_serving",
        "protein_per_serving",
        "carbs_per_serving",
        "fat_per_serving",
        "sugar_per_serving",
        "created_at",
        "updated_at",
    ]

    permission_classes: ClassVar[BasePermission] = [AllowAny]  # type: ignore[reportAssignmentType]
    search_fields: ClassVar[list[str]] = ["name", "description"]

    def get_queryset(self) -> BaseManager[Recipe]:  # type: ignore[reportIncomatibleMethodOverride]
        """
        Return a queryset of Recipe objects according to request parameters.
        """

        qs = (
            Recipe.objects.all()
            .select_related("category")
            .prefetch_related(
                Prefetch("ingredients", queryset=Ingredient.objects.all()),
                Prefetch(
                    "recipeingredient_set",
                    queryset=RecipeIngredient.objects.select_related("ingredient"),
                ),
                Prefetch(
                    "recipeimage_set",
                    queryset=RecipeImage.objects.select_related("image").order_by(
                        "order", "id"
                    ),
                ),
            )
            .annotate(total_time=F("prep_time") + F("cook_time"))
        )

        params = self.request.GET
        category = params.get("category")
        if category:
            if category.isdigit():
                qs = qs.filter(category_id=int(category))
            else:
                qs = qs.filter(
                    Q(category__name__iexact=category)
                    | Q(category__friendly_name__iexact=category)
                )

        time_max = params.get("time_max")
        if time_max and time_max.isdigit():
            qs = qs.filter(total_time__lte=int(time_max))

        macro_map = {
            "calories": "calories_per_serving",
            "protein": "protein_per_serving",
            "carbs": "carbs_per_serving",
            "fat": "fat_per_serving",
            "sugar": "sugar_per_serving",
        }

        for key, field in macro_map.items():
            vmin = params.get(f"{key}_min")
            vmax = params.get(f"{key}_max")
            if vmin:
                qs = qs.filter(**{f"{field}__gte": vmin})
            if vmax:
                qs = qs.filter(**{f"{field}__lte": vmax})

        include_ids = _parse_int_list(params.get("include_ingredients"))
        if include_ids:
            qs = qs.filter(recipeingredient__ingredient_id__in=include_ids)
            qs = qs.annotate(
                match_count=Count("recipeingredient__ingredient", distinct=True)
            )

            qs = qs.filter(match_count__gte=len(set(include_ids)))

        exclude_ids = _parse_int_list(params.get("exclude_ingredients"))
        if exclude_ids:
            qs = qs.exclude(recipeingredient__ingredient_id__in=exclude_ids)

        return qs
