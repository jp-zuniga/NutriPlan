"""
Custom user and dietary restriction models.
"""

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, ManyToManyField, Model, TextField


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.

    Attributes:
        dietary_restrictions: user's health-related restrictions.

    """

    dietary_restrictions = ManyToManyField(
        "DietaryRestriction", blank=True, related_name="users"
    )

    def __str__(self) -> str:
        """
        Returns the email of the user.
        """

        return self.email


class DietaryRestriction(Model):
    """
    Represents a dietary restriction that can be associated with a user.
    """

    name = CharField(max_length=100, unique=True)
    description = TextField(blank=True)

    def __str__(self) -> str:
        """
        Returns dietary restriction's name.
        """

        return self.name
