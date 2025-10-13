"""
Ingredient model used in recipes.
"""

from decimal import Decimal
from typing import ClassVar

from django.contrib.postgres.indexes import GinIndex
from django.db.models import (
    CharField,
    CheckConstraint,
    DecimalField,
    Index,
    ManyToManyField,
    Q,
    TextField,
)

from .base_model import BaseModel


class Ingredient(BaseModel):
    """
    A raw ingredient with nutrition facts per 100g.
    """

    name = CharField(max_length=120, unique=True)
    description = TextField(blank=True)
    calories_per_100g = DecimalField(max_digits=7, decimal_places=2, default=Decimal(0))
    protein_per_100g = DecimalField(max_digits=6, decimal_places=2, default=Decimal(0))
    carbs_per_100g = DecimalField(max_digits=6, decimal_places=2, default=Decimal(0))
    fat_per_100g = DecimalField(max_digits=6, decimal_places=2, default=Decimal(0))
    sugar_per_100g = DecimalField(max_digits=6, decimal_places=2, default=Decimal(0))
    dietary_restrictions = ManyToManyField(
        "DietaryRestriction", blank=True, related_name="ingredients"
    )

    class Meta(BaseModel.Meta):
        """
        Ensure non-negative nutrition values and indexing for search.
        """

        constraints: ClassVar[list[CheckConstraint]] = [
            CheckConstraint(
                check=None,
                condition=Q(calories_per_100g__gte=0),  # type: ignore[reportCallIssue]
                name="chk_ing_cal_ge_0",
            ),
            CheckConstraint(
                check=None,
                condition=Q(protein_per_100g__gte=0),  # type: ignore[reportCallIssue]
                name="chk_ing_pro_ge_0",
            ),
            CheckConstraint(
                check=None,
                condition=Q(carbs_per_100g__gte=0),  # type: ignore[reportCallIssue]
                name="chk_ing_carb_ge_0",
            ),
            CheckConstraint(
                check=None,
                condition=Q(fat_per_100g__gte=0),  # type: ignore[reportCallIssue]
                name="chk_ing_fat_ge_0",
            ),
            CheckConstraint(
                check=None,
                condition=Q(sugar_per_100g__gte=0),  # type: ignore[reportCallIssue]
                name="chk_ing_sug_ge_0",
            ),
        ]

        indexes: ClassVar[list[Index]] = [
            GinIndex(
                fields=["description"],
                name="gin_trgm_ingredient_desc",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["name"],
                name="gin_trgm_ingredient_name",
                opclasses=["gin_trgm_ops"],
            ),
        ]

        ordering: tuple[str] = ("name",)

    def __str__(self) -> str:
        """
        Return ingredient name.
        """

        return self.name
