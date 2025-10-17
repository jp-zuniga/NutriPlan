"""
Custom user and dietary restriction models.
"""

from __future__ import annotations

from typing import ClassVar

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import (
    CharField,
    EmailField,
    Index,
    ManyToManyField,
    TextField,
    UniqueConstraint,
)
from django.db.models.functions import Lower

from .base_model import BaseModel


class CustomUserManager(UserManager):
    """
    Custom manager for the CustomUser model.

    Provides methods to create regular users and superusers
    using `email` as the unique identifier instead of `username`.
    """

    use_in_migrations = True

    def _create_user(
        self,
        email: str,
        password: str | None,
        **extra_fields,  # noqa: ANN003
    ) -> CustomUser:
        """
        Creates and saves a user with the given email and password.

        Args:
            email:          User's email address. Must be provided.
            password:       User's password. If `None`, password will be unusable.
            **extra_fields: Additional fields to set on the user model.

        Returns:
            User: Created user instance.

        Raises:
            ValueError: If `email` is not provided.

        """

        if not email:
            msg = "Email must be set"
            raise ValueError(msg)

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_user(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        email: str,
        password: str | None = None,
        **extra_fields,  # noqa: ANN003
    ) -> CustomUser:
        """
        Creates and saves a regular user with the given email and password.

        Args:
            email:          User's email address.
            password:       User's password. Defaults to `None`.
            **extra_fields: Additional fields to set on the user object.

        Returns:
            CustomUser: Newly created user instance.

        Notes:
        -----
            - User will have `is_staff` and `is_superuser` set to `False` by default.

        """

        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        email: str,
        password: str | None = None,
        **extra_fields,  # noqa: ANN003
    ) -> CustomUser:
        """
        Creates and returns a superuser with the given email and password.

        This method sets the `is_staff` and `is_superuser` fields to `True` by default.
        If these fields are not explicitly set to `True` in `extra_fields`,
        a `ValueError` is raised.

        Args:
            email:          Email address for superuser.
            password:       Password for superuser. Defaults to `None`.
            **extra_fields: Additional fields to set on the user.

        Returns:
            CustomUser: Created superuser instance.

        Raises:
            ValueError: If `is_staff` or `is_superuser` are not set to `True`.

        """

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            msg = "Superuser must have is_staff=True."
            raise ValueError(msg)
        if extra_fields.get("is_superuser") is not True:
            msg = "Superuser must have is_superuser=True."
            raise ValueError(msg)

        return self._create_user(email, password, **extra_fields)


class CustomUser(BaseModel, AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Attributes:
        dietary_restrictions: User's health-related restrictions.
        phone_number:         User's contact number.

    """

    email = EmailField(db_index=True, unique=True)
    dietary_restrictions = ManyToManyField(
        "DietaryRestriction", blank=True, related_name="users"
    )

    phone_number = CharField(max_length=20, blank=True)
    objects = CustomUserManager()
    username = None

    REQUIRED_FIELDS: ClassVar[list[str]] = []  # type: ignore[incompatibleVariableOverride]
    USERNAME_FIELD = "email"

    class Meta(BaseModel.Meta):
        """
        Ensure case-insensitive uniqueness and indexing on `email`.
        """

        constraints: ClassVar[list[UniqueConstraint]] = [
            UniqueConstraint(Lower("email"), name="uniq_user_email_ci"),
        ]

        indexes: ClassVar[list[Index]] = [
            Index(Lower("email"), name="idx_user_email_lower"),
        ]

    def __str__(self) -> str:
        """
        Return username.
        """

        return self.email

    @property
    def role(self) -> str:
        """
        Get Django credentials for user.
        """

        if getattr(self, "is_superuser", False):
            return "admin"
        if getattr(self, "is_staff", False):
            return "staff"
        return "user"


class DietaryRestriction(BaseModel):
    """
    Represents a dietary restriction that can be associated with a user.
    """

    name = CharField(max_length=100, unique=True)
    description = TextField(blank=True)

    def __str__(self) -> str:
        """
        Return dietary restriction's name.
        """

        return self.name
