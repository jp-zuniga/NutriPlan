"""
Model for recipe categories.
"""

from typing import ClassVar

from django.contrib.postgres.indexes import GinIndex
from django.db.models import CharField, Index, Model, TextField


class Category(Model):
    """
    Model representing a recipe category, with name and description.
    """

    name = CharField(max_length=100, unique=True)
    friendly_name = CharField(max_length=100, blank=True)
    description = TextField(blank=True)

    class Meta:
        """
        Class metadata.
        """

        indexes: ClassVar[list[Index]] = [
            GinIndex(
                fields=["friendly_name"],
                name="gin_trgm_category_name",
                opclasses=["gin_trgm_ops"],
            ),
        ]

        ordering: ClassVar[list[str]] = ["friendly_name"]
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        """
        Return friendly name if available, else the actual name.
        """

        return self.friendly_name or self.name
