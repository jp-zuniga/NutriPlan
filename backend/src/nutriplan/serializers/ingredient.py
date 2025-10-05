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
        Ensure all fields of the `Ingredient` model are included.
        """

        model = Ingredient
        fields = "__all__"
