# type: ignore[reportAttributeAccessIssue]

from decimal import Decimal

from django.urls import reverse
from pytest import mark
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_402_PAYMENT_REQUIRED,
)
from rest_framework.test import APIClient

from nutriplan.models import Ingredient, Recipe, Review

from .factories import (
    CategoryFactory,
    IngredientFactory,
    RecipeFactory,
    RecipeIngredientFactory,
    UserFactory,
)

pytestmark = mark.django_db


def _attach_ri(
    recipe: Recipe, ingredient: Ingredient, amount: int = 100, unit: str = "g"
) -> None:
    RecipeIngredientFactory(
        recipe=recipe, ingredient=ingredient, amount=amount, unit=unit
    )


def test_filter_by_category_name(client: APIClient) -> None:
    cat = CategoryFactory(name="Desayunos", friendly_name="Desayunos")

    r1 = RecipeFactory(category=cat)
    RecipeFactory()

    url = reverse("recipe-list") + "?category=Desayunos"
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    slugs = (
        [row["slug"] for row in res.data["results"]]
        if "results" in res.data
        else [r["slug"] for r in res.data]
    )

    assert r1.slug in slugs


def test_include_ingredients_match_all(client: APIClient) -> None:
    ing_a, ing_b, _ = IngredientFactory(), IngredientFactory(), IngredientFactory()

    r_ok = RecipeFactory(name="Tiene A y B")
    _attach_ri(r_ok, ing_a)
    _attach_ri(r_ok, ing_b)

    r_partial = RecipeFactory(name="Solo A")
    _attach_ri(r_partial, ing_a)

    url = reverse("recipe-list") + f"?include_ingredients={ing_a.id},{ing_b.id}"
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    rows = (
        res.data["results"]
        if isinstance(res.data, dict) and "results" in res.data
        else res.data
    )

    names = [r["name"] for r in rows]

    assert "Tiene A y B" in names
    assert "Solo A" not in names


def test_exclude_ingredients(client: APIClient) -> None:
    ing = IngredientFactory()
    r = RecipeFactory(name="Sin excluir")
    _attach_ri(r, ing)
    url = reverse("recipe-list") + f"?exclude_ingredients={ing.id}"
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    rows = (
        res.data["results"]
        if isinstance(res.data, dict) and "results" in res.data
        else res.data
    )

    names = [r["name"] for r in rows]

    assert "Sin excluir" not in names


def test_sort_macro_desc(client: APIClient) -> None:
    _ = RecipeFactory(protein_per_serving=Decimal("5.0"))
    _ = RecipeFactory(protein_per_serving=Decimal("15.0"))
    _ = RecipeFactory(protein_per_serving=Decimal("25.0"))

    url = reverse("recipe-list") + "?sort_macro=protein"
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    rows = (
        res.data["results"]
        if isinstance(res.data, dict) and "results" in res.data
        else res.data
    )

    proteins = [Decimal(str(r["protein_per_serving"])) for r in rows]

    assert proteins == sorted(proteins, reverse=True)


def test_recipe_reviews_subendpoint(client: APIClient) -> None:
    r = RecipeFactory()
    u1, u2 = users = UserFactory(), UserFactory()

    Review.objects.create(user=u1, recipe=r, rating=5, comment="Top")
    Review.objects.create(user=u2, recipe=r, rating=3, comment="Ok")
    url = reverse("recipe-reviews", kwargs={"slug": r.slug})
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    body = res.data

    assert len(body) == len(users)
    assert {row["rating"] for row in body} == {3, 5}


def test_recipe_rate_action(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, _ = auth_client

    r = RecipeFactory()
    url = reverse("recipe-rate", kwargs={"slug": r.slug})
    res = client.post(url, {"rating": 4, "comment": "rico"})

    assert res.status_code == HTTP_201_CREATED

    res2 = client.post(url, {"rating": 5})

    assert res2.status_code in (HTTP_400_BAD_REQUEST, HTTP_402_PAYMENT_REQUIRED)
