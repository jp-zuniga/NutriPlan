# type: ignore[reportAttributeAccessIssue]

from django.urls import reverse
from pytest import mark
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from .factories import RecipeCollectionFactory, RecipeFactory, UserFactory

pytestmark = mark.django_db


def test_create_collection(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, _ = auth_client

    url = reverse("collection-list")
    payload = {"name": "Mi Semana", "description": "Plan", "is_public": False}
    res = client.post(url, payload, format="json")

    assert res.status_code == HTTP_201_CREATED
    assert res.data["name"] == "Mi Semana"


def test_by_slug(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, user = auth_client

    c = RecipeCollectionFactory(owner=user)
    url = reverse("collection-by-slug", kwargs={"slug": c.slug})
    res = client.get(url)

    assert res.status_code == HTTP_200_OK
    assert res.data["slug"] == c.slug


def test_by_slug_not_found(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, _ = auth_client

    url = reverse("collection-by-slug", kwargs={"slug": "no-existe"})
    res = client.get(url)

    assert res.status_code in (HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)


def test_add_and_remove_recipe(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, user = auth_client

    c = RecipeCollectionFactory(owner=user)
    r = RecipeFactory()

    add = reverse("collection-add-recipe", kwargs={"id": c.id})
    rem = reverse("collection-remove-recipe", kwargs={"id": c.id})

    res = client.post(add, {"recipe_id": str(r.id)})

    assert res.status_code == HTTP_200_OK
    assert any(it["recipe"]["id"] == str(r.id) for it in res.data["items"])

    res2 = client.post(rem, {"recipe_id": str(r.id)})

    assert res2.status_code == HTTP_200_OK
    assert not any(it["recipe"]["id"] == str(r.id) for it in res2.data["items"])


def test_add_recipe_invalid_recipe_id(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, user = auth_client

    c = RecipeCollectionFactory(owner=user)

    url = reverse("collection-add-recipe", kwargs={"id": c.id})
    res = client.post(url, {"recipe_id": "00000000-0000-0000-0000-000000000000"})

    assert res.status_code == HTTP_400_BAD_REQUEST


def test_add_recipe_missing_recipe_id(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, user = auth_client
    c = RecipeCollectionFactory(owner=user)
    url = reverse("collection-add-recipe", kwargs={"id": c.id})
    res = client.post(url, {})
    assert res.status_code == HTTP_400_BAD_REQUEST


def test_remove_recipe_missing_recipe_id(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, user = auth_client

    c = RecipeCollectionFactory(owner=user)
    url = reverse("collection-remove-recipe", kwargs={"id": c.id})
    res = client.post(url, {})

    assert res.status_code == HTTP_400_BAD_REQUEST


def test_reorder_items(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, user = auth_client

    c = RecipeCollectionFactory(owner=user)
    r1, r2 = RecipeFactory(), RecipeFactory()

    add = reverse("collection-add-recipe", kwargs={"id": c.id})
    client.post(add, {"recipe_id": str(r1.id)})
    client.post(add, {"recipe_id": str(r2.id)})

    reorder = reverse("collection-reorder", kwargs={"id": c.id})
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

    orders = [it["order"] for it in res.data["items"]]

    assert orders == sorted(orders)


def test_reorder_items_requires_list(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, user = auth_client

    c = RecipeCollectionFactory(owner=user)
    url = reverse("collection-reorder", kwargs={"id": c.id})
    res = client.post(url, {"items": "no-es-lista"}, format="json")

    assert res.status_code == HTTP_400_BAD_REQUEST


def test_reorder_skips_entries_with_missing_fields(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, user = auth_client

    c = RecipeCollectionFactory(owner=user)
    r1, r2 = RecipeFactory(), RecipeFactory()

    add = reverse("collection-add-recipe", kwargs={"id": c.id})
    client.post(add, {"recipe_id": str(r1.id)})
    client.post(add, {"recipe_id": str(r2.id)})

    reorder = reverse("collection-reorder", kwargs={"id": c.id})
    res = client.post(
        reorder,
        {
            "items": [
                {"recipe_id": str(r1.id)},
                {"order": 1},
                {"recipe_id": str(r2.id), "order": 5},
            ]
        },
        format="json",
    )

    assert res.status_code == HTTP_200_OK
