"""
Register admin interface for `DietaryRestriction` model.
"""

from django.contrib.admin import register

from nutriplan.models import DietaryRestriction

from .mixins import ReadOnlyForStaffAdmin


@register(DietaryRestriction)
class DietaryRestrictionAdmin(ReadOnlyForStaffAdmin):
    """
    Admin interface options for `DietaryRestriction` model.
    """

    list_display = ("name", "description")
    search_fields = ("name",)
