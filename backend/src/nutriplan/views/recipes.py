"""
Read-only viewset for recipes, including search and filter capabilities.
"""

from typing import ClassVar
from uuid import UUID

from django.db.models import Avg, Count, F, Prefetch, Q
from django.db.models.manager import BaseManager
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend, OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from nutriplan.models import Ingredient, Recipe, RecipeImage, RecipeIngredient, Review
from nutriplan.serializers import (
    RecipeSerializer,
    RecommendationRecipeSerializer,
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


def _split_csv(value: str | None) -> list[str]:
    return [] if not value else [v.strip() for v in value.split(",") if v.strip()]


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

    def get_queryset(  # type: ignore[reportIncomatibleMethodOverride]
        self,
    ) -> BaseManager[Recipe]:
        """
        Return a queryset of Recipe objects according to request parameters.
        """

        qs = Recipe.objects.all().prefetch_related(
            "categories",
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

        params = self.request.GET

        # ---- CATEGORÍAS: múltiples tokens (UUID o nombre/friendly) ----
        cat_tokens = _split_csv(params.get("categories") or params.get("category"))
        if cat_tokens:
            q = Q()
            for tok in cat_tokens:
                try:
                    q |= Q(categories__id=UUID(tok))
                except (ValueError, TypeError):
                    q |= Q(categories__name__iexact=tok) | Q(
                        categories__friendly_name__iexact=tok
                    )
            qs = qs.filter(q).distinct()

        # ---- Tiempo total máximo opcional ----
        time_max = params.get("time_max")
        if time_max and time_max.isdigit():
            qs = qs.filter(total_time__lte=int(time_max))

        # ---- Ingredientes include/exclude por UUID (match-all para include) ----
        include_ids = _parse_uuid_list(params.get("include_ingredients"))
        if include_ids:
            qs = qs.filter(recipe_ingredients__ingredient_id__in=include_ids)
            qs = qs.annotate(
                match_count=Count("recipe_ingredients__ingredient", distinct=True)
            ).filter(match_count__gte=len(set(include_ids)))

        exclude_ids = _parse_uuid_list(params.get("exclude_ingredients"))
        if exclude_ids:
            qs = qs.exclude(recipe_ingredients__ingredient_id__in=exclude_ids)

        # ---- Ratings ----
        qs = qs.annotate(
            rating_avg=Avg("reviews__rating"),
            rating_count=Count("reviews", distinct=True),
        )

        # ---- Orden por macro/calorías (DESC). Sin min/max. ----
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

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="recommend",
    )
    def recommend(self, request: Request) -> Response:  # noqa: C901, PLR0912
        """
        Recommend recipes for authenticated user based on available ingredients.

        Filters by user's dietary restrictions and (optionally) by category and macros.

        Return:
            Response: List of serialized recipes.

        """

        data: dict = request.data or {}  # type: ignore[reportAssignmentType]

        # ---- ingredientes: aceptar lista JSON o CSV string usando helpers ----
        raw_ing = data.get("ingredients")
        if isinstance(raw_ing, list):
            ing_ids: list[UUID] = []
            for v in raw_ing:
                try:
                    ing_ids.append(UUID(str(v)))
                except (ValueError, TypeError):
                    continue
        else:
            ing_ids = _parse_uuid_list(raw_ing)

        if not ing_ids:
            raise ValidationError(
                {"ingredients": "Debes enviar al menos un ingrediente."}
            )

        # ---- categorías: aceptar lista JSON o CSV string, separar ids/nombres ----
        raw_cats = data.get("categories", data.get("category"))
        if isinstance(raw_cats, list):
            cat_tokens = [str(v).strip() for v in raw_cats if str(v).strip()]
        else:
            cat_tokens = _split_csv(raw_cats)

        cat_ids: list[UUID] = []
        cat_names: list[str] = []
        for tok in cat_tokens:
            try:
                cat_ids.append(UUID(tok))
            except (ValueError, TypeError):
                cat_names.append(tok)

        macro = (data.get("macro") or "").strip().lower()

        qs = Recipe.objects.all().prefetch_related(
            "categories",  # <-- M2M categories
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

        # Filtro por múltiples categorías (IDs o nombres/friendly) — match cualquiera
        if cat_ids or cat_names:
            q_cat = Q()
            if cat_ids:
                q_cat |= Q(categories__id__in=cat_ids)
            for name in cat_names:
                q_cat |= Q(categories__name__iexact=name) | Q(
                    categories__friendly_name__iexact=name
                )

            qs = qs.filter(q_cat).distinct()

        # Excluir recetas con ingredientes que violen las restricciones del usuario
        user_restr_ids = list(
            request.user.dietary_restrictions.values_list("id", flat=True)
        )

        if user_restr_ids:
            qs = qs.exclude(
                recipe_ingredients__ingredient__dietary_restrictions__id__in=user_restr_ids
            )

        # Anotar missing_count = total_ing - have_ing
        qs = qs.annotate(
            total_ing=Count("recipe_ingredients__ingredient", distinct=True),
            have_ing=Count(
                "recipe_ingredients__ingredient",
                filter=Q(recipe_ingredients__ingredient_id__in=ing_ids),
                distinct=True,
            ),
        ).annotate(missing_count=F("total_ing") - F("have_ing"))

        # Ratings (consistencia con serializer base)
        qs = qs.annotate(
            rating_avg=Avg("reviews__rating"),
            rating_count=Count("reviews", distinct=True),
        )

        # Orden: menos faltantes, (opcional) macro desc, rating desc, nombre
        ordering = ["missing_count", "-rating_avg", "name"]
        if macro in MACRO_FIELD_MAP:
            ordering.insert(1, f"-{MACRO_FIELD_MAP[macro]}")

        qs = qs.order_by(*ordering)
        ser = RecommendationRecipeSerializer(
            qs, many=True, context={"request": request}
        )

        return Response(ser.data)
