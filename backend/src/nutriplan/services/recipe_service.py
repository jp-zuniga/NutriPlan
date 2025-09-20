from django.db.models.manager import BaseManager

from nutriplan.models import Recipe


class RecipeService:
    @staticmethod
    def get_recipes_by_category(category_name) -> BaseManager[Recipe]:
        return Recipe.objects.filter(category__name=category_name)

    @staticmethod
    def get_recipes_with_ingredients(ingredient_names) -> BaseManager[Recipe]:
        return Recipe.objects.filter(ingredients__name__in=ingredient_names).distinct()

    @staticmethod
    def create_recipe(recipe_data, ingredients_data) -> Recipe:
        recipe = Recipe.objects.create(
            name=recipe_data["name"],
            description=recipe_data["description"],
            category=recipe_data.get("category"),
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
