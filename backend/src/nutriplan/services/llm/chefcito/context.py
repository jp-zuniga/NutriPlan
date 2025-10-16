from __future__ import annotations

from typing import Any

from django.utils.timezone import now

from nutriplan.models import Category, Ingredient, Recipe


def _csv_limit(qs, field: str, limit: int) -> list[str]:
    return list(qs.values_list(field, flat=True)[:limit])


def build_base_context(
    user,
    *,
    max_recipes: int = 220,
    max_ingredients: int = 450,
    max_categories: int = 80,
) -> dict[str, Any]:
    allowed_recipes = _csv_limit(Recipe.objects.order_by("name"), "name", max_recipes)
    allowed_ingredients = _csv_limit(
        Ingredient.objects.order_by("name"), "name", max_ingredients
    )
    allowed_categories = _csv_limit(
        Category.objects.order_by("friendly_name"), "friendly_name", max_categories
    )

    user_ctx: dict[str, Any] = {
        "is_authenticated": bool(getattr(user, "is_authenticated", False))
    }
    if user_ctx["is_authenticated"]:
        user_ctx["dietary_restriction_ids"] = list(
            user.dietary_restrictions.values_list("id", flat=True)
        )

    return {
        "date_iso": now().date().isoformat(),
        "allowed_recipes": allowed_recipes,
        "allowed_ingredients": allowed_ingredients,
        "allowed_categories": allowed_categories,
        "user": user_ctx,
        "features": [
            "Búsqueda y filtros por categoría, tiempo total, macros, e ingredientes.",
            "Recomendación por ingredientes disponibles (receta rápida).",
            "Valoraciones (1-5) y comentarios por receta.",
            "Colecciones/favoritos de usuario.",
            "Registro/login (incluye Google Sign-In).",
        ],
    }
