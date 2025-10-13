from django.urls import reverse
from pytest import mark
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient

from .factories import RecipeCollectionFactory, RecipeFactory

pytestmark = mark.django_db


def test_create_collection(client: APIClient) -> None:
    url = reverse("collection-list")
    payload = {"name": "Mi Semana", "description": "Plan", "is_public": False}
    res = client.post(url, payload, format="json")

    assert res.status_code == HTTP_201_CREATED
    assert res.json()["name"] == "Mi Semana"


def test_by_slug(client: APIClient) -> None:
    c = RecipeCollectionFactory(owner=client.user)
    url = reverse("collection-by-slug", kwargs={"slug": c.slug})
    res = client.get(url)

    assert res.status_code == HTTP_200_OK
    assert res.json()["slug"] == c.slug


def test_add_and_remove_recipe(client: APIClient) -> None:
    c = RecipeCollectionFactory(owner=client.user)
    r = RecipeFactory()

    add = reverse("collection-add-recipe", kwargs={"pk": c.id})
    rem = reverse("collection-remove-recipe", kwargs={"pk": c.id})

    res = client.post(add, {"recipe_id": str(r.id)})

    assert res.status_code == HTTP_200_OK
    assert any(it["recipe"]["id"] == str(r.id) for it in res.json()["items"])

    res2 = client.post(rem, {"recipe_id": str(r.id)})

    assert res2.status_code == HTTP_200_OK
    assert not any(it["recipe"]["id"] == str(r.id) for it in res2.json()["items"])


def test_reorder_items(client: APIClient) -> None:
    c = RecipeCollectionFactory(owner=client.user)
    r1, r2 = RecipeFactory(), RecipeFactory()

    add = reverse("collection-add-recipe", kwargs={"pk": c.id})
    client.post(add, {"recipe_id": str(r1.id)})
    client.post(add, {"recipe_id": str(r2.id)})

    reorder = reverse("collection-reorder", kwargs={"pk": c.id})
    res = client.post(
        reorder,
        {
            "items": [
                {"recipe_id": str(r1.id), "order": 2},
                {"recipe_id": str(r2.id), "order": 1},
            ]
        },
        format="json",
    )

    assert res.status_code == HTTP_200_OK

    orders = [it["order"] for it in res.json()["items"]]

    assert orders == sorted(orders)
