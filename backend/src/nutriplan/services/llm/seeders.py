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


def seed_recipes_with_json(  # noqa: C901
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
    allowed_categories = {
        c.name  # type: ignore[reportAttributeAccessIssue]
        for c in Recipe._meta.get_field(  # noqa: SLF001
            "category"
        ).remote_field.model.objects.all()
    }

    for row in items or []:
        name = (row.get("name") or "").strip()
        if not name:
            skipped += 1
            continue

        description = (row.get("description") or "").strip() or f"{name}."

        def _safe_int(v: Any, default: int = 0) -> int:  # noqa: ANN401
            try:
                return max(int(v), 0)
            except (TypeError, ValueError):
                return default

        servings = _safe_int(row.get("servings"), default=1) or 1
        prep_time = _safe_int(row.get("prep_time"), default=0)
        cook_time = _safe_int(row.get("cook_time"), default=0)

        cat_name = (row.get("category_name") or "").strip()
        category = None
        if cat_name and cat_name in allowed_categories:
            category = ensure_category(cat_name)

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
                    if (recipe.servings or 0) == 0 and servings:
                        recipe.servings = servings
                        changed = True
                    if (recipe.prep_time or 0) == 0 and prep_time:
                        recipe.prep_time = prep_time
                        changed = True
                    if (recipe.cook_time or 0) == 0 and cook_time:
                        recipe.cook_time = cook_time
                        changed = True
                    if changed:
                        recipe.save()

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
