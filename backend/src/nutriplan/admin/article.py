from django.contrib.admin import register

from nutriplan.models import Article, ArticleRecipe

from .mixins import EditorsAdmin


@register(Article)
class ArticleAdmin(EditorsAdmin):
    autocomplete_fields = ("author",)
    list_display = ("title", "slug", "author", "created_at", "updated_at")
    list_filter = ("author",)
    search_fields = ("title", "slug", "text", "author__email")
    readonly_fields = ("created_at", "updated_at")


@register(ArticleRecipe)
class ArticleRecipeRefAdmin(EditorsAdmin):
    autocomplete_fields = ("article", "recipe")
    list_display = ("article", "recipe", "match_text", "first_index")
    search_fields = ("article__title", "recipe__name", "match_text")
