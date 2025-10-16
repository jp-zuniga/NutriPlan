"""
Admin registration for chat models.
"""

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import ChatMessage, ChatThread


@register(ChatThread)
class ChatThreadAdmin(ModelAdmin):
    autocomplete_fields = ("owner",)
    list_display = (
        "id",
        "owner",
        "title",
        "is_archived",
        "last_message_at",
        "updated_at",
    )

    list_filter = ("is_archived",)
    ordering = ("-updated_at",)
    search_fields = ("title", "owner__email")


@register(ChatMessage)
class ChatMessageAdmin(ModelAdmin):
    autocomplete_fields = ("thread",)
    list_display = ("id", "thread", "role", "created_at")
    list_filter = ("role",)
    ordering = ("-created_at",)
    search_fields = ("thread__title", "content")
