from __future__ import annotations

from typing import ClassVar

from django.conf import settings
from django.contrib.postgres.indexes import GinIndex
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    Index,
    ManyToManyField,
    SlugField,
    TextField,
    UniqueConstraint,
)
from django.db.models.functions import Lower
from django.utils.text import slugify

from .base_model import BaseModel
from .recipe import Recipe


class Article(BaseModel):
    """
    A staff-authored article with auto-linked recipe references.
    """

    slug = SlugField(max_length=160, unique=True, db_index=True)
    title = CharField(max_length=160)
    text = TextField()

    author = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        related_name="articles",
    )

    recipes = ManyToManyField(
        Recipe, through="ArticleRecipe", related_name="articles", blank=True
    )

    created_at = DateTimeField(auto_now_add=True, db_index=True)
    updated_at = DateTimeField(auto_now=True)

    class Meta(BaseModel.Meta):
        """
        Ensure uniqueness and fast lookups.
        """

        constraints: ClassVar[list[UniqueConstraint]] = [
            UniqueConstraint(Lower("slug"), name="uniq_article_slug_ci"),
        ]

        indexes: ClassVar[list[Index]] = [
            Index(fields=["author", "created_at"], name="idx_article_author_created"),
            Index(Lower("slug"), name="idx_article_slug_ci"),
            GinIndex(
                fields=["title"],
                name="gin_trgm_article_title",
                opclasses=["gin_trgm_ops"],
            ),
            GinIndex(
                fields=["text"],
                name="gin_trgm_article_text",
                opclasses=["gin_trgm_ops"],
            ),
        ]

        ordering: tuple[str, str] = ("-created_at", "title")

    def __str__(self) -> str:
        """
        Return article title.
        """

        return self.title

    def save(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        if not self.slug:
            base = slugify(self.title or "")[:150]
            self.slug = base or str(self.id)

        super().save(*args, **kwargs)


class ArticleRecipe(BaseModel):
    """
    Through model linking an Article to a Recipe that is mentioned in its text.
    """

    article = ForeignKey(Article, on_delete=CASCADE, related_name="recipe_refs")
    recipe = ForeignKey(Recipe, on_delete=CASCADE, related_name="article_refs")

    match_text = CharField(max_length=180, blank=True)
    first_index = CharField(max_length=24, blank=True)

    class Meta(BaseModel.Meta):
        """
        Ensure uniqueness and fast lookups.
        """

        constraints: ClassVar[list[UniqueConstraint]] = [
            UniqueConstraint(
                fields=["article", "recipe"],
                name="uniq_article_recipe_ref",
            )
        ]

        indexes: ClassVar[list[Index]] = [
            Index(fields=["article", "recipe"], name="idx_article_recipe_ref"),
        ]

    def __str__(self) -> str:
        """
        Return a simple representation of article's link.
        """

        return f"{self.article.id} → {self.recipe.id}"
