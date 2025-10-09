"""
LLM utility functions.
"""

from __future__ import annotations

from decimal import InvalidOperation
from typing import Any

from django.db import DataError, DatabaseError, IntegrityError, OperationalError
from rest_framework.exceptions import ValidationError

from nutriplan.models import Category, Ingredient, Recipe, RecipeIngredient

DEFAULT_LOCALE = "es-NI"


def ensure_category(name: str | None) -> Category | None:
    """
    Ensures that a Category object exists for the given name.

    Args:
        name: Name of category to ensure.

    Returns:
        Category | None: Existing or newly created `Category` object,
                         or None if `name` is empty.

    """

    if not name:
        return None

    n = name.strip()
    if not n:
        return None

    try:
        return Category.objects.filter(name__iexact=n).first()
    except (DatabaseError, OperationalError, IntegrityError, DataError):
        return None


def link_ingredients(
    recipe: Recipe, rows: list[dict[str, Any]], ing_by_lower: dict[str, Ingredient]
) -> None:
    """
    Links ingredients from a list of ingredient data rows to a given recipe.

    Args:
        recipe:       Recipe to which ingredients will be linked.
        rows:         List of dictionaries, each representing an ingredient.
        ing_by_lower: Mapping from lower-cased ingredient names to `Ingredient` objects.

    Returns:
        None

    """

    for it in rows or []:
        raw_name = (it.get("name") or "").strip()
        if not raw_name:
            continue
        ing = ing_by_lower.get(raw_name.lower())
        if not ing:
            continue

        amount = it.get("amount")
        unit = (it.get("unit") or "").strip()

        try:
            amount = float(amount)  # type: ignore[reportArgumentType]
        except (TypeError, ValueError, InvalidOperation):
            continue

        if amount <= 0:
            continue

        try:
            RecipeIngredient.objects.get_or_create(
                recipe=recipe,
                ingredient=ing,
                defaults={"amount": amount, "unit": unit},
            )
        except (
            ValidationError,
            IntegrityError,
            DataError,
            OperationalError,
            DatabaseError,
        ):
            # ignorar conflictos/errores de DB por duplicados o tipos
            continue
