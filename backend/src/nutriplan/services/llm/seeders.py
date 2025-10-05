"""
Seeders that prompt Gemini for structured data and persist it.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db import transaction

from nutriplan.models import Category, Ingredient, Recipe

if TYPE_CHECKING:
    from collections.abc import Iterable

    from nutriplan.services.llm.gemini import GeminiClient


INGREDIENT_SCHEMA_EXAMPLE: dict[str, list[dict[str, str | dict[str, int | float]]]] = {
    "items": [
        {
            "name": "Tomato",
            "description": "Fresh red tomato commonly used in salads and sauces.",
            "category_name": "Vegetables",
            "unit": "g",
            "nutrition": {
                "calories": 18,
                "protein_g": 0.9,
                "carbs_g": 3.9,
                "fat_g": 0.2,
            },
        }
    ]
}

RECIPE_SCHEMA_EXAMPLE: dict[
    str, list[dict[str, int | str | list[str] | list[dict[str, str | int]]]]
] = {
    "items": [
        {
            "name": "Simple Tomato Salad",
            "description": "A refreshing salad highlighting ripe tomatoes.",
            "instructions": [
                "Slice the tomatoes.",
                "Season with salt, pepper, and olive oil.",
                "Garnish with basil.",
            ],
            "category_name": "Salads",
            "servings": 2,
            "ingredients": [
                {"name": "Tomato", "quantity": 200, "unit": "g"},
                {"name": "Olive oil", "quantity": 1, "unit": "tbsp"},
                {"name": "Salt", "quantity": 1, "unit": "pinch"},
            ],
        }
    ]
}


def build_ingredient_prompt(count: int, locale: str) -> str:
    """
    Builds a prompt for generating ingredient items.

    Args:
        count: number of ingredient items to generate in the JSON object.
        locale: locale to use for ingredient names and descriptions.

    Returns:
        str: formatted prompt.

    """

    return f"""
        You are a nutrition data assistant.
        Generate a JSON object exactly like this schema (no extra keys):

        {INGREDIENT_SCHEMA_EXAMPLE}

        Rules:
        - Return exactly: an object with key "items" -> list of {count} items.
        - Use locale {locale} for names and descriptions.
        - category_name should be a common food category (e.g., Meat, Fruits, Dairy).
        - nutrition values are per 100 unit (if unknown, use grams and estimate).
        - Do not include comments or markdown.
    """


def build_recipe_prompt(
    count: int, locale: str, known_ingredients: Iterable[str]
) -> str:
    """
    Builds a prompt string for generating recipes.

    Args:
        count: number of recipe items to generate.
        locale: locale or language to use for the recipes.
        known_ingredients: ingredient names that the recipes can use.

    Returns:
        str: formatted prompt string.

    """

    ingredients_csv = ", ".join(sorted(set(known_ingredients))[:200])
    return f"""
        You are a recipe generator.
        Produce a JSON object exactly like this schema (no extra keys):

        {RECIPE_SCHEMA_EXAMPLE}

        Rules:
        - Return exactly: an object with key "items" -> list of {count} items.
        - Use locale {locale}.
        - Choose realistic recipes that can be assembled from: {ingredients_csv}
        - ingredients[*].name MUST match from the known list; otherwise omit it.
        - instructions: 3-10 concise steps as plain text.
        - If uncertain about servings, use 2 or 4.
        - Do not include comments or markdown.
    """


def _safe_assign(model_obj, data: dict[str, Any], allowed: Iterable[str]) -> None:  # noqa: ANN001
    """
    Assign only whitelisted keys if the attribute exists on the model instance.
    """

    for key in allowed:
        if hasattr(model_obj, key) and key in data:
            setattr(model_obj, key, data[key])


def _ensure_category(name: str | None) -> Category | None:
    if not name:
        return None

    category, _ = Category.objects.get_or_create(name=name.strip())
    return category


def _get_first_present_name(names: Iterable[str], in_set: set[str]) -> str | None:
    for n in names:
        if n in in_set:
            return n

    return None


def _link_ingredients_with_quantities(  # noqa: C901, PLR0912
    recipe: Recipe, row_ings: list[dict[str, Any]], ing_by_name: dict[str, Ingredient]
) -> None:
    """
    Link ingredients to a recipe.
    """

    if not hasattr(recipe, "ingredients"):
        return

    mgr = recipe.ingredients
    through_model = getattr(mgr, "through", None)
    metadata = through_model._meta  # noqa: SLF001 # type: ignore[reportOptionalMemberAccess]

    resolved = []
    for item in row_ings or []:
        n = (item.get("name") or "").strip().lower()
        if not n or n not in ing_by_name:
            continue
        resolved.append(
            (
                ing_by_name[n],
                item.get("quantity"),
                (item.get("unit") or "").strip() or None,
            )
        )

    if not resolved:
        return

    auto_created = getattr(metadata, "auto_created", False) if through_model else True

    if not through_model or auto_created:
        mgr.add(*[ing.pk for ing, _, _ in resolved])
        return

    field_names = {f.name for f in metadata.get_fields()}
    recipe_fk = None
    ingredient_fk = None

    for f in metadata.get_fields():
        rel_model = getattr(f, "related_model", None)
        if rel_model is None:
            continue
        if rel_model is type(recipe) and recipe_fk is None:
            recipe_fk = f.name
        if (
            rel_model is type(next(iter(ing_by_name.values())))
            and ingredient_fk is None
        ):
            ingredient_fk = f.name

    qty_field = _get_first_present_name(
        ("quantity", "amount", "qty", "quantity_g", "weight", "weight_g"), field_names
    )

    unit_field = _get_first_present_name(
        ("unit", "measurement_unit", "unit_name", "uom"), field_names
    )

    recipe_fk = recipe_fk or "recipe"
    ingredient_fk = ingredient_fk or "ingredient"

    for ing, qty, unit in resolved:
        defaults = {}
        if qty_field and isinstance(qty, (int, float)):
            defaults[qty_field] = qty
        if unit_field and unit:
            defaults[unit_field] = unit

        try:
            through_model.objects.get_or_create(
                **{recipe_fk: recipe, ingredient_fk: ing},
                defaults=defaults,
            )
        except Exception:  # noqa: BLE001
            try:
                obj = through_model(
                    **{recipe_fk: recipe, ingredient_fk: ing} | defaults
                )

                obj.save()
            except Exception:  # noqa: BLE001, S110
                pass


def seed_ingredients_with_json(items: list[dict[str, Any]]) -> tuple[int, int]:  # noqa: C901, PLR0912
    """
    Persist ingredient items. Return (created, skipped).
    """

    created = 0
    skipped = 0
    for row in items:
        name = (row.get("name") or "").strip()
        if not name:
            skipped += 1
            continue

        category = _ensure_category(row.get("category_name"))
        description = (row.get("description") or "").strip() or f"{name} ingredient."
        unit = (row.get("unit") or "").strip() or "g"
        nutrition = row.get("nutrition") or {}
        ing_defaults: dict[str, Any] = {}

        if category:
            ing_defaults["category"] = category
        if description:
            ing_defaults["description"] = description

        if (
            unit
            and hasattr(Ingredient, "_meta")
            and any(f.name == "unit" for f in Ingredient._meta.get_fields())  # noqa: SLF001
        ):
            ing_defaults["unit"] = unit

        for fld, src in [
            ("calories", "calories"),
            ("protein_g", "protein_g"),
            ("carbs_g", "carbs_g"),
            ("fat_g", "fat_g"),
        ]:
            if (
                any(f.name == fld for f in Ingredient._meta.get_fields())  # noqa: SLF001
                and src in nutrition
            ):
                ing_defaults[fld] = nutrition[src]

        try:
            ing, created_flag = Ingredient.objects.get_or_create(
                name=name, defaults=ing_defaults
            )

            if not created_flag:
                changed = False
                for k, v in ing_defaults.items():
                    if getattr(ing, k, None) in (None, "", 0) and v not in (
                        None,
                        "",
                        0,
                    ):
                        setattr(ing, k, v)
                        changed = True
                if changed:
                    ing.save()
            else:
                created += 1
        except Exception:  # noqa: BLE001
            skipped += 1

    return created, skipped


def seed_recipes_with_json(items: list[dict[str, Any]]) -> tuple[int, int]:  # noqa: C901, PLR0912
    """
    Persist recipes.
    """

    created = 0
    skipped = 0

    ing_by_name = {i.name.lower(): i for i in Ingredient.objects.all()}

    for row in items:
        name = (row.get("name") or row.get("title") or "").strip()
        if not name:
            skipped += 1
            continue

        description = (row.get("description") or "").strip() or f"{name} recipe."
        instructions_list = row.get("instructions") or []
        instructions_text = "\n".join(
            step.strip() for step in instructions_list if step
        )

        defaults: dict[str, Any] = {}

        if any(f.name == "title" for f in Recipe._meta.get_fields()):  # noqa: SLF001
            defaults["title"] = name
            lookup_field = "title"
        else:
            lookup_field = "name"

        if any(f.name == "name" for f in Recipe._meta.get_fields()):  # noqa: SLF001
            defaults["name"] = name
        if any(f.name == "description" for f in Recipe._meta.get_fields()):  # noqa: SLF001
            defaults["description"] = description

        instr_field = _get_first_present_name(
            ("instructions", "directions", "steps_text"),
            {f.name for f in Recipe._meta.get_fields()},  # noqa: SLF001
        )

        if instr_field:
            defaults[instr_field] = instructions_text

        if isinstance(row.get("servings"), int) and any(
            f.name == "servings"
            for f in Recipe._meta.get_fields()  # noqa: SLF001
        ):
            defaults["servings"] = row["servings"]

        category = _ensure_category(row.get("category_name"))
        if category and any(f.name == "category" for f in Recipe._meta.get_fields()):  # noqa: SLF001
            defaults["category"] = category

        try:
            with transaction.atomic():
                recipe, created_flag = Recipe.objects.get_or_create(
                    **{lookup_field: name}, defaults=defaults
                )
                if not created_flag:
                    # Optionally update missing optional fields on existing records
                    changed = False
                    for k, v in defaults.items():
                        if getattr(recipe, k, None) in (None, "", 0) and v not in (
                            None,
                            "",
                            0,
                        ):
                            setattr(recipe, k, v)
                            changed = True
                    if changed:
                        recipe.save()

                _link_ingredients_with_quantities(
                    recipe, row.get("ingredients") or [], ing_by_name
                )

                if created_flag:
                    created += 1
        except Exception:  # noqa: BLE001
            skipped += 1

    return created, skipped


def generate_and_seed_ingredients(
    count: int, locale: str, client: GeminiClient
) -> tuple[int, int]:
    """
    Call Gemini to generate ingredient JSON and persist it.
    """

    prompt = build_ingredient_prompt(count=count, locale=locale)
    data = client.generate_json(prompt)
    items = list(data.get("items") or [])
    return seed_ingredients_with_json(items)


def generate_and_seed_recipes(
    count: int, locale: str, client: GeminiClient
) -> tuple[int, int]:
    """
    Call Gemini to generate recipe JSON and persist it.
    """

    known = (ing.name for ing in Ingredient.objects.all())
    prompt = build_recipe_prompt(count=count, locale=locale, known_ingredients=known)
    data = client.generate_json(prompt)
    items = list(data.get("items") or [])
    return seed_recipes_with_json(items)
