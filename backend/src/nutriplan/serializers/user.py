"""
Serializers for user registration and profile management.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import (
    CharField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    Serializer,
    ValidationError,
)

from nutriplan.models import DietaryRestriction
from nutriplan.services import UserService

CustomUser = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    """
    Serializer for user registration.
    """

    password = CharField(write_only=True, min_length=8)

    class Meta:
        """
        Class metadata.
        """

        model = CustomUser
        fields = ("email", "username", "password", "first_name", "last_name")

    def create(self, validated_data: dict) -> AbstractUser:
        """
        Creates a new user instance using the provided validated data.

        Args:
            validated_data: user information.

        Returns:
            AbstractUser: created user instance.

        """

        return UserService.create_user(validated_data)

    def validate_pw(self, value: str) -> str:
        """
        Validates the provided password using Django's built-in password validators.

        Args:
            value: string to validate.

        Returns:
            str: validated password string.

        """

        validate_password(value)
        return value


class UserProfileSerializer(ModelSerializer):
    """
    Serializer for existing users' profile data.

    Used by the UserViewSet for retrieve/update and the /users/me endpoint.
    """

    dietary_restrictions = PrimaryKeyRelatedField(
        many=True, queryset=DietaryRestriction.objects.all(), required=False
    )

    class Meta:
        """
        Class metadata.
        """

        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "dietary_restrictions",
        )
        read_only_fields = ("id", "username", "email")


class ChangePasswordSerializer(Serializer):
    """
    Serializer for changing the current user's password via /users/me/change-password.

    Enforces current password and runs Django's password validators.
    """

    current_password = CharField(write_only=True)
    new_password = CharField(write_only=True, min_length=8)

    def validate_current_pw(self, value: str) -> str:
        """
        Validates that the provided password matches the current user's password.

        Args:
            value: password to validate.

        Returns:
            str: validated password if it matches.

        Raises:
            ValidationError: if provided password doesn't match.

        """
        user = self.context["request"].user
        if not user.check_password(value):
            msg = "Invalid current password."
            raise ValidationError(msg)

        return value

    def validate_new_pw(self, value: str) -> str:
        """
        Validates the new password provided by the user.

        This method uses Django's `validate_password` function to ensure
        that the new password meets the required security standards.

        Args:
            value: new password to be validated.

        Returns:
            str: validated password.

        Raises:
            ValidationError: If password doesn't meet the validation criteria.

        """

        validate_password(value, self.context["request"].user)
        return value
