# type: ignore[reportAttributeAccessIssue]

from typing import NoReturn

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

from nutriplan.services.auth import google as google_service

pytestmark = mark.django_db


def test_register_and_login(client: APIClient) -> None:
    reg = reverse("register_user")
    payload = {
        "full_name": "Ana Gomez",
        "email": "ana@example.com",
        "phone_number": "",
        "password": "superclave123",
        "password_confirm": "superclave123",
    }

    res = client.post(reg, payload, format="json")

    assert res.status_code == HTTP_201_CREATED
    assert "access" in res.data
    assert "refresh" in res.data

    login = reverse("login_user")
    res2 = client.post(login, {"email": "ana@example.com", "password": "superclave123"})

    assert res2.status_code == HTTP_200_OK
    assert "access" in res2.data


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
    def fake_verify(_token: str) -> dict[str, str]:
        return {
            "email": "gg@example.com",
            "sub": "google-sub-123",
            "name": "GG User",
            "picture": "https://example.com/a.png",
            "given_name": "GG",
            "family_name": "User",
        }

    monkeypatch.setattr(google_service, "verify_google_id_token", fake_verify)
    url = reverse("google_sign_in")
    res = client.post(url, {"id_token": "fake"})

    assert res.status_code in (HTTP_200_OK, HTTP_201_CREATED)

    data = res.data

    assert data["user"]["email"] == "gg@example.com"
    assert "access" in data
    assert "refresh" in data


def test_google_sign_in_existing_sa_updates(
    monkeypatch: MonkeyPatch, client: APIClient
) -> None:
    test_google_sign_in_creates_user(monkeypatch, client)

    def fake_verify2(_token: str) -> dict[str, str]:
        return {
            "email": "gg@example.com",
            "sub": "google-sub-123",
            "name": "GG User 2",
            "picture": "https://example.com/b.png",
            "given_name": "GG",
            "family_name": "User",
        }

    monkeypatch.setattr(google_service, "verify_google_id_token", fake_verify2)
    url = reverse("google_sign_in")
    res = client.post(url, {"id_token": "fake"})

    assert res.status_code == HTTP_200_OK
    assert res.data["created"] is False


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
    settings.GOOGLE_CLIENT_IDS = ["client-123"]

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
    settings.GOOGLE_CLIENT_IDS = ["ok"]

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
    settings.GOOGLE_CLIENT_IDS = ["ok"]

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
