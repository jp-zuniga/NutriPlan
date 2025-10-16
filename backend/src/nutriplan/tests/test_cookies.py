# type: ignore[reportAttributeAccessIssue]

from django.urls import reverse
from pytest import mark
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

pytestmark = mark.django_db

COOKIE_NAME = "nutriplan-refresh"


def test_register_sets_access_cookie_and_me_allows_cookie_auth(
    client: APIClient,
) -> None:
    url = reverse("register_user")
    payload = {
        "full_name": "Ana Gomez",
        "email": "ana-cookie@example.com",
        "phone_number": "",
        "password": "superclave123",
        "password_confirm": "superclave123",
    }

    res = client.post(url, payload, format="json")

    assert res.status_code == HTTP_201_CREATED

    # debe venir la cookie con el access token
    assert COOKIE_NAME in res.cookies

    morsel = res.cookies[COOKIE_NAME]

    assert morsel["httponly"] is True
    assert morsel["samesite"] in ("Lax", "Strict", "None")

    # usando el MISMO client (con cookie), /users/me debe funcionar sin header auth
    me = client.get(reverse("user-me"))

    assert me.status_code == HTTP_200_OK
    assert me.data["email"] == payload["email"]


def test_login_sets_access_cookie_and_me_allows_cookie_auth(client: APIClient) -> None:
    # primero registramos al usuario
    reg = reverse("register_user")
    payload = {
        "full_name": "Carlos Perez",
        "email": "carlos-cookie@example.com",
        "phone_number": "",
        "password": "otraclave123",
        "password_confirm": "otraclave123",
    }

    res_reg = client.post(reg, payload, format="json")

    assert res_reg.status_code == HTTP_201_CREATED

    # limpiamos cookies para asegurar que el login es quien autentica por cookie
    client.cookies.clear()

    login = reverse("login_user")
    res_login = client.post(
        login, {"email": payload["email"], "password": payload["password"]}
    )

    assert res_login.status_code == HTTP_200_OK

    # cookie presente y con flags seguros
    assert COOKIE_NAME in res_login.cookies

    morsel = res_login.cookies[COOKIE_NAME]

    assert morsel["httponly"] is True
    assert morsel["samesite"] in ("Lax", "Strict", "None")

    # /users/me debe responder OK sin Authorization (usa cookie)
    me = client.get(reverse("user-me"))

    assert me.status_code == HTTP_200_OK
    assert me.data["email"] == payload["email"]


def test_login_requires_email_and_password_for_cookie(client: APIClient) -> None:
    url = reverse("login_user")
    res = client.post(url, {})

    assert res.status_code == HTTP_400_BAD_REQUEST
