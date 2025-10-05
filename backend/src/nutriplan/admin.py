"""
Register models with admin interface and customizes their admin options.
"""

from collections.abc import Mapping, Sequence
from typing import ClassVar

from django.contrib.admin import ModelAdmin, site
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from rest_framework.request import HttpRequest

from nutriplan.models import (
    Category,
    CollectionItem,
    CustomUser,
    DietaryRestriction,
    Ingredient,
    Recipe,
    RecipeCollection,
    RecipeIngredient,
)


class CustomAdmin(UserAdmin):
    """
    Admin interface options for the CustomUser model.
    """

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "phone_number",
                    "password",
                    "password_confirm",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal Info"), {"fields": ("first_name", "last_name", "phone_number")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
        (_("Dietary Restrictions"), {"fields": ("dietary_restrictions",)}),
    )

    model = CustomUser
    list_display: ClassVar[list[str]] = [  # type: ignore[reportAssignmentType]
        "email",
        "first_name",
        "last_name",
        "phone_number",
        "is_staff",
    ]

    ordering: tuple[str] = ("email",)  # type: ignore[reportIncompatibleVariableOverride]
    search_fields: ClassVar[Sequence[str]] = [  # type: ignore[reportIncompatibleVariableOverride]
        "email",
        "first_name",
        "last_name",
    ]

    def get_form(  # type: ignore[reportIncompatibleMethodOverride]
        self,
        request: HttpRequest,
        obj: object | None = None,
        **kwargs,  # noqa: ANN003
    ) -> type[ModelForm]:
        """
        Override the default `get_form` method to customize the admin form.

        Removes the `username` field from the form's `base_fields` if it exists,
        effectively hiding the `username` field from the admin interface for this model.

        Args:
            request:  Current HTTP request object.
            obj:      Object being edited, or None if adding a new object.
            change:   True if editing an existing object, False if adding a new one.
            **kwargs: Additional keyword arguments.

        Returns:
            type[ModelForm]: Modified class with "username" field removed if present.

        """

        form = super().get_form(request, obj, **kwargs)
        if "username" in form.base_fields:  # type: ignore[reportAttributeAccessIssue]
            form.base_fields.pop("username")  # type: ignore[reportAttributeAccessIssue]

        return form


class CategoryAdmin(ModelAdmin):
    """
    Admin interface options for the Category model.
    """

    list_display = ("name", "friendly_name", "description")
    readonly_fields = ("name",)


class CollectionItemAdmin(ModelAdmin):
    """
    Admin interface options for the CollectionItem model.
    """

    list_display = ("collection", "recipe", "order", "added_at")
    search_fields = ("collection__name", "recipe__name", "collection__owner__email")
    list_filter = ("collection__is_public",)
    autocomplete_fields = ("collection", "recipe")


class RecipeAdmin(ModelAdmin):
    """
    Admin interface options for the Recipe model.
    """

    prepopulated_fields: ClassVar[Mapping[str, Sequence[str]]] = {"slug": ("name",)}  # type: ignore[reportIncompatibleVariableOverride]
    list_display = ("name", "slug", "category", "created_at")
    search_fields = ("name", "slug")


class RecipeCollectionAdmin(ModelAdmin):
    """
    Admin interface options for the RecipeCollection model.
    """

    list_display = ("name", "owner", "is_public", "created_at")
    search_fields = ("name", "owner__email")
    list_filter = ("is_public",)
    readonly_fields = ("created_at", "updated_at")
    autocomplete_fields = ("owner",)


site.register(Category, CategoryAdmin)
site.register(CollectionItem, CollectionItemAdmin)
site.register(CustomUser, CustomAdmin)
site.register(DietaryRestriction)
site.register(Ingredient)
site.register(Recipe, RecipeAdmin)
site.register(RecipeIngredient)
site.register(RecipeCollection, RecipeCollectionAdmin)
