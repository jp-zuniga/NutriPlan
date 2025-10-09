"""
Model for social authentication.
"""

from __future__ import annotations

from typing import ClassVar

from django.conf import settings
from django.db.models import (
    CASCADE,
    BaseConstraint,
    CharField,
    CheckConstraint,
    DateTimeField,
    EmailField,
    ForeignKey,
    Index,
    Q,
    TextChoices,
    URLField,
    UniqueConstraint,
)

from .base_model import BaseModel


class Provider(TextChoices):
    """
    Enums for social authentication providers.
    """

    GOOGLE = ("google", "Google")


class SocialAccount(BaseModel):
    """
    Account linked to a social authentication provider (e.g., Google).
    """

    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="social_accounts",
    )

    provider = CharField(max_length=32, choices=Provider.choices)
    provider_user_id = CharField(max_length=128)
    email = EmailField(blank=True)
    display_name = CharField(max_length=150, blank=True)
    avatar_url = URLField(blank=True)
    created_at = DateTimeField(auto_now_add=True)
    last_login_at = DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        """
        Ensure unique provider/user.id pairs and valid provider values.
        """

        constraints: ClassVar[list[BaseConstraint]] = [
            UniqueConstraint(
                fields=["provider", "provider_user_id"],
                name="uniq_provider_uid",
            ),
            CheckConstraint(
                check=Q(provider__in=[c for c, _ in Provider.choices]),
                name="chk_valid_provider",
            ),
        ]

        indexes: ClassVar[list[Index]] = [
            Index(fields=["provider", "provider_user_id"], name="idx_provider_uid"),
            Index(fields=["user"], name="idx_social_user"),
        ]

    def __str__(self) -> str:
        """
        Return string representation of self with provider and IDs.
        """

        return f"{self.provider}:{self.provider_user_id} → {self.user.id}"
