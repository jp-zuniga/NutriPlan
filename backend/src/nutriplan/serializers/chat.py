"""
Serializers for chat threads and messages.
"""

from __future__ import annotations

from typing import Any

from rest_framework.serializers import (
    BooleanField,
    CharField,
    JSONField,
    ModelSerializer,
    Serializer,
    UUIDField,
    ValidationError,
)

from nutriplan.models import ChatMessage, ChatThread


class ChatThreadSerializer(ModelSerializer):
    """
    Read/Write serializer for ChatThread.

    Owner is inferred from request.user on create.
    """

    is_archived = BooleanField(required=False)

    class Meta:
        model = ChatThread
        fields = (
            "id",
            "title",
            "is_archived",
            "created_at",
            "updated_at",
            "last_message_at",
        )

        read_only_fields = ("id", "created_at", "updated_at", "last_message_at")

    def create(self, validated_data: dict[str, Any]) -> ChatThread:
        user = self.context["request"].user
        return ChatThread.objects.create(owner=user, **validated_data)


class ChatMessageSerializer(ModelSerializer):
    """
    Read-only shape for messages.
    """

    class Meta:
        model = ChatMessage
        fields = ("id", "thread", "role", "content", "meta", "created_at")
        read_only_fields = fields


class SendMessageSerializer(Serializer):
    """
    Payload to continue a conversation.
    """

    message = CharField()
    history = JSONField(required=False)
    title_if_empty = CharField(required=False, allow_blank=True, max_length=120)
    thread_id = UUIDField(required=True)

    def validate_message(self, value: str) -> str:
        if not value or not value.strip():
            msg = "message requerido."
            raise ValidationError(msg)

        return value.strip()
