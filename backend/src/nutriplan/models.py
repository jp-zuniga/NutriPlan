from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["friendly_name"]

    def __str__(self) -> str:
        return self.friendly_name or self.name


class Recipe(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=300, unique=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recipes",
    )

    ingredients = models.ManyToManyField(
        Ingredient,
        through="RecipeIngredient",
    )

    prep_time = models.PositiveIntegerField(
        verbose_name="Prep Time", help_text="Preparation time (in minutes)"
    )

    cook_time = models.PositiveIntegerField(
        verbose_name="Cook Time", help_text="Cooking time (in minutes)", default=0
    )

    def __str__(self) -> str:
        return self.name

    @property
    def total_time(self) -> int:
        return self.prep_time + self.cook_time

    def format_time(self, minutes: int) -> str:
        if minutes < 60:
            return f"{minutes} min"

        hours = minutes // 60
        mins = minutes % 60

        if mins == 0:
            return f"{hours} hr"
        return f"{hours} hr {mins} min"


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    unit = models.CharField(max_length=20, blank=True)

    class Meta:
        unique_together = ["recipe", "ingredient"]

    def __str__(self) -> str:
        return (
            f"{self.amount} {self.unit} {self.ingredient.name} for {self.recipe.name}"
        )
