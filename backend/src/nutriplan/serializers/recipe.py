from rest_framework import serializers

from nutriplan.models import Recipe
from nutriplan.serializers.category import CategorySerializer
from nutriplan.serializers.ingredient import IngredientSerializer


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"
