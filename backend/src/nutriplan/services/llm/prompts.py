"""
Prompts for Gemini using pre-defined JSON schemas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .schemas import INGREDIENT_SCHEMA, RECIPE_SCHEMA
from .utils import DEFAULT_LOCALE

if TYPE_CHECKING:
    from collections.abc import Iterable


def build_ingredient_prompt(count: int, locale: str = DEFAULT_LOCALE) -> str:
    """
    Builds a prompt for generating ingredient items.

    Args:
        count:  Number of ingredient items to generate in the JSON object.
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
        calories, protein_g, carbs_g, fat_g, sugar_g. Si desconoces "sugar_g", estima razonablemente.
        - NO incluyas markdown, ni texto fuera del JSON.
    """


def build_recipe_prompt(
    count: int,
    known_ingredients: Iterable[str],
    locale: str = DEFAULT_LOCALE,
) -> str:
    """
    Builds a prompt string for generating recipes.

    Args:
        count:             Number of recipe items to generate.
        locale:            Locale or language to use for the recipes.
        known_ingredients: Ingredient names that the recipes can use.

    Returns:
        str: Formatted prompt.

    """

    ingredients_csv = ", ".join(
        sorted({(n or "").strip() for n in known_ingredients if n})[:200]
    )

    return f"""
        Eres un generador de recetas nicaragüenses.
        Genera un JSON plano con EXACTAMENTE esta forma (sin comentarios ni claves extra):

        {RECIPE_SCHEMA}

        Reglas:
        - Devuelve un objeto con clave "items" que contiene una lista de {count} recetas.
        - Usa locale {locale}.
        - Solo puedes usar ingredientes de esta lista (coincidencia exacta por nombre, sin cambiarlo): {ingredients_csv}
        - "ingredients" debe ser una lista con objetos: {{ "name": <string>, "amount": <number>, "unit": <string> }}.
        - Si no estás seguro de "servings", usa 2 o 4.
        - "prep_time" y "cook_time" son minutos (enteros >= 0).
        - "category_name" debe ser una categoría culinaria razonable (p.ej., Ensaladas, Sopas, Postres).
        - NO incluyas markdown, ni texto fuera del JSON.
    """
