"""
Register admin interface for `Category` model.
"""

from django.contrib.admin import register

from nutriplan.models import Category

from .mixins import ReadOnlyForStaffAdmin


@register(Category)
class CategoryAdmin(ReadOnlyForStaffAdmin):
    """
    Admin interface options for `Category` model.
    """

    list_display = ("name", "friendly_name", "description")
    search_fields = ("name",)
