from django.contrib import admin

from .models import Category, Recipe


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "friendly_name", "description")
    readonly_fields = ("name",)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Recipe)
