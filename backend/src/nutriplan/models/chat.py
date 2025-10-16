"""
Chat history models for Chefcito.
"""

from __future__ import annotations

from typing import ClassVar

from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    JSONField,
    TextChoices,
    TextField,
)
from django.utils import timezone

from .base_model import BaseModel
from .user import CustomUser


class ChatThread(BaseModel):
    owner = ForeignKey(
        CustomUser,
        on_delete=CASCADE,
        related_name="chat_threads",
    )

    title = CharField(max_length=120, blank=True)
    is_archived = BooleanField(default=False)

    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)
    last_message_at = DateTimeField(default=timezone.now, db_index=True)

    class Meta(BaseModel.Meta):
        indexes: ClassVar[list[Index]] = [
            Index(fields=["owner", "-updated_at"], name="idx_chatthread_owner_upd"),
            Index(fields=["owner", "is_archived"], name="idx_chatthread_owner_arch"),
        ]

        ordering: tuple[str, str] = ("-updated_at", "-last_message_at")

    def __str__(self) -> str:
        return self.title or f"Conversación {self.pk}"

    def touch(self) -> None:
        self.last_message_at = timezone.now()
        self.save(update_fields=["last_message_at", "updated_at"])


class ChatRole(TextChoices):
    USER = ("user", "user")
    ASSISTANT = ("assistant", "assistant")
    TOOL = ("tool", "tool")


class ChatMessage(BaseModel):
    thread = ForeignKey(
        ChatThread,
        on_delete=CASCADE,
        related_name="messages",
    )

    role = CharField(max_length=16, choices=ChatRole.choices)
    content = TextField(blank=True)
    meta = JSONField(default=dict, blank=True)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        indexes: ClassVar[list[Index]] = [
            Index(fields=["thread", "created_at"], name="idx_chatmsg_thread_created"),
            Index(fields=["role"], name="idx_chatmsg_role"),
        ]

        ordering = ("created_at",)

    def __str__(self) -> str:
        return f"{self.role} @ {self.created_at:%Y-%m-%d %H:%M}"
