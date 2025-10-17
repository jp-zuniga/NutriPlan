"""
Utilities to extract recipe references from article text and sync M2M links.
"""

from __future__ import annotations

from re import Pattern, compile as comp, escape
from typing import TYPE_CHECKING

from django.db.transaction import atomic

from nutriplan.models import Article, ArticleRecipe, Recipe

if TYPE_CHECKING:
    from collections.abc import Iterable


def _build_matchers(recipes: Iterable[Recipe]) -> list[tuple[Recipe, Pattern[str]]]:
    matchers: list[tuple[Recipe, Pattern[str]]] = []
    for r in recipes:
        name = (r.name or "").strip()
        slug = (r.slug or "").strip()
        parts = [escape(name)]
        if slug and slug != name:
            parts.append(escape(slug))

        pat = r"(?i)(?<![\w/])(" + "|".join(parts) + r")(?![\w-])"
        matchers.append((r, comp(pat)))

    return matchers


def extract_recipe_ids_from_text(text: str) -> list[tuple[str, str, int]]:
    if not text:
        return []

    recs = Recipe.objects.only("id", "name", "slug").all()
    matchers = _build_matchers(recs)
    found: list[tuple[str, str, int]] = []

    lower_seen: set[str] = set()
    for r, pattern in matchers:
        m = pattern.search(text)
        if m:
            key = str(r.id)
            if key not in lower_seen:
                lower_seen.add(key)
                found.append((key, m.group(1), m.start(1)))

    return found


@atomic()
def sync_article_recipe_refs(article: Article, text: str | None = None) -> int:
    body = text if text is not None else (article.text or "")
    mentions = extract_recipe_ids_from_text(body)

    ArticleRecipe.objects.filter(article=article).delete()

    if not mentions:
        return 0

    objs = [
        ArticleRecipe(
            article=article, recipe_id=rid, match_text=mt[:180], first_index=str(idx)
        )
        for rid, mt, idx in mentions
    ]

    ArticleRecipe.objects.bulk_create(objs, ignore_conflicts=True)
    return len(objs)
