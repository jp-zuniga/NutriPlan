"""
Seeders that prompt Gemini for structured data and persist it.
"""

from decimal import InvalidOperation
from typing import Any

from django.db import DataError, DatabaseError, IntegrityError, OperationalError
from django.db.transaction import atomic
from rest_framework.exceptions import ValidationError

from nutriplan.models import Ingredient, Recipe

from .utils import ensure_category, link_ingredients


def seed_ingredients_with_json(  # noqa: C901
    items: list[dict[str, Any]],
) -> tuple[int, int]:
    """
    Seeds the Ingredient database table with a list of ingredient dictionaries.

    Args:
        items: List of ingredient dictionaries. Each dictionary may contain:
            - `name`:               Name of ingredient (required).
            - `description`:        Description of ingredient.
            - `nutrition_per_100g`: Nutritional info per 100g, with keys:
                - `calories`
                - `protein_g`
                - `carbs_g`
                - `fat_g`
                - `sugar_g`

    Returns:
        tuple[int, int]: Number of ingredients created and number of items skipped.

    """

    created = 0
    skipped = 0

    for row in items or []:
        name = (row.get("name") or "").strip()
        if not name:
            skipped += 1
            continue

        desc = (row.get("description") or "").strip() or f"{name}."
        nut = row.get("nutrition_per_100g") or {}
        cal = nut.get("calories", 0) or 0
        pro = nut.get("protein_g", 0) or 0
        carb = nut.get("carbs_g", 0) or 0
        fat = nut.get("fat_g", 0) or 0
        sug = nut.get("sugar_g", 0) or 0

        try:
            obj, was_created = Ingredient.objects.get_or_create(
                name=name,
                defaults={
                    "description": desc,
                    "calories_per_100g": cal,
                    "protein_per_100g": pro,
                    "carbs_per_100g": carb,
                    "fat_per_100g": fat,
                    "sugar_per_100g": sug,
                },
            )

            if not was_created:
                changed = False
                if not obj.description and desc:
                    obj.description = desc
                    changed = True
                if obj.calories_per_100g == 0 and cal:
                    obj.calories_per_100g = cal
                    changed = True
                if obj.protein_per_100g == 0 and pro:
                    obj.protein_per_100g = pro
                    changed = True
                if obj.carbs_per_100g == 0 and carb:
                    obj.carbs_per_100g = carb
                    changed = True
                if obj.fat_per_100g == 0 and fat:
                    obj.fat_per_100g = fat
                    changed = True
                if obj.sugar_per_100g == 0 and sug:
                    obj.sugar_per_100g = sug
                    changed = True
                if changed:
                    obj.save()
            else:
                created += 1
        except (
            ValidationError,
            InvalidOperation,
            ValueError,
            TypeError,
            IntegrityError,
            DataError,
            OperationalError,
            DatabaseError,
        ):
            skipped += 1

    return created, skipped


def seed_recipes_with_json(  # noqa: C901, PLR0912, PLR0915
    items: list[dict[str, Any]],
) -> tuple[int, int]:
    """
    Seeds the database with recipe data from a list of dictionaries.

    Each dictionary in the input list should represent a recipe in the following way:
        - `name`:          Name of the recipe (required).
        - `description`:   Description of the recipe (optional).
        - `servings`:      Number of servings (optional, defaults to 1).
        - `prep_time`:     Preparation time in minutes (optional, defaults to 0).
        - `cook_time`:     Cooking time in minutes (optional, defaults to 0).
        - `category_name`: Name of recipe category (optional).
        - `ingredients`:   List of ingredient data for recipe (optional).

    Args:
        items: List of dictionaries containing recipe data.

    Returns:
        tuple[int, int]: Number of recipes created and number skipped.

    """

    created = 0
    skipped = 0
    ing_by_lower = {i.name.lower(): i for i in Ingredient.objects.all()}

    for row in items or []:
        name = (row.get("name") or "").strip()
        if not name:
            skipped += 1
            continue

        description = (row.get("description") or "").strip() or f"{name}."
        servings = row.get("servings")

        try:
            servings = int(servings) if servings is not None else 1
        except (ValueError, TypeError):
            servings = 1

        if servings < 0:
            servings = 1

        prep_time = row.get("prep_time")
        try:
            prep_time = int(prep_time) if prep_time is not None else 0
        except (ValueError, TypeError):
            prep_time = 0
        prep_time = max(prep_time, 0)

        cook_time = row.get("cook_time")
        try:
            cook_time = int(cook_time) if cook_time is not None else 0
        except (ValueError, TypeError):
            cook_time = 0
        cook_time = max(cook_time, 0)

        category = ensure_category(row.get("category_name"))

        try:
            with atomic():
                recipe, was_created = Recipe.objects.get_or_create(
                    name=name,
                    defaults={
                        "description": description,
                        "category": category,
                        "servings": servings,
                        "prep_time": prep_time,
                        "cook_time": cook_time,
                    },
                )

                changed = False
                if not was_created:
                    if not recipe.description and description:
                        recipe.description = description
                        changed = True
                    if category and recipe.category.id is None:  # type: ignore[reportOptionalMemberAccess]
                        recipe.category = category
                        changed = True
                    if (recipe.servings or 0) in (None, 0) and servings:
                        recipe.servings = servings
                        changed = True
                    if (recipe.prep_time or 0) in (None, 0) and prep_time:
                        recipe.prep_time = prep_time
                        changed = True
                    if (recipe.cook_time or 0) in (None, 0) and cook_time:
                        recipe.cook_time = cook_time
                        changed = True
                    if changed:
                        recipe.save()

                # Vincular ingredientes (DB ops dentro)
                link_ingredients(recipe, row.get("ingredients") or [], ing_by_lower)

                if was_created:
                    created += 1
        except (
            ValidationError,
            InvalidOperation,
            ValueError,
            TypeError,
            IntegrityError,
            DataError,
            OperationalError,
            DatabaseError,
        ):
            skipped += 1

    return created, skipped
