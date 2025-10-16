# type: ignore[reportAttributeAccessIssue]

from decimal import Decimal

from django.urls import reverse
from pytest import mark
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from nutriplan.models import Ingredient, Recipe

from .factories import (
    CategoryFactory,
    DietaryRestrictionFactory,
    IngredientFactory,
    RecipeFactory,
    RecipeIngredientFactory,
    UserFactory,
)

pytestmark = mark.django_db

RECOMMEND_URL_NAME = "recipe-recommend"

MIN_EXPECTED_RECOMMENDATIONS = 4


def _attach(
    recipe: Recipe, ingredient: Ingredient, amount: int = 100, unit: str = "g"
) -> None:
    RecipeIngredientFactory(
        recipe=recipe, ingredient=ingredient, amount=amount, unit=unit
    )


def test_recommend_requires_at_least_one_ingredient(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, _ = auth_client
    url = reverse(RECOMMEND_URL_NAME)

    res = client.post(url, {"ingredients": []}, format="json")
    assert res.status_code == HTTP_400_BAD_REQUEST

    res2 = client.post(url, {}, format="json")
    assert res2.status_code == HTTP_400_BAD_REQUEST


def test_recommend_excludes_recipes_with_user_dietary_restrictions(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, user = auth_client

    # user con restricción
    restr = DietaryRestrictionFactory(name="Lactosa")
    user.dietary_restrictions.add(restr)

    # ingredientes
    ing_ok = IngredientFactory(name="Arroz")
    ing_bad = IngredientFactory(name="Leche")
    ing_bad.dietary_restrictions.add(restr)

    # recetas: una segura y otra con ingrediente restringido
    r_ok = RecipeFactory(name="Arroz con algo", protein_per_serving=Decimal("5.0"))
    _attach(r_ok, ing_ok)

    r_bad = RecipeFactory(name="Bebida láctea", protein_per_serving=Decimal("50.0"))
    _attach(r_bad, ing_bad)

    url = reverse(RECOMMEND_URL_NAME)
    res = client.post(url, {"ingredients": [str(ing_ok.id)]}, format="json")

    assert res.status_code == HTTP_200_OK

    names = [row["name"] for row in res.data]

    assert "Arroz con algo" in names
    assert "Bebida láctea" not in names


def test_recommend_missing_count_and_sorting(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, _ = auth_client

    # el usuario tiene A y B
    ing_a, ing_b, ing_c, ing_d = (
        IngredientFactory(),
        IngredientFactory(),
        IngredientFactory(),
        IngredientFactory(),
    )

    # recetas
    r_all = RecipeFactory(name="A+B")  # missing 0
    _attach(r_all, ing_a)
    _attach(r_all, ing_b)

    r_one = RecipeFactory(name="Solo A")  # missing 0
    _attach(r_one, ing_a)

    r_miss1 = RecipeFactory(name="A+C")  # missing 1
    _attach(r_miss1, ing_a)
    _attach(r_miss1, ing_c)

    r_miss2 = RecipeFactory(name="D solo")  # missing 1 (porque D no lo tiene)
    _attach(r_miss2, ing_d)

    url = reverse(RECOMMEND_URL_NAME)
    res = client.post(
        url, {"ingredients": [str(ing_a.id), str(ing_b.id)]}, format="json"
    )

    assert isinstance(res.data, list)
    assert len(res.data) >= MIN_EXPECTED_RECOMMENDATIONS

    # missing_count no-decreciente y los primeros con 0
    # missing_count no-decreciente y los primeros con 0
    missing_counts = [row["missing_count"] for row in res.data]
    assert missing_counts == sorted(missing_counts)
    assert missing_counts[0] == 0


def test_recommend_macro_secondary_sort_desc(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, _ = auth_client

    ing_a = IngredientFactory()
    ing_b = IngredientFactory()

    # mismas condiciones de missing_count (0), diferente macro (protein)
    r_low = RecipeFactory(name="Low Protein", protein_per_serving=Decimal("10.0"))
    _attach(r_low, ing_a)

    r_high = RecipeFactory(name="High Protein", protein_per_serving=Decimal("50.0"))
    _attach(r_high, ing_b)

    url = reverse(RECOMMEND_URL_NAME)
    res = client.post(
        url,
        {"ingredients": [str(ing_a.id), str(ing_b.id)], "macro": "protein"},
        format="json",
    )

    assert res.status_code == HTTP_200_OK

    names = [row["name"] for row in res.data]

    assert names.index("High Protein") < names.index("Low Protein")


def test_recommend_filters_by_multiple_categories_any_match(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, _ = auth_client

    cat1 = CategoryFactory(name="Desayunos", friendly_name="Desayunos")
    cat2 = CategoryFactory(name="Almuerzo", friendly_name="Almuerzo")
    cat3 = CategoryFactory(name="Cena", friendly_name="Cena")

    ing = IngredientFactory()

    r1 = RecipeFactory(name="Receta Desayuno", category=cat1)
    _attach(r1, ing)

    r2 = RecipeFactory(name="Receta Almuerzo", category=cat2)
    _attach(r2, ing)

    r3 = RecipeFactory(name="Receta Cena", category=cat3)
    _attach(r3, ing)

    url = reverse(RECOMMEND_URL_NAME)

    # acepta IDs y nombres; debe traer r1 y r2 (match en cualquiera)
    res = client.post(
        url,
        {
            "ingredients": [str(ing.id)],
            "categories": [str(cat2.id), "Desayunos"],
        },
        format="json",
    )

    assert res.status_code == HTTP_200_OK

    names = {row["name"] for row in res.data}

    assert "Receta Desayuno" in names
    assert "Receta Almuerzo" in names
    assert "Receta Cena" not in names
