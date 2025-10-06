"""
Models for user-owned recipe collections (lists) and their items.
"""

from typing import ClassVar
from uuid import uuid4

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    PositiveIntegerField,
    SlugField,
    UniqueConstraint,
)
from django.db.models.functions import Lower
from django.utils.text import slugify

from .base_model import BaseModel
from .recipe import Recipe
from .user import CustomUser


class RecipeCollection(BaseModel):
    """
    A user-owned list of recipes. Name must be unique per owner.
    """

    owner = ForeignKey(CustomUser, on_delete=CASCADE, related_name="recipe_collections")
    name = CharField(max_length=100)
    slug = SlugField(max_length=120, db_index=True)
    description = CharField(max_length=200, blank=True)
    is_public = BooleanField(default=False)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        """
        Ensure per-owner uniqueness and fast lookups.
        """

        constraints: ClassVar[list[UniqueConstraint]] = [
            UniqueConstraint(
                "owner", Lower("name"), name="uniq_collection_name_per_owner_ci"
            ),
            UniqueConstraint(
                "owner", Lower("slug"), name="uniq_collection_slug_per_owner_ci"
            ),
        ]

        indexes: ClassVar[list[Index]] = [
            Index("owner", Lower("name"), name="idx_collection_owner_name_ci"),
            Index("owner", "created_at", name="idx_collection_owner_created"),
            Index(Lower("slug"), name="idx_collection_slug_ci"),
        ]

        ordering: tuple[str, str] = ("-created_at", "name")

    def __str__(self) -> str:
        """
        Return collection name with owner email.
        """

        return f"{self.name} ({self.owner.email})"

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """
        Saves current instance, automatically generating a slug if it doesn't exist.

        If the `slug` attribute is not set, it's generated from `name` using `slugify`.
        If `name` is not provided or `slugify` returns an empty string,
        a UUID4 string is used as the slug.

        Calls the superclass's `save` method to persist the instance.

        Args:
            *args: Variable length argument list passed to the superclass save method.
            **kwargs: Arbitrary keyword arguments passed to the superclass save method.

        """

        if not self.slug:
            base = slugify(self.name or "")
            self.slug = base or str(uuid4())

        super().save(*args, **kwargs)


class CollectionItem(BaseModel):
    """
    Through table linking recipes to collections with explicit order.
    """

    collection = ForeignKey(RecipeCollection, on_delete=CASCADE, related_name="items")
    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name="in_collections")
    order = PositiveIntegerField(default=0)
    added_at = DateTimeField(auto_now_add=True)

    class Meta(BaseModel.Meta):
        """
        Ensure unique recipe per collection and fast lookups.
        """

        constraints: tuple[UniqueConstraint] = (
            UniqueConstraint(
                fields=["collection", "recipe"], name="uniq_collection_recipe"
            ),
        )

        indexes: ClassVar[list[Index]] = [
            Index(
                fields=["collection", "order", "id"], name="idx_collectionitem_order"
            ),
            Index(fields=["recipe"], name="idx_collectionitem_recipe"),
        ]

        ordering = ("order", "id")

    def __str__(self) -> str:
        """
        Return collection name, recipe name, and order number.
        """

        return f"{self.collection.name} → {self.recipe.name} (#{self.order})"
