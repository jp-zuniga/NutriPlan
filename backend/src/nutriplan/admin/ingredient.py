"""
Register admin interface for `Ingredient` model.
"""

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import Ingredient


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    """
    Admin interface options for `Ingredient` model.
    """

    list_display = (
        "name",
        "calories_per_100g",
        "protein_per_100g",
        "carbs_per_100g",
        "fat_per_100g",
        "sugar_per_100g",
    )

    search_fields = ("name", "description")
    ordering = ("name",)
