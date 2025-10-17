"""
Serializers for recipe reviews/ratings.
"""

from typing import Any
from uuid import UUID

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, UUIDField, ValidationError

from nutriplan.models import Recipe, Review

from .user import UserPublicSerializer

User = get_user_model()

MIN_STARS = 1
MAX_STARS = 5


class ReviewSerializer(ModelSerializer):
    """
    Review serializer, capable of validating rating and corresponding recipe IDs.
    """

    recipe_id = UUIDField(write_only=True, required=True)

    class Meta:
        """
        Define fields and read-only fields.
        """

        model = Review
        fields = (
            "id",
            "recipe_id",
            "recipe",
            "user",
            "rating",
            "comment",
            "created_at",
            "updated_at",
        )

        read_only_fields = ("id", "recipe", "user", "created_at", "updated_at")

    def validate_rating(self, value: int) -> int:
        """
        Validates that the provided rating value is within the allowed range.

        Args:
            value: Rating to validate.

        Returns:
            int: Validated rating value.

        Raises:
            ValidationError: If rating is not between `MIN_STARS` and `MAX_STARS`.

        """

        if value < MIN_STARS or value > MAX_STARS:
            msg = "La calificación debe ser entre 1 y 5."
            raise ValidationError(msg)

        return value

    def validate_recipe_id(self, value: UUID) -> UUID:
        """
        Validate that the provided recipe ID corresponds to an existing Recipe.

        Args:
            value: Candidate primary key to validate.

        Returns:
            Any: Original value the Recipe exists.

        Raises:
            ValidationError: If a Recipe with the given primary key does not exist.

        """

        if not Recipe.objects.filter(pk=value).exists():
            msg = "Receta no encontrada."
            raise ValidationError(msg)

        return value

    def create(self, validated_data: dict[str, Any]) -> Review:
        """
        Create new Review instance for a given recipe and user.

        Args:
            validated_data: Validated review fields.

        Returns:
            Review: Newly created Review instance.

        Raises:
            ValidationError:     If user has already reviewed the specified recipe.
            Recipe.DoesNotExist: If recipe with the given `recipe_id` does not exist.

        Notes:
            - User is retrieved from the serializer context.
            - Ensures that a user cannot review the same recipe more than once.

        """

        user = self.context["request"].user
        recipe_id = validated_data.pop("recipe_id")
        recipe = Recipe.objects.get(pk=recipe_id)

        if Review.objects.filter(user=user, recipe=recipe).exists():
            raise ValidationError({"non_field_errors": ["Ya calificaste esta receta."]})

        return Review.objects.create(user=user, recipe=recipe, **validated_data)

    def update(self, instance: Review, validated_data: dict[str, Any]) -> Review:
        """
        Update existing Review instance with provided validated data.

        Args:
            instance:       Review instance to update.
            validated_data: Data to update the instance with.

        Returns:
            Review: Updated Review instance.

        """

        validated_data.pop("recipe_id", None)
        return super().update(instance, validated_data)


class ReviewReadSerializer(ModelSerializer):
    """
    Read-friendly shape (includes nested ids/emails minimal).
    """

    user = UserPublicSerializer(read_only=True)

    class Meta:
        """
        Ensure all fields are read-only.
        """

        model = Review
        fields = (
            "id",
            "user",
            "rating",
            "comment",
            "created_at",
        )

        read_only_fields = fields
