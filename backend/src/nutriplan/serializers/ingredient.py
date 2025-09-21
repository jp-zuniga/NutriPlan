"""
Serializer for Ingredient model.
"""

from rest_framework.serializers import ModelSerializer

from nutriplan.models import Ingredient


class IngredientSerializer(ModelSerializer):
    """
    Ingredient serializer, which automatically includes all of its fields.
    """

    class Meta:
        """
        Class metadata.
        """

        model = Ingredient
        fields = "__all__"
