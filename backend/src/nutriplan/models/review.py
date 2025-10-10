"""
User reviews/ratings for recipes.
"""

from typing import ClassVar

from django.conf import settings
from django.db.models import (
    CASCADE,
    CheckConstraint,
    DateTimeField,
    ForeignKey,
    Index,
    PositiveSmallIntegerField,
    Q,
    TextField,
    UniqueConstraint,
)

from .base_model import BaseModel
from .recipe import Recipe


class Review(BaseModel):
    """
    A user review for a recipe.
    """

    user = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="reviews"
    )

    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name="reviews")
    rating = PositiveSmallIntegerField()
    comment = TextField(blank=True)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        """
        Ensure one review per recipe per user and that ratings are between 1 and 5.
        """

        constraints: ClassVar[list[CheckConstraint | UniqueConstraint]] = [
            UniqueConstraint(fields=["user", "recipe"], name="uniq_review_user_recipe"),
            CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5), name="chk_rating_1_5"
            ),
        ]

        indexes: ClassVar[list[Index]] = [
            Index(fields=["recipe"], name="idx_review_recipe"),
            Index(fields=["user"], name="idx_review_user"),
            Index(fields=["rating"], name="idx_review_rating"),
            Index(fields=["created_at"], name="idx_review_created"),
        ]

    def __str__(self) -> str:
        """
        Return string representation of `self`.
        """

        return f"{self.user.id} → {self.recipe.id}: {self.rating}★"
