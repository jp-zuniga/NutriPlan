"""
CRUD for reviews (ratings).
"""

from django.db.models import Avg, Count, Prefetch
from django.db.models.manager import BaseManager
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from nutriplan.models import Ingredient, Recipe, RecipeImage, RecipeIngredient, Review
from nutriplan.serializers import ReviewReadSerializer, ReviewSerializer

from .permissions import ReviewAccessPermission


class ReviewViewSet(ModelViewSet):
    """
    Endpoints for managing recipe reviews.

    Routes:
      - GET    /reviews?recipe=<uuid>
      - POST   /reviews

      - GET    /reviews/{id}
      - PATCH  /reviews/{id}
      - DELETE /reviews/{id}.

    """

    queryset = Review.objects.select_related("recipe", "user").all()
    serializer_class = ReviewSerializer

    def get_permissions(self) -> list[BasePermission]:
        """
        Determine and instantiate permissions for current action.

        Returns:
            list[BasePermission]: Permission instances to apply to request.

        """

        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        if self.action in ("create",):
            return [IsAuthenticated()]

        return [IsAuthenticated(), ReviewAccessPermission()]

    def get_serializer_class(self) -> ReviewSerializer | ReviewReadSerializer:  # type: ignore[reportIncompatibleMethodOverride]
        """
        Return the serializer class appropriate for the current action.

        For read-only operations, return `ReviewReadSerializer`.
        For write operations, return `ReviewSerializer`.

        Returns:
            ReviewReadSerializer | ReviewSerializer: Appropriate class.

        """

        return (  # type: ignore[reportReturnType]
            ReviewReadSerializer
            if self.action in ("list", "retrieve")
            else ReviewSerializer
        )

    def get_queryset(self) -> BaseManager[Review]:  # type: ignore[reportIncompatibleMethodOverride]
        """
        Return the base queryset for this view, optionally filtered and ordered.
        """

        recipe_qs = Recipe.objects.prefetch_related(
            "categories",
            Prefetch(
                "recipe_ingredients",
                queryset=RecipeIngredient.objects.select_related("ingredient"),
            ),
            Prefetch(
                "ingredients",
                queryset=Ingredient.objects.all(),
            ),
            Prefetch(
                "recipe_images",
                queryset=RecipeImage.objects.select_related("image").order_by(
                    "order", "id"
                ),
            ),
        ).annotate(
            rating_avg=Avg("reviews__rating"),
            rating_count=Count("reviews", distinct=True),
        )

        qs = (
            Review.objects.select_related("user")
            .prefetch_related(Prefetch("recipe", queryset=recipe_qs))
            .order_by("-created_at")
        )

        recipe_id = self.request.query_params.get("recipe")  # type: ignore[reportAttributeAccessIssue]
        if recipe_id:
            qs = qs.filter(recipe_id=recipe_id)

        return qs
