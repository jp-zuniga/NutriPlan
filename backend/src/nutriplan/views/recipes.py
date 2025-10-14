"""
Read-only viewset for recipes, including search and filter capabilities.
"""

from typing import ClassVar
from uuid import UUID

from django.db.models import Avg, Count, Prefetch, Q
from django.db.models.manager import BaseManager
from rest_framework.decorators import action
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from nutriplan.models import Ingredient, Recipe, RecipeImage, RecipeIngredient, Review
from nutriplan.serializers import (
    RecipeSerializer,
    ReviewReadSerializer,
    ReviewSerializer,
)

MACRO_FIELD_MAP: dict[str, str] = {
    "calories": "calories_per_serving",
    "protein": "protein_per_serving",
    "carbs": "carbs_per_serving",
    "fat": "fat_per_serving",
    "sugar": "sugar_per_serving",
}


def _parse_uuid_list(value: str | None) -> list[UUID]:
    if not value:
        return []

    out: list[UUID] = []

    for part in value.split(","):
        s = part.strip()
        if not s:
            continue

        try:
            out.append(UUID(s))
        except (ValueError, TypeError):
            continue

    return out


class RecipeViewSet(ReadOnlyModelViewSet):
    """
    Read-only API for recipes with search and filters.

    Routes:
      - GET /recipes
      - GET /recipes/{name}

    """

    filter_backends: ClassVar[list[BaseFilterBackend]] = [SearchFilter, OrderingFilter]  # type: ignore[reportAssignmentType]
    lookup_field: ClassVar[str] = "slug"
    ordering: ClassVar[list[str]] = ["-created_at", "name"]
    ordering_fields: ClassVar[list[str]] = [
        "name",
        "prep_time",
        "cook_time",
        "total_time",
        "servings",
        "calories_per_serving",
        "total_calories",
        "protein_per_serving",
        "carbs_per_serving",
        "fat_per_serving",
        "sugar_per_serving",
        "created_at",
        "updated_at",
    ]

    permission_classes: ClassVar[list[type[BasePermission]]] = [AllowAny]
    search_fields: ClassVar[list[str]] = ["name", "description"]
    serializer_class = RecipeSerializer

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
                    "recipe_ingredients",
                    queryset=RecipeIngredient.objects.select_related("ingredient"),
                ),
                Prefetch(
                    "recipe_images",
                    queryset=RecipeImage.objects.select_related("image").order_by(
                        "order", "id"
                    ),
                ),
            )
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

        for key, field in MACRO_FIELD_MAP.items():
            vmin = params.get(f"{key}_min")
            vmax = params.get(f"{key}_max")
            if vmin:
                qs = qs.filter(**{f"{field}__gte": vmin})
            if vmax:
                qs = qs.filter(**{f"{field}__lte": vmax})

        include_ids = _parse_uuid_list(params.get("include_ingredients"))
        if include_ids:
            qs = qs.filter(recipe_ingredients__ingredient_id__in=include_ids)
            qs = qs.annotate(
                match_count=Count("recipe_ingredients__ingredient", distinct=True)
            ).filter(match_count__gte=len(set(include_ids)))

        exclude_ids = _parse_uuid_list(params.get("exclude_ingredients"))
        if exclude_ids:
            qs = qs.exclude(recipe_ingredients__ingredient_id__in=exclude_ids)

        qs = qs.annotate(
            rating_avg=Avg("reviews__rating"),
            rating_count=Count("reviews", distinct=True),
        )

        sort_macro = (params.get("sort_macro") or "").strip().lower()
        if sort_macro in MACRO_FIELD_MAP:
            qs = qs.order_by(f"-{MACRO_FIELD_MAP[sort_macro]}", "-created_at", "name")

        return qs

    @action(detail=True, methods=["get"], permission_classes=[AllowAny])
    def reviews(self, request: Request, slug: str | None = None) -> Response:  # noqa: ARG002
        """
        Return serialized reviews for the current recipe.

        Args:
            request: Incoming DRF request.
            slug:    Optional slug captured from URL; accepted for routing but not used.

        Returns:
            Response: 200 OK with JSON array of serialized reviews (newest first).

        Raises:
            Http404: If recipe does not exist.

        """

        recipe: Recipe = self.get_object()
        qs = (
            Review.objects.filter(recipe=recipe)
            .select_related("user")
            .order_by("-created_at")
        )

        return Response(ReviewReadSerializer(qs, many=True).data)

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def rate(self, request: Request, slug: str | None = None) -> Response:  # noqa: ARG002
        """
        Create a new review for the current recipe and return its serialized data.

        Args:
            request: Incoming DRF request.
            slug:    Optional slug captured from URL; accepted for routing but not used.

        Returns:
            Response: HTTP 201 with serialized review data.

        Raises:
            ValidationError:      If provided review data is invalid.
            Http404:              If recipe does not exist.
            PermissionDenied:     If user lacks permission to create review.
            AuthenticationFailed: If authentication is required and fails.

        """

        recipe: Recipe = self.get_object()
        payload = request.data.copy()
        payload["recipe_id"] = str(recipe.id)
        ser = ReviewSerializer(data=payload, context={"request": request})
        ser.is_valid(raise_exception=True)
        review = ser.save()
        return Response(ReviewReadSerializer(review).data, status=201)
