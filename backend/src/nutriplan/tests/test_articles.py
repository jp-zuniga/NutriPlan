# type: ignore[reportIncompatibleVariableOverride]

from __future__ import annotations

from typing import TYPE_CHECKING

from django.conf import settings
from pytest import mark
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)

from nutriplan.models import Article, ArticleRecipe

if TYPE_CHECKING:
    from rest_framework.test import APIClient

    from .factories import RecipeFactory, UserFactory

pytestmark = mark.django_db

USER = settings.AUTH_USER_MODEL

BASE = "/articles"
EXPECTED_ARTICLE_RECIPE_COUNT = 2


def test_public_can_list_and_retrieve_articles(
    auth_client: tuple[APIClient, UserFactory],
    staff_client: tuple[APIClient, UserFactory],
    recipes_gallo_vigoron: tuple[RecipeFactory, RecipeFactory],  # noqa: ARG001
) -> None:
    a_client, _ = auth_client
    _, s_user = staff_client

    payload = {
        "title": "Desayunos con Gallo Pinto",
        "text": "Hoy hablamos del Gallo Pinto como base energética.",
    }

    resp_create = a_client.post(BASE, payload, format="json")

    assert resp_create.status_code == HTTP_201_CREATED, resp_create.data

    slug = resp_create.data["slug"]

    # Público puede listar
    resp_list = a_client.get(BASE)

    assert resp_list.status_code == HTTP_200_OK
    assert isinstance(resp_list.data, list)
    assert any(a["slug"] == slug for a in resp_list.data)

    # Público puede ver detalle
    resp_get = a_client.get(f"{BASE}/{slug}")

    assert resp_get.status_code == HTTP_200_OK

    body = resp_get.data

    assert isinstance(body["author"], dict)
    assert body["author"]["id"]
    assert body["author"]["email"] == s_user.email

    # Como menciona "Gallo Pinto", recipes debe incluirlo (autoref ejecutada en create)
    names = {r["name"] for r in body["recipes"]}

    assert "Gallo Pinto" in names


def test_staff_can_create_with_auto_recipe_refs(
    auth_client: tuple[APIClient, UserFactory],
    staff_client: tuple[APIClient, UserFactory],
    recipes_gallo_vigoron: tuple[RecipeFactory, RecipeFactory],
) -> None:
    a_client, _ = auth_client
    _, _ = staff_client
    gallo, vig = recipes_gallo_vigoron

    payload = {
        "title": "Menú típico",
        "text": f"Probá {gallo.name} por la mañana y {vig.name} al mediodía.",
    }

    resp = a_client.post(BASE, payload, format="json")
    data = resp.data

    assert resp.status_code == HTTP_201_CREATED, data

    assert data["title"] == payload["title"]

    # Verifica autoref por nombres
    rec_names = {r["name"] for r in data["recipes"]}

    assert rec_names == {"Gallo Pinto", "Vigorón"}

    # Verifica through en DB
    art = Article.objects.get(slug=data["slug"])
    refs = ArticleRecipe.objects.filter(article=art)

    assert refs.count() == EXPECTED_ARTICLE_RECIPE_COUNT
    assert list({str(x.recipe_id) for x in refs}) == list(
        {str(gallo.id), {str(vig.id)}}
    )

    assert list({str(x.recipe_id) for x in refs}) == list({str(gallo.id), str(vig.id)})


