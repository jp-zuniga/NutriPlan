"""
Generators that create data using seeders.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from nutriplan.models import Category, Ingredient

from .prompts import build_category_prompt, build_ingredient_prompt, build_recipe_prompt
from .seeders import seed_ingredients_with_json, seed_recipes_with_json
from .utils import DEFAULT_LOCALE

if TYPE_CHECKING:
    from nutriplan.services.llm import GeminiClient


def generate_and_seed_categories(
    count: int, locale: str, client: GeminiClient
) -> tuple[int, int]:
    """
    Generate and seed categories in database using data from an LLM.

    Args:
        count:  Number of categories to generate.
        locale: Locale to use for category generation.
        client: Client used to generate category data.

    Returns:
        tuple[int, int]: Number of categories created and number skipped.

    """

    created = 0
    skipped = 0
    prompt = build_category_prompt(count=count, locale=locale)
    data = client.generate_json(prompt)
    items = list(data.get("items") or [])

    for row in items:
        name = (row.get("name") or "").strip()
        if not name:
            skipped += 1
            continue
        if Category.objects.filter(name__iexact=name).exists():
            skipped += 1
            continue

        Category.objects.create(
            name=name,
            friendly_name=(row.get("friendly_name") or "").strip() or name,
            description=(row.get("description") or "").strip(),
        )

        created += 1

    return created, skipped


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

    prompt = build_recipe_prompt(
        count=count,
        locale=locale,
        allowed_ingredients=Ingredient.objects.values_list("name", flat=True),
        allowed_categories=Category.objects.values_list("name", flat=True),
    )

    data = client.generate_json(prompt)
    items = list(data.get("items") or [])
    return seed_recipes_with_json(items)
