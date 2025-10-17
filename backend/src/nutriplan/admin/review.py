"""
Register admin interface for `Review` model.
"""

from django.contrib.admin import register

from nutriplan.models import Review

from .mixins import ReadOnlyForStaffAdmin


@register(Review)
class ReviewAdmin(ReadOnlyForStaffAdmin):
    """
    Admin interface options for `Review` model.
    """

    list_display = ("recipe", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("recipe__name", "user__email", "comment")
