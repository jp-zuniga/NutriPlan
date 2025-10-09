"""
Register admin interface for `DietaryRestriction` model.
"""

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import DietaryRestriction


@register(DietaryRestriction)
class DietaryRestrictionAdmin(ModelAdmin):
    """
    Admin interface options for `DietaryRestriction` model.
    """

    list_display = ("name", "description")
    search_fields = ("name",)
