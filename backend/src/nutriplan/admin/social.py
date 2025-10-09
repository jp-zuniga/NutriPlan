"""
Register admin interfaces for `SocialAccount` model.
"""

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import SocialAccount


@register(SocialAccount)
class SocialAccountAdmin(ModelAdmin):
    """
    Admin interface options for `SocialAccount` model.
    """

    autocomplete_fields = ("user",)
    list_display = (
        "provider",
        "provider_user_id",
        "user",
        "email",
        "display_name",
        "last_login_at",
        "created_at",
    )

    list_filter = ("provider",)
    ordering = ("-last_login_at", "provider", "user")
    readonly_fields = ("created_at", "last_login_at")
    search_fields = (
        "provider_user_id",
        "email",
        "display_name",
        "user__email",
        "user__first_name",
        "user__last_name",
    )
