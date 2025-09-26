"""
Seed DB with AI-generated ingredients and recipes using Gemini (Google GenAI SDK).
"""

from __future__ import annotations

from json import dumps

from django.core.management.base import BaseCommand, CommandParser

from nutriplan.models import Ingredient
from nutriplan.services.llm.gemini import GeminiClient
from nutriplan.services.llm.seeders import (
    build_ingredient_prompt,
    build_recipe_prompt,
    generate_and_seed_ingredients,
    generate_and_seed_recipes,
)


class Command(BaseCommand):
    """
    Command to generate and persist AI-seeded ingredients and recipes using Gemini.
    """

    help = "Generate and persist AI-seeded ingredients/recipes."

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Adds command-line arguments to the management command parser.

        Args:
            parser: argument parser to which the command-line arguments are added.

        Supported arguments:
        --------------------
            --ingredients (int): Number of ingredients to populate (default: 0).
            --recipes (int): Number of recipes to populate (default: 0).
            --locale (str): Locale to use for data generation (default: "en-US").
            --dry-run (store_true): If set, performs a dry run without making changes.
            --verbose (store_true): If set, enables verbose output.

        """

        parser.add_argument("--ingredients", type=int, default=0)
        parser.add_argument("--recipes", type=int, default=0)
        parser.add_argument("--locale", type=str, default="en-US")
        parser.add_argument("--dry-run", action="store_true")
        parser.add_argument("--verbose", action="store_true")

    def handle(self, *args: list, **opts: dict) -> None:  # noqa: ARG002
        """
        Handles the population of ingredients and recipes in the database.

        This command supports generating and seeding ingredient and recipe data,
        either by performing a dry run (outputting the generated data as JSON),
        or by saving the data to the database.

        The number of ingredients and recipes to generate, the locale,
        and verbosity can be controlled via command-line options.

        Args:
            args: Additional positional arguments (unused).
            opts: Command-line options, including:
                - "ingredients" (int): Number of ingredients to generate.
                - "recipes" (int): Number of recipes to generate.
                - "locale" (str): Locale to use for data generation.
                - "dry_run" (bool): If True, output generated data without saving.
                - "verbose" (bool): If True, print detailed output.

        Returns:
            None

        """

        ing_n = int(opts.get("ingredients", 0))  # type: ignore[reportArgumentType]
        rec_n = int(opts.get("recipes", 0))  # type: ignore[reportArgumentType]
        locale = opts.get("locale", "en-US")
        dry = bool(opts.get("dry_run", False))
        verbose = bool(opts.get("verbose", False))

        if not ing_n and not rec_n:
            self.stdout.write(
                self.style.WARNING("Nothing to do. Use --ingredients and/or --recipes.")
            )
            return

        client = GeminiClient()

        if ing_n:
            if dry:
                data = client.generate_json(build_ingredient_prompt(ing_n, locale))  # type: ignore[reportArgumentType]
                self.stdout.write(
                    dumps({"ingredients": data.get("items", [])}, indent=2)
                )
            else:
                created, skipped = generate_and_seed_ingredients(ing_n, locale, client)  # type: ignore[reportArgumentType]
                if verbose:
                    self.stdout.write(
                        f"Ingredients created: {created}, skipped: {skipped}"
                    )

        if rec_n:
            if dry:
                known = (i.name for i in Ingredient.objects.all())
                data = client.generate_json(build_recipe_prompt(rec_n, locale, known))  # type: ignore[reportArgumentType]
                self.stdout.write(dumps({"recipes": data.get("items", [])}, indent=2))
            else:
                created, skipped = generate_and_seed_recipes(rec_n, locale, client)  # type: ignore[reportArgumentType]
                if verbose:
                    self.stdout.write(f"Recipes created: {created}, skipped: {skipped}")
