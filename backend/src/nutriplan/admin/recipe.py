"""
Register admin interfaces for all recipe-related models.
"""

from collections.abc import Mapping, Sequence
from typing import ClassVar

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import Recipe, RecipeIngredient


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    """
    Admin interface options for `Recipe` model.
    """

    date_hierarchy = "created_at"
    list_display = ("name", "slug", "created_at")
    list_filter = ("created_at",)
    prepopulated_fields: ClassVar[Mapping[str, Sequence[str]]] = {"slug": ("name",)}  # type: ignore[reportIncompatibleVariableOverride]
    search_fields = ("name", "slug")


@register(RecipeIngredient)
class RecipeIngredientAdmin(ModelAdmin):
    """
    Admin interface options for `RecipeIngredient` model.
    """

    list_display = ("recipe", "ingredient", "amount", "unit")
    search_fields = ("recipe__name", "ingredient__name")
    autocomplete_fields = ("recipe", "ingredient")
