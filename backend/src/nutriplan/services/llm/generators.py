"""
Generators that create data using seeders.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from nutriplan.models import Ingredient

from .prompts import build_ingredient_prompt, build_recipe_prompt
from .seeders import seed_ingredients_with_json, seed_recipes_with_json
from .utils import DEFAULT_LOCALE

if TYPE_CHECKING:
    from nutriplan.services.llm import GeminiClient


def generate_and_seed_ingredients(
    count: int, client: GeminiClient, locale: str = DEFAULT_LOCALE
) -> tuple[int, int]:
    """
    Generates and seeds a specified amount of ingredients using an LLM.

    Args:
        count:  Number of ingredient items to generate.
        client: Language model client used to generate ingredient data.
        locale: Locale to use for ingredient generation.

    Returns:
        tuple[int, int]: Number of successful insertions and number of failures.

    """

    prompt = build_ingredient_prompt(count=count, locale=locale)
    data = client.generate_json(prompt)
    items = list(data.get("items") or [])
    return seed_ingredients_with_json(items)


def generate_and_seed_recipes(
    client: GeminiClient, count: int, locale: str = DEFAULT_LOCALE
) -> tuple[int, int]:
    """
    Generates and seeds a specified number of recipes using an LLM.

    Args:
        client: Language model client used to generate recipes.
        count:  N umber of recipes to generate.
        locale: Locale to use for recipe generation.

    Returns:
        tuple[int, int]: Number of recipes created and number of recipes updated.

    """

    known = (ing.name for ing in Ingredient.objects.all())
    prompt = build_recipe_prompt(count=count, locale=locale, known_ingredients=known)
    data = client.generate_json(prompt)
    items = list(data.get("items") or [])
    return seed_recipes_with_json(items)
