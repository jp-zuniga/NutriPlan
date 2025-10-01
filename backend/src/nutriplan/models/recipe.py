"""
Models for recipes, their ingredient relations, and images.
"""

from decimal import Decimal

from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    TextField,
    URLField,
    UniqueConstraint,
)
from django.utils import timezone

from .category import Category
from .ingredient import Ingredient

MINUTES = 60


class Recipe(Model):
    """
    A cookable recipe with times, nutrition, category, ingredients and images.
    """

    name = CharField(max_length=100, primary_key=True)
    description = TextField(help_text="Short description shown prominently.")
    category = ForeignKey(
        Category,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
    )

    ingredients = ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
        related_name="recipes",
    )

    images = ManyToManyField(
        "Image",
        through="RecipeImage",
        related_name="recipes",
        blank=True,
    )

    main_image_url = URLField(blank=True, help_text="Primary image URL")
    prep_time = PositiveIntegerField(
        verbose_name="Prep Time",
        help_text="Preparation time (in minutes)",
    )

    cook_time = PositiveIntegerField(
        verbose_name="Cook Time",
        help_text="Cooking time (in minutes)",
        default=0,
    )

    servings = PositiveSmallIntegerField(default=1)
    calories_per_serving = DecimalField(
        max_digits=7,
        decimal_places=2,
        default=Decimal(0),
        help_text="kcal per serving",
    )

    protein_per_serving = DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal(0),
        help_text="grams protein per serving",
    )

    carbs_per_serving = DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal(0),
        help_text="grams carbs per serving",
    )

    fat_per_serving = DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal(0),
        help_text="grams fat per serving",
    )

    sugar_per_serving = DecimalField(
        max_digits=6,
        decimal_places=2,
        default=Decimal(0),
        help_text="grams sugar per serving",
    )

    created_at = DateTimeField(default=timezone.now)
    updated_at = DateTimeField(default=timezone.now)

    class Meta:
        """
        Meta options for default ordering.
        """

        ordering = ("-created_at", "name")

    def __str__(self) -> str:
        """
        Return human-readable recipe name.
        """

        return self.name

    @property
    def total_time(self) -> int:
        """
        Total time in minutes (prep + cook).
        """

        return self.prep_time + self.cook_time

    def format_time(self, minutes: int) -> str:
        """
        Format a minutes value as a human-readable string.
        """

        if minutes < MINUTES:
            return f"{minutes} min"

        hours = minutes // MINUTES
        mins = minutes % MINUTES

        if mins == 0:
            return f"{hours} hr"
        return f"{hours} hr {mins} min"

    @property
    def total_calories(self) -> Decimal:
        """
        Total kcal for the full recipe (per-serving kcal * servings).
        """

        return (self.calories_per_serving or Decimal(0)) * max(self.servings or 0, 0)

    @property
    def primary_image(self) -> str:
        """
        Return the best image URL to display for this recipe.
        """

        if self.main_image_url:
            return self.main_image_url
        ri = (
            self.images.through.objects.filter(recipe=self)
            .select_related("image")
            .order_by("order", "id")
            .first()
        )
        return ri.image.url if ri and ri.image else ""


class RecipeIngredient(Model):
    """
    Through model linking recipes and ingredients with amounts and units.
    """

    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name="recipe_ingredients",
    )

    ingredient = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name="ingredient_recipes",
    )

    amount = DecimalField(max_digits=6, decimal_places=2)
    unit = CharField(max_length=20, blank=True)

    class Meta:
        """
        Enforce uniqueness of ingredient per recipe.
        """

        constraints = (
            UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            ),
        )

    def __str__(self) -> str:
        """
        Readable representation of the ingredient entry for a recipe.
        """

        return (
            f"{self.amount} {self.unit} {self.ingredient.name} for {self.recipe.name}"
        )


class RecipeImage(Model):
    """
    Additional images for a recipe with display ordering.
    """

    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name="recipe_images")

    image = ForeignKey("Image", on_delete=CASCADE, related_name="uses")
    order = PositiveSmallIntegerField(default=0)

    class Meta:
        """
        Default ordering for deterministic image sequences.
        """

        ordering = ("order", "id")
        constraints = (
            UniqueConstraint(fields=["recipe", "image"], name="unique_recipe_image"),
        )

    def __str__(self) -> str:
        """
        Human-friendly representation for admin lists.
        """

        return f"Image for {self.recipe.name} ({self.image.url})"


class Image(Model):
    """
    Reusable image entity backed by a URL and optional alt text.
    """

    url = URLField(unique=True)
    alt_text = CharField(max_length=150, blank=True)
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """
        Return the image URL for display in admin lists.
        """

        return self.url
