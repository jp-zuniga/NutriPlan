from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import Avg, Count, Prefetch, QuerySet

from nutriplan.models import Recipe, RecipeImage

if TYPE_CHECKING:
    from collections.abc import Iterable


def summarize_recipes_by_ids(ids: Iterable[str]) -> list[dict[str, Any]]:
    id_list = [str(x) for x in ids if str(x).strip()]
    if not id_list:
        return []

    order_index = {s: i for i, s in enumerate(id_list)}

    qs: QuerySet[Recipe] = (
        Recipe.objects.filter(id__in=id_list)
        .prefetch_related(
            Prefetch(
                "recipe_images",
                queryset=RecipeImage.objects.select_related("image").order_by(
                    "order", "id"
                ),
            ),
        )
        .annotate(
            rating_avg=Avg("reviews__rating"),
            rating_count=Count("reviews", distinct=True),
        )
    )

    items = [
        {
            "id": str(r.id),
            "slug": r.slug,
            "name": r.name,
            "total_time": r.total_time,
            "servings": r.servings,
            "primary_image": r.primary_image,
            "rating_avg": float(r.rating_avg) if r.rating_avg is not None else None,  # type: ignore[reportAttributeAccessIssue]
            "rating_count": int(r.rating_count or 0),  # type: ignore[reportAttributeAccessIssue]
        }
        for r in qs
    ]

    # preservar el orden del cliente
    items.sort(key=lambda d: order_index.get(d["id"], 10**9))  # type: ignore[reportCallIssue]
    return items
