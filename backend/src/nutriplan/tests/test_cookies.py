# type: ignore[reportAttributeAccessIssue]

from django.conf import settings
from django.urls import reverse
from pytest import mark
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from .conftest import TokenApplier

USER = settings.AUTH_USER_MODEL

pytestmark = mark.django_db


def test_register_tokens_then_me_via_cookie(
    client: APIClient, apply_tokens_to_client: TokenApplier
) -> None:
    url_register = reverse("register_user")
    res = client.post(
        url_register,
        {
            "full_name": "Ana Lopez",
            "email": "ana@example.com",
            "password": "pass12345",
            "password_confirm": "pass12345",
        },
        format="json",
    )

    assert res.status_code == HTTP_201_CREATED

    # Ya no esperamos cookies aquí
    assert "np-refresh" not in res.cookies
    assert "np-access" not in res.cookies

    body = res.data

    assert "access" in body
    assert "refresh" in body

    # Simular frontend: escribir cookies en el client
    api_client = apply_tokens_to_client(client, body["access"], body["refresh"])

    # Comprobar que /users/me acepta cookie-auth
    res_me = api_client.get(reverse("user-me"))

    assert res_me.status_code == HTTP_200_OK
    assert res_me.data["user"]["email"] == "ana@example.com"


def test_login_tokens_then_me_via_cookie(
    client: APIClient, django_user_model: USER, apply_tokens_to_client: TokenApplier
) -> None:
    _ = django_user_model.objects.create_user(
        email="ana@example.com",
        password="pass12345",  # noqa: S106
    )

    url_login = reverse("login_user")
    res = client.post(
        url_login, {"email": "ana@example.com", "password": "pass12345"}, format="json"
    )

    assert res.status_code == HTTP_200_OK

    # Ya no esperamos cookies aquí
    assert "np-refresh" not in res.cookies
    assert "np-access" not in res.cookies

    body = res.data
    assert "access" in body
    assert "refresh" in body

    # Simular frontend: escribir cookies en el client
    api_client = apply_tokens_to_client(client, body["access"], body["refresh"])

    # Comprobar que /users/me acepta cookie-auth
    res_me = api_client.get(reverse("user-me"))

    assert res_me.status_code == HTTP_200_OK
    assert res_me.data["user"]["email"] == "ana@example.com"


def test_login_requires_email_and_password_for_cookie(client: APIClient) -> None:
    url = reverse("login_user")
    res = client.post(url, {})

    assert res.status_code == HTTP_400_BAD_REQUEST
