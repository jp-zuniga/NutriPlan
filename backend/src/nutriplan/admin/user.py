"""
Register admin interface for `CustomUser` model.
"""

from collections.abc import Sequence
from typing import ClassVar

from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.forms import ModelForm
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _

from nutriplan.models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface options for `CustomUser` model.
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

    ordering: tuple[str, ...] = ("email",)  # type: ignore[reportIncompatibleVariableOverride]
    search_fields: ClassVar[Sequence[str]] = ["email", "first_name", "last_name"]  # type: ignore[reportIncompatibleVariableOverride]

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
