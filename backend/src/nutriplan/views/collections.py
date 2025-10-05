"""
CRUD + custom actions for user recipe collections.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response

from nutriplan.models import CollectionItem, Recipe, RecipeCollection
from nutriplan.serializers import AddRemoveRecipeSerializer, RecipeCollectionSerializer

if TYPE_CHECKING:
    from django.db.models import QuerySet
    from rest_framework.request import Request


class IsOwnerOrAdmin(BasePermission):
    """
    Only owners (or admins) can read/modify their collections.
    """

    def has_object_permission(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        request: Request,
        view: RecipeCollectionViewSet,  # noqa: ARG002
        obj: RecipeCollection,
    ) -> bool:
        """
        Verify ownership of requesting user.

        Args:
            request: HTTP request object.
            view:    View being accessed.
            obj:     RecipeCollection instance being accessed.

        Returns:
            bool: True if permission is granted, False otherwise.

        """

        user = request.user

        return (
            False
            if not user or not user.is_authenticated
            else bool(user.is_staff or obj.owner_id == user.id)  # type: ignore[reportAttributeAccessIssue]
        )


class RecipeCollectionViewSet(viewsets.ModelViewSet):
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
    lookup_field: ClassVar[str] = "slug"

    def get_queryset(self) -> QuerySet[RecipeCollection]:  # type: ignore[reportIncompatibleMethodOverride]
        """
        If the requesting user is a staff member, returns all collections.

        Otherwise, returns only collections owned by the requesting user.

        Returns:
            QuerySet[RecipeCollection]: Filtered and optimized queryset of collections.

        """

        user = self.request.user
        qs = RecipeCollection.objects.select_related("owner").prefetch_related(
            "items__recipe"
        )

        if user.is_staff:
            return qs

        return qs.filter(owner=user)

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
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["post"], url_path="add-recipe")
    def add_recipe(self, request: Request, slug: str | None = None) -> Response:  # noqa: ARG002
        """
        Adds a recipe to the specified recipe collection.

        Args:
            request: HTTP request object containing the recipe ID in its data.
            slug:    Identifier for the collection.

        Returns:
            Response: Object containing serialized collection data if successful,
                      or error message if recipe isn't found.

        """

        collection: RecipeCollection = self.get_object()
        payload = AddRemoveRecipeSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        recipe_id = payload.validated_data["recipe_id"]
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return Response({"detail": "Receta no encontrada."}, status=404)

        item, created = CollectionItem.objects.get_or_create(
            collection=collection, recipe=recipe
        )

        if created:
            # Set order = max + 1
            max_order = (
                CollectionItem.objects.filter(collection=collection)
                .exclude(pk=item.pk)
                .order_by("-order")
                .values_list("order", flat=True)
                .first()
            ) or 0
            item.order = max_order + 1
            item.save(update_fields=["order"])

        return Response(self.get_serializer(collection).data, status=200)

    @action(detail=True, methods=["post"], url_path="remove-recipe")
    def remove_recipe(self, request: Request, slug: str | None = None) -> Response:  # noqa: ARG002
        """
        Removes a recipe from the current recipe collection.

        Args:
            request: HTTP request object containing data.
            slug:    Identifier for collection.

        Returns:
            Response: Object containing updated collection data if recipe was removed,
                      or a 404 response if recipe wasn't found in collection.

        Raises:
            ValidationError: If provided data is invalid.

        """

        collection: RecipeCollection = self.get_object()
        payload = AddRemoveRecipeSerializer(data=request.data)
        payload.is_valid(raise_exception=True)

        recipe_id = payload.validated_data["recipe_id"]
        deleted, _ = CollectionItem.objects.filter(
            collection=collection, recipe_id=recipe_id
        ).delete()

        if not deleted:
            return Response(
                {"detail": "La receta no estaba en la colección."}, status=404
            )

        return Response(self.get_serializer(collection).data, status=200)

    @action(detail=True, methods=["post"], url_path="reorder")
    def reorder(self, request: Request, slug: str | None = None) -> Response:  # noqa: ARG002
        """
        Reorders the items in a recipe collection based on the provided order.

        Args:
            request: HTTP request object containing the data.
            slug:    Optional slug identifying the collection.

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

        collection: RecipeCollection = self.get_object()
        items = request.data.get("items") or []
        if not isinstance(items, list) or not items:
            return Response(
                {"detail": "Formato inválido: se espera 'items'."}, status=400
            )

        # Normalizamos y validamos
        mapping: dict[str, int] = {}
        for row in items:
            rid = str(row.get("recipe_id", "")).strip()
            try:
                order = int(row.get("order"))
            except Exception:  # noqa: BLE001
                return Response(
                    {"detail": "Todos los 'order' deben ser enteros."}, status=400
                )
            if not rid:
                return Response(
                    {"detail": "Falta recipe_id en algún item."}, status=400
                )
            mapping[rid] = order

        qs = CollectionItem.objects.filter(
            collection=collection, recipe_id__in=mapping.keys()
        )

        if qs.count() != len(mapping):
            return Response(
                {"detail": "Alguna receta no pertenece a la colección."}, status=400
            )

        # Aplicamos en bloque
        for ci in qs:
            new_order = mapping[str(ci.recipe_id)]
            if ci.order != new_order:
                ci.order = new_order
                ci.save(update_fields=["order"])

        return Response(self.get_serializer(collection).data, status=200)
