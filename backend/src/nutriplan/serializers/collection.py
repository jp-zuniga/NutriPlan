"""
Serializers for recipe collections and items.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from rest_framework.serializers import (
    BooleanField,
    CharField,
    ModelSerializer,
    Serializer,
    SerializerMethodField,
    UUIDField,
    ValidationError,
)

from nutriplan.models import CollectionItem, RecipeCollection

from .recipe import RecipeSerializer

if TYPE_CHECKING:
    from collections.abc import Mapping

    from django.db.models import QuerySet


class CollectionItemReadSerializer(ModelSerializer):
    """
    Read-only item including nested recipe (reusing RecipeSerializer).
    """

    recipe = RecipeSerializer(read_only=True)

    class Meta:
        """
        Read-only fields.
        """

        model = CollectionItem
        fields = read_only_fields = ("id", "order", "added_at", "recipe")


class RecipeCollectionSerializer(ModelSerializer):
    """
    Serializer for collections; owner is inferred from request.user.
    """

    items = SerializerMethodField()
    is_public = BooleanField(required=False)

    class Meta:
        """
        Fields and read-only fields.
        """

        model = RecipeCollection
        fields = (
            "id",
            "slug",
            "name",
            "description",
            "is_public",
            "items",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("id", "slug", "items", "created_at", "updated_at")

    def validate_name(self, value: str) -> str:
        """
        Validate that the collection name is unique for the current user.

        Args:
            value: Name of the collection to validate.

        Returns:
            str: Validated collection name.

        Raises:
            ValidationError: If a collection with the same name exists.

        """

        user = self.context["request"].user
        qs: QuerySet[RecipeCollection] = RecipeCollection.objects.filter(owner=user)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.filter(name__iexact=value).exists():
            msg = "Ya existe una colección con ese nombre."
            raise ValidationError(msg)

        return value

    def get_items(self, obj: RecipeCollection) -> list[dict[str, Any]]:
        """
        Retrieve and serialize the items of a RecipeCollection.

        Args:
            obj: Recipe collection instance whose items are to be retrieved.

        Returns:
            list[dict[str, Any]]: Serialized collection items.

        """

        return CollectionItemReadSerializer(
            obj.items.select_related("recipe").order_by("order", "id"),  # type: ignore[reportAttributeAccessIssue]
            many=True,
        ).data  # type: ignore[reportReturnType]

    def create(self, validated_data: dict) -> RecipeCollection:
        """
        Creates new RecipeCollection instance with provided validated data.

        Args:
            validated_data: Validated data for creating the RecipeCollection.

        Returns:
            RecipeCollection: Newly created RecipeCollection instance.

        """

        user = self.context["request"].user
        return RecipeCollection.objects.create(owner=user, **validated_data)


class AddRemoveRecipeSerializer(Serializer):
    """
    Payload para agregar/quitar recetas.
    """

    recipe_id = UUIDField()


class ReorderItemsSerializer(Serializer):
    """
    Serializer for reordering items within a collection.
    """

    class Item(Serializer):
        """
        Individual item with recipe ID and new order.
        """

        recipe_id = UUIDField()
        order = CharField()

    items = SerializerMethodField()

    def get_items(self, obj: Mapping) -> list[dict[str, Any]]:
        """
        Retrieve the list of items from the given object.

        Args:
            obj: Dictionary-like object containing an `items` key.

        Returns:
            list[dict[str, Any]]: List of dictionaries representing the items.

        """

        return obj["items"]
