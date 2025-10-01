"""
Register models with admin interface and customizes their admin options.
"""

from typing import ClassVar

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from nutriplan.models import (
    Category,
    CustomUser,
    DietaryRestriction,
    Ingredient,
    Recipe,
    RecipeIngredient,
)


class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface options for the Category model.
    """

    list_display = ("name", "friendly_name", "description")
    readonly_fields = ("name",)


class CustomUserAdmin(UserAdmin):
    """
    Admin interface options for the CustomUser model.
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (_("Dietary Restrictions"), {"fields": ("dietary_restrictions",)}),
    )

    list_display: ClassVar[list[str]] = ["username", "email", "first_name", "last_name"]  # type: ignore[reportAssignmentType]
    model = CustomUser


admin.site.register(Category, CategoryAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(DietaryRestriction)
admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
