"""
Prompts for Gemini using pre-defined JSON schemas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .schemas import CATEGORY_SCHEMA, INGREDIENT_SCHEMA, RECIPE_SCHEMA
from .utils import DEFAULT_LOCALE

if TYPE_CHECKING:
    from collections.abc import Iterable


def build_category_prompt(count: int, locale: str = DEFAULT_LOCALE) -> str:
    """
    Builds a prompt for generating recipe categories.

    Args:
        count:  Number of categories to generate.
        locale: Locale to use for category names and descriptions.

    Returns:
        str: Formatted prompt.

    """

    return f"""
        Eres un asistente culinario. Genera un JSON plano EXACTAMENTE con esta forma:

        {CATEGORY_SCHEMA}

        Reglas:
        - Devuelve un objeto con clave "items" -> lista de {count} categorías.
        - Usa locale {locale}.
        - "name" y "friendly_name" pueden ser iguales; ambos en {locale}.
        - Las categorías deben ser generales.
        - Las categorías deben ser relevantes para recetas nicaragüenses.
        - NO incluyas markdown ni texto fuera del JSON.
    """


def build_ingredient_prompt(count: int, locale: str = DEFAULT_LOCALE) -> str:
    """
    Builds a prompt for generating ingredient items.

    Args:
        count:  Number of ingredient items to generate.
        locale: Locale to use for ingredient names and descriptions.

    Returns:
        str: Formatted prompt.

    """

    return f"""
        Eres un asistente de datos nutricionales.
        Genera un JSON plano con EXACTAMENTE esta forma (sin comentarios ni claves extra):

        {INGREDIENT_SCHEMA}

        Reglas:
        - Devuelve un objeto con clave "items" que contiene una lista de {count} elementos.
        - Usa locale {locale} para nombres y descripciones.
        - "nutrition_per_100g" SIEMPRE es por 100 g (o ml si aplica), con claves:
            - calories
            - protein_g
            - carbs_g
            - fat_g
            - sugar_g
        - Si desconoces alguna cantidad, estima razonablemente.
        - NO incluyas markdown, ni texto fuera del JSON.
    """


def build_recipe_prompt(
    count: int,
    allowed_categories: Iterable[str],
    allowed_ingredients: Iterable[str],
    locale: str = DEFAULT_LOCALE,
) -> str:
    """
    Builds a prompt string for generating recipes.

    Args:
        count:               Number of recipe items to generate.
        locale:              Locale or language to use for the recipes.
        allowed_categories:  Existing categories that recipes can belong to.
        allowed_ingredients: Existing ingredients that can be used in recipes.

    Returns:
        str: Formatted prompt.

    """

    ing_csv = ", ".join(
        sorted({(n or "").strip() for n in allowed_ingredients if n})[:300]
    )

    cat_csv = ", ".join(
        sorted({(c or "").strip() for c in allowed_categories if c})[:100]
    )

    return f"""
        Eres un generador de recetas nicaragüenses.
        Genera un **JSON plano** EXACTAMENTE con esta forma:

        {RECIPE_SCHEMA}

        Reglas:
        - Devuelve un objeto con clave "items" -> lista de {count} recetas.
        - Usa locale {locale}.
        - SOLO puedes usar ingredientes de esta lista (coincidencia exacta, sin inventar): {ing_csv}
        - SOLO puedes usar estas categorías (coincidencia exacta): {cat_csv}
        - Prohibe campos no definidos.
        - "ingredients": cada item debe ser {{ "name": <string>, "amount": <number>, "unit": <string> }}.
        - "servings" entero (entre 1 y 3 si dudas).
        - "prep_time" y "cook_time" enteros >= 0.
        - NO incluyas markdown ni texto fuera del JSON.
    """
