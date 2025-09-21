"""
Serializer for Recipe model, including nested ingredients and images.
"""

from __future__ import annotations

from typing import Any

from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    SerializerMethodField,
)

from nutriplan.models.recipe import Recipe, RecipeImage, RecipeIngredient
from nutriplan.serializers import CategorySerializer, IngredientSerializer


class RecipeSerializer(ModelSerializer):
    """
    Recipe serializer exposing ingredients and ordered images.
    """

    category = CategorySerializer(read_only=True)
    ingredients = SerializerMethodField()
    images = SerializerMethodField()
    total_time = IntegerField(read_only=True)
    primary_image = CharField(read_only=True)

    class Meta:
        """
        Serializer options and exposed fields.
        """

        model = Recipe
        fields = (
            "name",
            "description",
            "category",
            "prep_time",
            "cook_time",
            "total_time",
            "servings",
            "calories_per_serving",
            "protein_per_serving",
            "carbs_per_serving",
            "fat_per_serving",
            "sugar_per_serving",
            "primary_image",
            "images",
            "ingredients",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("created_at", "updated_at", "primary_image", "total_time")

    def get_ingredients(self, obj: Recipe) -> list[dict[str, Any]]:
        """
        Return ingredient entries with amount/unit and nested ingredient data.
        """

        qs = RecipeIngredient.objects.select_related("ingredient").filter(recipe=obj)
        return [
            {
                "ingredient": IngredientSerializer(ri.ingredient).data,
                "amount": ri.amount,
                "unit": ri.unit,
            }
            for ri in qs
        ]

    def get_images(self, obj: Recipe) -> list[dict[str, Any]]:
        """
        Return ordered image data from the through model.
        """

        qs = (
            RecipeImage.objects.select_related("image")
            .filter(recipe=obj)
            .order_by("order", "id")
        )

        return [
            {
                "url": ri.image.url,
                "alt_text": ri.image.alt_text,
                "order": ri.order,
            }
            for ri in qs
        ]
