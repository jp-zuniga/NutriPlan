"""
Serializers for user registration and profile management.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from rest_framework.serializers import CharField, ModelSerializer

from nutriplan.services import UserService

CustomUser = get_user_model()


class UserRegistrationSerializer(ModelSerializer):
    """
    Serializer for user registration.
    """

    password = CharField(write_only=True)

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
            AbstractUser: The created user instance.

        """

        return UserService.create_user(validated_data)


class UserProfileSerializer(ModelSerializer):
    """
    Serializer for existing users' profile data.
    """

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
