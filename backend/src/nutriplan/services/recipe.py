"""
Service layer for handling operations related to Recipe objects.
"""

from collections.abc import Iterable

from django.db.models.manager import BaseManager
from django.db.transaction import atomic

from nutriplan.models import Category, Recipe


class RecipeService:
    """
    Service class for handling operations related to Recipe objects.
    """

    @staticmethod
    def get_recipes_by_category(category_name: str) -> BaseManager[Recipe]:
        """
        Retrieve all Recipe objects that belong to a specific category.

        Args:
            category_name: Name of the category to filter recipes by.

        Returns:
            BaseManager[Recipe]: Queryset with Recipe objects in the specified category.

        """

        return Recipe.objects.filter(category__name__iexact=category_name)

    @staticmethod
    def get_recipes_with_ingredients(
        ingredient_names: Iterable[str],
    ) -> BaseManager[Recipe]:
        """
        Retrieve recipes that contain any of the specified ingredient names.

        Args:
            ingredient_names: List or iterable of ingredient names to filter recipes by.

        Returns:
            BaseManager[Recipe]: Queryset of Recipe objects that include
                                 at least one of the specified ingredients.

        """

        return Recipe.objects.filter(ingredients__name__in=ingredient_names).distinct()

    @staticmethod
    def create_recipe(
        recipe_data: dict[str, int | str], ingredients_data: list[dict[str, int | str]]
    ) -> Recipe:
        """
        Creates a new Recipe instance along with its associated ingredients.

        Args:
            recipe_data:         Dictionary containing the recipe's details.
                - "name":        name of the recipe.
                - "description": description of the recipe.
                - "category":    category of the recipe.
                - "prep_time":   preparation time in minutes, defaults to 0.
                - "cook_time":   cooking time in minutes, defaults to 0.

            ingredients_data:   List of dictionaries, each containing:
                - "ingredient": ingredient instance or identifier to associate.
                - "amount":     quantity of the ingredient.
                - "unit":       unit of measurement, defaults to an empty string.

        Returns:
            Recipe: Created Recipe instance with associated ingredients.

        """

        category = recipe_data.get("category")
        category_obj: Category | None = None

        if isinstance(category, str):
            category_obj = Category.objects.filter(name__iexact=category).first()
            if not category_obj:
                category_obj = Category.objects.create(
                    name=category, friendly_name=category
                )
        elif isinstance(category, Category):
            category_obj = category

        with atomic():
            recipe = Recipe.objects.create(
                name=recipe_data["name"],
                description=recipe_data["description"],
                category=category_obj,
                prep_time=recipe_data.get("prep_time", 0),
                cook_time=recipe_data.get("cook_time", 0),
            )

        for ingredient_data in ingredients_data:
            recipe.ingredients.add(
                ingredient_data["ingredient"],
                through_defaults={
                    "amount": ingredient_data["amount"],
                    "unit": ingredient_data.get("unit", ""),
                },
            )

        return recipe
