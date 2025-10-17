"""
Serializers for user registration and profile management.
"""

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.password_validation import validate_password
from rest_framework.fields import DjangoValidationError, EmailField
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

    full_name = CharField(write_only=True)
    email = EmailField()
    phone_number = CharField(required=False, allow_blank=True)
    password = CharField(write_only=True, min_length=8)
    password_confirm = CharField(write_only=True, min_length=8)
    dietary_restrictions = PrimaryKeyRelatedField(
        many=True, queryset=DietaryRestriction.objects.all(), required=False
    )

    role = CharField(read_only=True, source="role")

    class Meta:
        """
        Ensure required fields for registration.
        """

        model = CustomUser
        fields = (
            "full_name",
            "email",
            "phone_number",
            "password",
            "password_confirm",
            "dietary_restrictions",
            "role",
        )

        read_only_fields = ("id", "email", "role")

    def create(self, validated_data: dict) -> AbstractUser:
        """
        Creates a new user instance using the provided validated data.

        Args:
            validated_data: User information.

        Returns:
            AbstractUser: Created user instance.

        """

        full_name = validated_data.pop("full_name", "").strip()
        first_name, last_name = "", ""
        if full_name:
            parts = full_name.split()
            first_name = parts[0]
            last_name = " ".join(parts[1:]) if len(parts) > 1 else ""

        email = validated_data.get("email", "").strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError({"email": "Este correo ya está registrado."})

        phone_number = validated_data.get("phone_number", "").strip()

        password = validated_data.pop("password")
        validated_data.pop("password_confirm", None)

        return UserService.create_user(
            {
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "phone_number": phone_number,
            }
        )

    def validate(self, attrs: dict) -> dict:
        """
        Validates registration data.

        Args:
            attrs: User's registration attributes.

        Returns:
            dict: Validated user attributes.

        """

        if attrs.get("password") != attrs.get("password_confirm"):
            raise ValidationError({"password_confirm": "Las contraseñas no coinciden."})

        try:
            validate_password(
                password=attrs["password"],
                user=CustomUser(email=attrs.get("email", "")),
            )
        except DjangoValidationError as e:
            # <- AQUÍ el cambio clave: mandarlo como error de "password"
            raise ValidationError({"password": list(e.messages)}) from e

        return attrs


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
        Ensure profile fields are read-only where appropriate.
        """

        model = CustomUser
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "dietary_restrictions",
        )

        read_only_fields = ("id", "email")


class ChangePasswordSerializer(Serializer):
    """
    Serializer for changing the current user's password via /users/me/change-password.

    Enforces current password and runs Django's password validators.
    """

    current_password = CharField(write_only=True)
    new_password = CharField(write_only=True, min_length=8)

    def validate_current_password(self, value: str) -> str:
        """
        Validates that the provided password matches the current user's password.

        Args:
            value: Password to validate.

        Returns:
            str: Validated password if it matches.

        Raises:
            ValidationError: If provided password doesn't match.

        """

        user = self.context["request"].user
        if not user.check_password(value):
            msg = "Contraseña actual inválida."
            raise ValidationError(msg)

        return value

    def validate_new_password(self, value: str) -> str:
        """
        Validates the new password provided by the user.

        This method uses Django's `validate_password` function to ensure
        that the new password meets the required security standards.

        Args:
            value: New password to be validated.

        Returns:
            str: Validated password.

        Raises:
            ValidationError: If password doesn't meet the validation criteria.

        """

        try:
            validate_password(value, self.context["request"].user)
        except DjangoValidationError as e:
            raise ValidationError(list(e.messages)) from e
        return value
