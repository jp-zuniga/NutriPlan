"""
Ingredient model used in recipes.
"""

from decimal import Decimal

from django.db.models import CharField, DecimalField, ManyToManyField, Model, TextField


class Ingredient(Model):
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

    class Meta:
        """
        Class metadata.
        """

        ordering = ("name",)

    def __str__(self) -> str:
        """
        Return ingredient name.
        """

        return self.name
