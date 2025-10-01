"""
Serializer for the Category model.
"""

from rest_framework.serializers import ModelSerializer

from nutriplan.models import Category


class CategorySerializer(ModelSerializer):
    """
    Category serializer, which automatically includes all of its fields.
    """

    class Meta:
        """
        Class metadata.
        """

        model = Category
        fields = "__all__"
