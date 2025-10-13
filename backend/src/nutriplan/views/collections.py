"""
CRUD custom actions for user recipe collections.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.db.models import Max, Prefetch
from django.db.transaction import atomic
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ModelViewSet

from nutriplan.models import (
    CollectionItem,
    Recipe,
    RecipeCollection,
    RecipeImage,
    RecipeIngredient,
)
from nutriplan.serializers import RecipeCollectionSerializer

from .permissions import CollectionAccessPermission

if TYPE_CHECKING:
    from collections.abc import Sequence

    from django.db.models import QuerySet
    from rest_framework.request import Request


class RecipeCollectionViewSet(ModelViewSet):
    """
    API endpoint for interacting with recipe collections.

    Routes:
      - GET    /collections
      - POST   /collections

      - GET    /collections/{slug}
      - PUT    /collections/{slug}
      - PATCH  /collections/{slug}
      - DELETE /collections/{slug}

      - POST   /collections/{slug}/add-recipe    { recipe_id }
      - POST   /collections/{slug}/remove-recipe { recipe_id }
      - POST   /collections/{slug}/reorder       { items: [{recipe_id, order}] }
    """

    serializer_class = RecipeCollectionSerializer
    permission_classes: ClassVar[list[type[BasePermission]]] = [IsAuthenticated]
    lookup_field: ClassVar[str] = "id"

    def get_queryset(self) -> QuerySet[RecipeCollection]:  # type: ignore[reportIncompatibleMethodOverride]
        """
        If the requesting user is a staff member, returns all collections.

        Otherwise, returns only collections owned by the requesting user.

        Returns:
            QuerySet[RecipeCollection]: Filtered and optimized queryset of collections.

        """

        user = self.request.user

        recipe_qs = Recipe.objects.select_related("category").prefetch_related(
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

        qs = RecipeCollection.objects.select_related("owner").prefetch_related(
            Prefetch("items__recipe", queryset=recipe_qs)
        )

        return qs if user.is_staff else qs.filter(owner=user)

    def get_permissions(self) -> list[BasePermission]:
        """
        Returns permission classes that should be applied to current action.

        Returns:
            list: Instantiated permission classes based on the current action.

        """

        if self.action in (
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "add_recipe",
            "remove_recipe",
            "reorder",
        ):
            return [IsAuthenticated(), CollectionAccessPermission()]
        return [IsAuthenticated()]

    @action(detail=False, methods=["get"], url_path=r"by-slug/(?P<slug>[^/]+)")
    def by_slug(self, request: Request, slug: str) -> Response:
        """
        Retrieve collection instance by its slug.

        Args:
            request: HTTP request object.
            slug:    Identifier for collection.
            *args:   Optional positional arguments.
            **kwargs: Optional keyword arguments.

        Returns:
            Response: Object containing serialized collection data if found,
                      or 404 error message if collection doesn't exist.

        """

        qs = self.get_queryset().filter(slug__iexact=slug)

        count = qs.count()
        if count == 0:
            msg = "Colección no encontrada."
            raise NotFound(msg)

        if count > 1:
            raise ValidationError(
                {"slug": "Slug no es único. Usa el ID de la colección."}
            )

        collection = qs.first()
        self.check_object_permissions(request, collection)
        return Response(self.get_serializer(collection).data)

    @action(detail=True, methods=["post"], url_path="add-recipe")
    def add_recipe(
        self,
        request: Request,
        slug: str | None = None,  # noqa: ARG002
        *args: Sequence,  # noqa: ARG002
        **kwargs: dict,  # noqa: ARG002
    ) -> Response:
        """
        Adds a recipe to the specified recipe collection.

        Args:
            request: HTTP request object containing the recipe ID in its data.
            slug:    Identifier for the collection.
            *args:   Optional positional arguments.
            **kwargs: Optional keyword arguments.

        Returns:
            Response: Object containing serialized collection data if successful,
                      or error message if recipe isn't found.

        """

        collection = self.get_object()
        recipe_id = request.data.get("recipe_id")
        if not recipe_id:
            msg = "Se necesita el ID de receta."
            raise ValidationError(msg)

        try:
            recipe = Recipe.objects.get(id=recipe_id)
        except Recipe.DoesNotExist as e:
            msg = "Receta no encontrada en la colección."
            raise ValidationError(msg) from e

        next_order = (collection.items.aggregate(m=Max("order"))["m"] or 0) + 1
        CollectionItem.objects.get_or_create(
            collection=collection, recipe=recipe, defaults={"order": next_order}
        )

        # limpiar prefetched cache para que el serializer vea el ítem recién agregado
        if hasattr(collection, "_prefetched_objects_cache"):
            collection._prefetched_objects_cache.clear()  # noqa: SLF001

        return Response(self.get_serializer(collection).data, status=HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="remove-recipe")
    def remove_recipe(
        self,
        request: Request,
        slug: str | None = None,  # noqa: ARG002
        *args: Sequence,  # noqa: ARG002
        **kwargs: dict,  # noqa: ARG002
    ) -> Response:
        """
        Removes a recipe from the current recipe collection.

        Args:
            request: HTTP request object containing data.
            slug:    Identifier for collection.
            *args:   Optional positional arguments.
            **kwargs: Optional keyword arguments.

        Returns:
            Response: Object containing updated collection data if recipe was removed,
                      or a 404 response if recipe wasn't found in collection.

        Raises:
            ValidationError: If provided data is invalid.

        """

        collection = self.get_object()
        recipe_id = request.data.get("recipe_id")
        if not recipe_id:
            msg = "Se necesita el ID de receta."
            raise ValidationError(msg)

        CollectionItem.objects.filter(
            collection=collection, recipe_id=recipe_id
        ).delete()

        if hasattr(collection, "_prefetched_objects_cache"):
            collection._prefetched_objects_cache.clear()  # noqa: SLF001

        return Response(self.get_serializer(collection).data, status=HTTP_200_OK)

    @action(detail=True, methods=["post"], url_path="reorder")
    def reorder(
        self,
        request: Request,
        slug: str | None = None,  # noqa: ARG002
        *args: Sequence,  # noqa: ARG002
        **kwargs: dict,  # noqa: ARG002
    ) -> Response:
        """
        Reorders the items in a recipe collection based on the provided order.

        Args:
            request: HTTP request object containing the data.
            slug:    Optional slug identifying the collection.
            *args:   Optional positional arguments.
            **kwargs: Optional keyword arguments.

        Request data format:
        --------------------
        {
            "items": [
                {"recipe_id": <str or int>, "order": <int>},
                ...
            ]
        }

        Possible error responses:
        -------------------------
            - If `items` is missing or not a list.
            - If any `order` is not an integer.
            - If any `recipe_id` is missing.
            - If any recipe does not belong to the collection.

        Returns:
            Response: Object with updated collection data if successful,
                      or error message with status 400 if validation fails.

        """

        collection = self.get_object()
        items = request.data.get("items")
        if not isinstance(items, list):
            raise ValidationError({"items": "Lista de items es requerida."})

        with atomic():
            for it in items:
                rid = it.get("recipe_id")
                order = it.get("order")
                if rid is None or order is None:
                    continue

                CollectionItem.objects.filter(
                    collection=collection, recipe_id=rid
                ).update(order=order)

        if hasattr(collection, "_prefetched_objects_cache"):
            collection._prefetched_objects_cache.clear()  # noqa: SLF001

        return Response(self.get_serializer(collection).data, status=HTTP_200_OK)
