from __future__ import annotations

from typing import Any

from django.db.models import Avg, Count, F, Q

from nutriplan.models import Ingredient, Recipe, RecipeImage, RecipeIngredient

from .contracts import MACRO_FIELD_MAP


def tool_find_recipes(args: dict[str, Any]) -> list[dict[str, Any]]:
    q = (args.get("query") or "").strip()
    categories = args.get("categories") or []
    include_ing = args.get("include_ingredients") or []
    exclude_ing = args.get("exclude_ingredients") or []
    macro = (args.get("macro") or "").strip().lower()
    time_max = args.get("time_max")

    qs = Recipe.objects.all()

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))

    if categories:
        qcat = Q()
        for tok in categories:
            tok = (tok or "").strip()  # noqa: PLW2901
            if not tok:
                continue

            qcat |= Q(categories__name__iexact=tok) | Q(
                categories__friendly_name__iexact=tok
            )

        qs = qs.filter(qcat).distinct()

    if include_ing:
        qs = qs.filter(recipe_ingredients__ingredient__name__in=include_ing)
        qs = qs.annotate(
            have_ing=Count(
                "recipe_ingredients__ingredient",
                filter=Q(recipe_ingredients__ingredient__name__in=include_ing),
                distinct=True,
            )
        ).filter(have_ing__gte=len(set(include_ing)))

    if exclude_ing:
        qs = qs.exclude(recipe_ingredients__ingredient__name__in=exclude_ing)

    if isinstance(time_max, (int, float)) and time_max >= 0:
        qs = qs.filter(total_time__lte=int(time_max))

    qs = qs.annotate(
        rating_avg=Avg("reviews__rating"),
        rating_count=Count("reviews", distinct=True),
    )

    order = ["-rating_avg", "name"]
    if macro in MACRO_FIELD_MAP:
        order.insert(0, f"-{MACRO_FIELD_MAP[macro]}")

    qs = qs.order_by(*order)[:15]

    out: list[dict[str, Any]] = [
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

    return out


def tool_get_recipe_detail(args: dict[str, Any]) -> dict[str, Any] | None:
    rid = (args.get("id") or "").strip()
    slug = (args.get("slug") or "").strip()
    name = (args.get("name") or "").strip()

    qs = Recipe.objects.all()
    if rid:
        qs = qs.filter(id=rid)
    elif slug:
        qs = qs.filter(slug__iexact=slug)
    elif name:
        qs = qs.filter(name__iexact=name)
    else:
        return None

    rec = qs.first()
    if not rec:
        return None

    ings = (
        RecipeIngredient.objects.filter(recipe=rec)
        .select_related("ingredient")
        .order_by("id")
    )
    imgs = (
        RecipeImage.objects.filter(recipe=rec)
        .select_related("image")
        .order_by("order", "id")
    )

    return {
        "id": str(rec.id),
        "slug": rec.slug,
        "name": rec.name,
        "description": rec.description,
        "instructions": rec.instructions,
        "servings": rec.servings,
        "prep_time": rec.prep_time,
        "cook_time": rec.cook_time,
        "total_time": rec.total_time,
        "calories_per_serving": float(rec.calories_per_serving or 0),
        "protein_per_serving": float(rec.protein_per_serving or 0),
        "carbs_per_serving": float(rec.carbs_per_serving or 0),
        "fat_per_serving": float(rec.fat_per_serving or 0),
        "sugar_per_serving": float(rec.sugar_per_serving or 0),
        "categories": list(rec.categories.values_list("friendly_name", flat=True)),
        "ingredients": [
            {
                "name": ri.ingredient.name,
                "amount": float(ri.amount),
                "unit": ri.unit,
            }
            for ri in ings
        ],
        "images": [
            {"url": ri.image.url, "alt_text": ri.image.alt_text, "order": ri.order}
            for ri in imgs
        ],
        "primary_image": rec.primary_image,
    }


def tool_find_ingredients(args: dict[str, Any]) -> list[dict[str, Any]]:
    q = (args.get("query") or "").strip()
    qs = Ingredient.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    qs = qs.order_by("name")[:25]
    return [
        {
            "id": str(i.id),
            "name": i.name,
            "calories_per_100g": float(i.calories_per_100g or 0),
            "protein_per_100g": float(i.protein_per_100g or 0),
            "carbs_per_100g": float(i.carbs_per_100g or 0),
            "fat_per_100g": float(i.fat_per_100g or 0),
            "sugar_per_100g": float(i.sugar_per_100g or 0),
        }
        for i in qs
    ]


def tool_recommend(
    args: dict[str, Any], *, dietary_restriction_ids: list | None
) -> list[dict[str, Any]]:
    names = [
        n for n in (args.get("ingredients") or []) if isinstance(n, str) and n.strip()
    ]

    categories = [
        c for c in (args.get("categories") or []) if isinstance(c, str) and c.strip()
    ]

    macro = (args.get("macro") or "").strip().lower()
    if not names:
        return []

    qs = Recipe.objects.all().prefetch_related("categories")

    if categories:
        qcat = Q()
        for tok in categories:
            qcat |= Q(categories__name__iexact=tok) | Q(
                categories__friendly_name__iexact=tok
            )

        qs = qs.filter(qcat).distinct()

    if dietary_restriction_ids:
        qs = qs.exclude(
            recipe_ingredients__ingredient__dietary_restrictions__id__in=dietary_restriction_ids
        )

    qs = qs.annotate(
        total_ing=Count("recipe_ingredients__ingredient", distinct=True),
        have_ing=Count(
            "recipe_ingredients__ingredient",
            filter=Q(recipe_ingredients__ingredient__name__in=names),
            distinct=True,
        ),
        missing_count=F("total_ing") - F("have_ing"),
        rating_avg=Avg("reviews__rating"),
        rating_count=Count("reviews", distinct=True),
    )

    order = ["missing_count", "-rating_avg", "name"]
    if macro in MACRO_FIELD_MAP:
        order.insert(1, f"-{MACRO_FIELD_MAP[macro]}")

    qs = qs.order_by(*order)[:15]

    out: list[dict[str, Any]] = [
        {
            "id": str(r.id),
            "slug": r.slug,
            "name": r.name,
            "missing_count": int(getattr(r, "missing_count", 0) or 0),
            "total_time": r.total_time,
            "servings": r.servings,
            "primary_image": r.primary_image,
            "rating_avg": float(r.rating_avg) if r.rating_avg is not None else None,  # type: ignore[reportAttributeAccessIssue]
            "rating_count": int(r.rating_count or 0),  # type: ignore[reportAttributeAccessIssue]
        }
        for r in qs
    ]

    return out
