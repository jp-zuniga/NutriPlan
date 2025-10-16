"""
Register admin interface for `Category` model.
"""

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import Category


@register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Admin interface options for `Category` model.
    """

    list_display = ("name", "friendly_name", "description")
    search_fields = ("name",)
