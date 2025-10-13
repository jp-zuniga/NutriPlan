"""
Models for recipes, their ingredient relations, and images.
"""

from decimal import Decimal
from typing import ClassVar

from django.contrib.postgres.indexes import GinIndex
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    CheckConstraint,
    DateTimeField,
    DecimalField,
    F,
    ForeignKey,
    Index,
    IntegerField,
    ManyToManyField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    Q,
    SlugField,
    TextField,
    URLField,
    UniqueConstraint,
)
from django.db.models.fields.generated import GeneratedField
from django.db.models.functions import Coalesce, Lower
from django.utils.text import slugify

from .base_model import BaseModel
from .category import Category
from .ingredient import Ingredient

MINUTES = 60


class Recipe(BaseModel):
    """
    A cookable recipe with times, nutrition, category, ingredients and images.
    """

    slug = SlugField(max_length=120, unique=True, db_index=True)
    name = CharField(max_length=100)
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

    main_image_url = URLField(blank=True, help_text="Primary recipe image.")
    prep_time = PositiveIntegerField(
        verbose_name="Prep Time",
        help_text="Preparation time (in minutes)",
    )

    cook_time = PositiveIntegerField(
        verbose_name="Cook Time",
        help_text="Cooking time (in minutes)",
        default=0,
    )

    total_time = GeneratedField(
        expression=F("prep_time") + F("cook_time"),
        output_field=IntegerField(),
        db_persist=True,
        editable=False,
    )

    servings = PositiveSmallIntegerField(default=1)
    calories_per_serving = DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal(0),
        help_text="kcal per serving",
    )

    total_calories = GeneratedField(
        expression=Coalesce(F("calories_per_serving"), 0) * Coalesce(F("servings"), 0),
        output_field=DecimalField(max_digits=8, decimal_places=2),
        db_persist=True,
        editable=False,
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

    created_at = DateTimeField(auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        """
        Ensure non-negative values, unique case-insensitive slug, and indexing.
        """

        constraints: ClassVar[list[CheckConstraint | UniqueConstraint]] = [
            CheckConstraint(
                check=None,
                condition=Q(prep_time__gte=0),  # type: ignore[reportCallIssue]
                name="chk_rec_prep_ge_0",
            ),
            CheckConstraint(
                check=None,
                condition=Q(cook_time__gte=0),  # type: ignore[reportCallIssue]
                name="chk_rec_cook_ge_0",
            ),
            CheckConstraint(
                check=None,
                condition=Q(servings__gte=0),  # type: ignore[reportCallIssue]
                name="chk_rec_serv_ge_0",
            ),
            UniqueConstraint(Lower("slug"), name="uniq_recipe_slug_ci"),
        ]

        indexes: ClassVar[list[Index]] = [
            GinIndex(
                fields=["description"],
                name="idx_recipe_desc_trgm",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["name"], name="idx_recipe_name_trgm", opclasses=["gin_trgm_ops"]
            ),
            Index(fields=["category"]),
            Index(fields=["created_at"]),
            Index(fields=["slug"], name="idx_recipe_slug"),
            Index(fields=["total_time"]),
        ]

        ordering: tuple[str, str] = ("-created_at", "name")

    def __str__(self) -> str:
        """
        Return human-readable recipe name.
        """

        return self.name

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """
        Save current instance with auto-generated slug.
        """

        if not self.slug:
            self.slug = self._build_unique_slug()

        super().save(*args, **kwargs)

    def _build_unique_slug(self) -> str:
        base = slugify(self.name or "")
        slug = base or str(self.id)
        qs = type(self).objects.all()

        if self.pk:
            qs = qs.exclude(pk=self.pk)

        if not qs.filter(slug=slug).exists():
            return slug

        i = 2
        while True:
            candidate = f"{base}-{i}"
            if not qs.filter(slug=candidate).exists():
                return candidate

            i += 1

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


class RecipeIngredient(BaseModel):
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

    class Meta(BaseModel.Meta):
        """
        Enforce uniqueness of ingredient per recipe.
        """

        constraints: tuple[CheckConstraint, UniqueConstraint] = (
            CheckConstraint(
                check=None,
                condition=Q(amount__gt=0),  # type: ignore[reportCallIssue]
                name="chk_ri_amount_gt_0",
            ),
            UniqueConstraint(
                fields=["recipe", "ingredient"],
                name="unique_recipe_ingredient",
            ),
        )

        indexes: ClassVar[list[Index]] = [
            Index(fields=["ingredient"], name="idx_ri_ingredient"),
        ]

    def __str__(self) -> str:
        """
        Readable representation of the ingredient entry for a recipe.
        """

        return (
            f"{self.amount} {self.unit} {self.ingredient.name} for {self.recipe.name}"
        )


class RecipeImage(BaseModel):
    """
    Additional images for a recipe with display ordering.
    """

    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name="recipe_images")
    image = ForeignKey("Image", on_delete=CASCADE, related_name="uses")
    order = PositiveSmallIntegerField(default=0)

    class Meta(BaseModel.Meta):
        """
        Default ordering for deterministic image sequences.
        """

        constraints: tuple[UniqueConstraint] = (
            UniqueConstraint(fields=["recipe", "image"], name="unique_recipe_image"),
        )

        indexes: ClassVar[list[Index]] = [
            Index(fields=["recipe", "order", "id"], name="idx_recipeimage_rec_ord"),
        ]

        ordering: tuple[str, str] = ("order", "id")

    def __str__(self) -> str:
        """
        Human-friendly representation for admin lists.
        """

        return f"Image for {self.recipe.name} ({self.image.url})"


class Image(BaseModel):
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
