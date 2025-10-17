from django.contrib.admin import ModelAdmin


class ReadOnlyForStaffAdmin(ModelAdmin):
    def has_view_permission(self, request, obj=None) -> bool:
        if request.user.is_staff:
            return True
        return super().has_view_permission(request, obj)

    def has_add_permission(self, request) -> bool:
        return bool(request.user.is_superuser)

    def has_change_permission(self, request, obj=None) -> bool:
        return bool(request.user.is_superuser)

    def has_delete_permission(self, request, obj=None) -> bool:
        return bool(request.user.is_superuser)


class EditorsAdmin(ReadOnlyForStaffAdmin):
    def has_add_permission(self, request) -> bool:
        return bool(request.user.is_staff or request.user.is_superuser)

    def has_change_permission(self, request, obj=None) -> bool:
        return bool(request.user.is_staff or request.user.is_superuser)
