"""
Register admin interface for `Review` model.
"""

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import Review


@register(Review)
class ReviewAdmin(ModelAdmin):
    """
    Admin interface options for `Review` model.
    """

    list_display = ("recipe", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("recipe__name", "user__email", "comment")
