"""
Register admin interfaces for collection-related models.
"""

from django.contrib.admin import ModelAdmin, register

from nutriplan.models import CollectionItem, RecipeCollection


@register(CollectionItem)
class CollectionItemAdmin(ModelAdmin):
    """
    Admin interface options for `CollectionItem` model.
    """

    autocomplete_fields = ("collection", "recipe")
    list_display = ("collection", "recipe", "order", "added_at")
    list_filter = ("collection__is_public",)
    search_fields = ("collection__name", "recipe__name", "collection__owner__email")


@register(RecipeCollection)
class RecipeCollectionAdmin(ModelAdmin):
    """
    Admin interface options for `RecipeCollection` model.
    """

    autocomplete_fields = ("owner",)
    list_display = ("name", "owner", "is_public", "created_at")
    list_filter = ("is_public",)
    readonly_fields = ("created_at", "updated_at")
    search_fields = ("name", "owner__email")
