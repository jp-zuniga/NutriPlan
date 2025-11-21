# type: ignore[reportAttributeAccessIssue]

from typing import NoReturn

from django.conf import settings
from django.test import Client
from django.urls import reverse
from pytest import MonkeyPatch, mark, raises
from pytest_django.fixtures import SettingsWrapper
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.test import APIClient

from nutriplan.models import Provider, SocialAccount
from nutriplan.services.auth import google as google_service

from .conftest import TokenApplier

USER = settings.AUTH_USER_MODEL

pytestmark = mark.django_db


def test_register_and_login(
    client: APIClient, apply_tokens_to_client: TokenApplier
) -> None:
    # REGISTER devuelve tokens en el body (no cookies)
    url_register = reverse("register_user")
    payload = {
        "full_name": "Ana Lopez",
        "email": "ana@example.com",
        "password": "pass12345",
        "password_confirm": "pass12345",
    }

    res = client.post(url_register, payload, format="json")

    assert res.status_code == HTTP_201_CREATED

    body = res.data

    assert "access" in body
    assert "refresh" in body
    assert "user" in body
    assert body["user"]["email"] == "ana@example.com"

    # Simular frontend: poner tokens en cookies del client
    api_client = apply_tokens_to_client(client, body["access"], body["refresh"])

    # Ahora sí: endpoints autenticados por cookie
    url_me = reverse("user-me")
    res_me = api_client.get(url_me)

    assert res_me.status_code == HTTP_200_OK
    assert res_me.data["user"]["email"] == "ana@example.com"

    # LOGIN también devuelve tokens en el body
    url_login = reverse("login_user")
    res_login = api_client.post(
        url_login, {"email": "ana@example.com", "password": "pass12345"}, format="json"
    )

    assert res_login.status_code == HTTP_200_OK

    body_login = res_login.data

    assert "access" in body_login
    assert "refresh" in body_login


def test_login_requires_email_and_password(client: APIClient) -> None:
    url = reverse("login_user")

    assert client.post(url, {}).status_code == HTTP_400_BAD_REQUEST


def test_login_invalid_credentials(client: APIClient) -> None:
    url = reverse("login_user")

    assert (
        client.post(url, {"email": "nobody@x.y", "password": "nope"}).status_code
        == HTTP_401_UNAUTHORIZED
    )


def test_google_sign_in_creates_user(
    monkeypatch: MonkeyPatch, client: APIClient
) -> None:
    monkeypatch.setattr(
        google_service,
        "verify_google_id_token",
        lambda _: {
            "email": "gg@example.com",
            "sub": "google-sub-123",
            "name": "GG User",
            "picture": "https://example.com/gg.png",
            "given_name": "GG",
            "family_name": "User",
        },
    )

    url = reverse("google_sign_in")
    res = client.post(url, {"id_token": "FAKE"}, format="json")

    assert res.status_code in (HTTP_200_OK, HTTP_201_CREATED)

    body = res.data

    assert body["user"]["email"] == "gg@example.com"

    # <- cookies NO seteadas por el backend
    assert "np-access" not in res.cookies
    assert "np-refresh" not in res.cookies


def test_google_sign_in_existing_sa_updates(
    monkeypatch: MonkeyPatch, client: APIClient, django_user_model: USER
) -> None:
    user = django_user_model.objects.create_user(email="gg@example.com", password=None)
    SocialAccount.objects.create(
        user=user,
        provider=Provider.GOOGLE,
        provider_user_id="google-sub-123",
        email="gg@example.com",
        display_name="GG User",
        avatar_url="",
    )

    monkeypatch.setattr(
        google_service,
        "verify_google_id_token",
        lambda _: {
            "email": "gg@example.com",
            "sub": "google-sub-123",
            "name": "GG User",
            "picture": "https://example.com/gg2.png",
            "given_name": "GG",
            "family_name": "User",
        },
    )

    url = reverse("google_sign_in")
    res = client.post(url, {"id_token": "FAKE"}, format="json")

    assert res.status_code == HTTP_200_OK

    # <- cookies NO seteadas por el backend
    assert "np-access" not in res.cookies
    assert "np-refresh" not in res.cookies


def test_google_sign_in_requires_token(client: APIClient) -> None:
    url = reverse("google_sign_in")
    res = client.post(url, {})

    assert res.status_code == HTTP_400_BAD_REQUEST


def test_google_sign_in_bad_token(monkeypatch: MonkeyPatch, client: Client) -> None:
    def boom(*args, **kwargs) -> NoReturn:  # noqa: ANN002, ANN003, ARG001
        raise google_service.GoogleTokenError("x")  # noqa: EM101

    monkeypatch.setattr(google_service, "verify_google_id_token", boom)
    url = reverse("google_sign_in")
    res = client.post(url, {"id_token": "bad"})

    assert res.status_code == HTTP_400_BAD_REQUEST


def test_verify_google_id_token_happy_path(
    monkeypatch: MonkeyPatch, settings: SettingsWrapper
) -> None:
    settings.GOOGLE_CLIENT_ID = "client-123"

    def fake_verify(raw, req) -> dict[str, str | bool]:  # noqa: ANN001, ARG001
        return {
            "aud": "client-123",
            "iss": "https://accounts.google.com",
            "email": "x@y.z",
            "email_verified": True,
            "sub": "sub123",
            "name": "X Y",
            "picture": "http://p",
            "given_name": "X",
            "family_name": "Y",
            "hd": "",
        }

    monkeypatch.setattr(google_service.id_token, "verify_oauth2_token", fake_verify)
    out = google_service.verify_google_id_token("tok")

    assert out["email"] == "x@y.z"
    assert out["sub"] == "sub123"


def test_verify_google_id_token_bad_aud(
    monkeypatch: MonkeyPatch, settings: SettingsWrapper
) -> None:
    settings.GOOGLE_CLIENT_ID = ["ok"]

    def fake_verify(raw, req) -> dict[str, str | bool]:  # noqa: ANN001, ARG001
        return {
            "aud": "nope",
            "iss": "https://accounts.google.com",
            "email": "a@b.c",
            "email_verified": True,
            "sub": "s",
        }

    monkeypatch.setattr(google_service.id_token, "verify_oauth2_token", fake_verify)
    with raises(google_service.GoogleTokenError):
        google_service.verify_google_id_token("tok")


def test_verify_google_id_token_unverified_email(
    monkeypatch: MonkeyPatch, settings: SettingsWrapper
) -> None:
    settings.GOOGLE_CLIENT_ID = ["ok"]

    def fake_verify(raw, req) -> dict[str, str | bool]:  # noqa: ANN001, ARG001
        return {
            "aud": "ok",
            "iss": "https://accounts.google.com",
            "email": "a@b.c",
            "email_verified": False,
            "sub": "s",
        }

    monkeypatch.setattr(google_service.id_token, "verify_oauth2_token", fake_verify)
    with raises(google_service.GoogleTokenError):
        google_service.verify_google_id_token("tok")
