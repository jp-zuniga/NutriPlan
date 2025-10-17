"""
Serializers for Article and related references.
"""

from __future__ import annotations

from typing import Any

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)

from nutriplan.models import Article, Recipe
from nutriplan.services import sync_article_recipe_refs

from .user import UserPublicSerializer


class ArticleRecipeMiniSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ("id", "slug", "name", "primary_image")


class ArticleSerializer(ModelSerializer):
    """
    Staff write, everyone reads.

    Author inferred from request.user on create.
    Recipe references auto-synced from text.
    """

    author = UserPublicSerializer(read_only=True)
    recipes = SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            "id",
            "slug",
            "title",
            "text",
            "author",
            "recipes",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "slug",
            "author",
            "recipes",
            "created_at",
            "updated_at",
        )

    def get_recipes(self, obj: Article) -> list[dict[str, Any]]:
        qs = obj.recipes.all().only("id", "slug", "name")
        return ArticleRecipeMiniSerializer(qs, many=True).data  # type: ignore[return-value]

    def create(self, validated_data: dict) -> Article:
        user = self.context["request"].user
        if not (user and user.is_authenticated and user.is_staff):
            raise ValidationError({"detail": "Solo staff puede crear artículos."})

        art = Article.objects.create(author=user, **validated_data)
        sync_article_recipe_refs(art, art.text)
        return art

    def update(self, instance: Article, validated_data: dict) -> Article:
        # staff edit; RBAC se valida en la view
        for k, v in validated_data.items():
            setattr(instance, k, v)

        instance.save()
        sync_article_recipe_refs(instance, instance.text)
        return instance