def test_staff_can_update_and_refs_resync(
    auth_client: tuple[APIClient, UserFactory],
    staff_client: tuple[APIClient, UserFactory],
    recipes_gallo_vigoron: tuple[RecipeFactory, RecipeFactory],
) -> None:
    a_client, _ = auth_client
    _, _ = staff_client
    gallo, vig = recipes_gallo_vigoron

    # Crear mencionando sólo Gallo Pinto
    resp_create = a_client.post(
        BASE,
        {"title": "Notas", "text": f"El {gallo.name} salva el día."},
        format="json",
    )

    assert resp_create.status_code == HTTP_201_CREATED

    slug = resp_create.data["slug"]

    # PATCH para ahora mencionar Vigorón y NO Gallo Pinto
    resp_patch = a_client.patch(
        f"{BASE}/{slug}",
        {"text": f"Para almuerzo, mejor {vig.name}."},
        format="json",
    )

    assert resp_patch.status_code == HTTP_200_OK, resp_patch.data

    names = {r["name"] for r in resp_patch.data["recipes"]}

    assert names == {"Vigorón"}

    art = Article.objects.get(slug=slug)
    refs = ArticleRecipe.objects.filter(article=art)

    assert refs.count() == 1
    assert refs.first().recipe.name == "Vigorón"


def test_delete_requires_admin(
    auth_client: tuple[APIClient, UserFactory],
    staff_client: tuple[APIClient, UserFactory],
    recipes_gallo_vigoron: tuple[RecipeFactory, RecipeFactory],
) -> None:
    a_client, _ = auth_client
    _, _ = staff_client
    gallo, vig = recipes_gallo_vigoron

    resp_create = a_client.post(
        BASE,
        {"title": "Borrable", "text": f"{gallo.name} presente."},
        format="json",
    )

    assert resp_create.status_code == HTTP_201_CREATED

    slug = resp_create.data["slug"]

    # Staff NO puede borrar
    resp_del_staff = a_client.delete(f"{BASE}/{slug}")

    assert resp_del_staff.status_code in (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN), (
        resp_del_staff.data
    )

    # Admin SÍ puede borrar
    resp_del_admin = a_client.delete(f"{BASE}/{slug}")

    assert resp_del_admin.status_code == HTTP_204_NO_CONTENT
    assert not Article.objects.filter(slug=slug).exists()


def test_create_forbidden_for_non_staff_and_anonymous(
    auth_client: tuple[APIClient, UserFactory],
    staff_client: tuple[APIClient, UserFactory],
    recipes_gallo_vigoron: tuple[RecipeFactory, RecipeFactory],
) -> None:
    a_client, _ = auth_client
    _, _ = staff_client
    gallo, _ = recipes_gallo_vigoron

    resp_user = a_client.post(
        BASE, {"title": "No debería", "text": f"Menciono {gallo.name}."}, format="json"
    )

    assert resp_user.status_code == HTTP_403_FORBIDDEN, resp_user.data

    # Anónimo -> HTTP_401_UNAUTHORIZED (falla IsAuthenticated)
    a_client.force_authenticate(user=None)
    resp_anonymous = a_client.post(
        BASE, {"title": "Anon", "text": "Nada"}, format="json"
    )

    assert resp_anonymous.status_code == HTTP_401_UNAUTHORIZED, resp_anonymous.data


def test_search_by_title_or_text(
    auth_client: tuple[APIClient, UserFactory],
    staff_client: tuple[APIClient, UserFactory],
    recipes_gallo_vigoron: tuple[RecipeFactory, RecipeFactory],
) -> None:
    a_client, _ = auth_client
    _, _ = staff_client
    gallo, vig = recipes_gallo_vigoron

    a_client.post(
        BASE,
        {"title": "Guía de desayunos", "text": f"El {gallo.name} manda en la mañana."},
        format="json",
    )

    a_client.post(
        BASE,
        {"title": "Almuerzos potentes", "text": f"Para la tarde, {vig.name} va bien."},
        format="json",
    )

    # Buscar por 'desayunos' (en title)
    a_client.force_authenticate(user=None)
    r1 = a_client.get(f"{BASE}?search=desayunos")

    assert r1.status_code == HTTP_200_OK
    assert len(r1.data) == 1
    assert r1.data[0]["title"].startswith("Guía de desayunos")

    # Buscar por 'tarde' (en text)
    r2 = a_client.get(f"{BASE}?search=tarde")

    assert r2.status_code == HTTP_200_OK
    assert len(r2.data) == 1
    assert r2.data[0]["title"].startswith("Almuerzos potentes")
