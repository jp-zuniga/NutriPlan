# type: ignore[reportAttributeAccessIssue]

from django.urls import reverse
from pytest import MonkeyPatch, mark
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
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
