"""
Service layer for handling operations related to Recipe objects.
"""

from collections.abc import Iterable

from django.db.models.manager import BaseManager

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

        return Recipe.objects.filter(categories__name__iexact=category_name)

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

        cats: str | list = (
            recipe_data.get("category") or recipe_data.get("categories") or []
        )  # type: ignore[reportAssignmentType]

        if isinstance(cats, str):
            cats = [cats]

        cat_objs: list[Category] = []
        for c in cats:
            if isinstance(c, Category):
                cat_objs.append(c)
            else:
                obj = Category.objects.filter(name__iexact=str(c)).first()
                if not obj:
                    obj = Category.objects.create(name=str(c), friendly_name=str(c))

                cat_objs.append(obj)

        recipe = Recipe.objects.create(
            name=recipe_data["name"],
            description=recipe_data["description"],
            prep_time=recipe_data.get("prep_time", 0),
            cook_time=recipe_data.get("cook_time", 0),
        )

        if cat_objs:
            recipe.categories.add(*cat_objs)

        for ing in ingredients_data:
            recipe.ingredients.add(
                ing["ingredient"],
                through_defaults={"amount": ing["amount"], "unit": ing.get("unit", "")},
            )

        return recipe
