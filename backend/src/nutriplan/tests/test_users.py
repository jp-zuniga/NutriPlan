# type: ignore[reportAttributeAccessIssue]

from django.urls import reverse
from pytest import mark
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_405_METHOD_NOT_ALLOWED,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from rest_framework.test import APIClient

from .factories import UserFactory

pytestmark = mark.django_db


def test_me_get_and_patch(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, user = auth_client

    url = reverse("user-me")
    res = client.get(url)

    assert res.status_code == HTTP_200_OK
    assert user.email == res.data["email"]

    res2 = client.patch(url, {"first_name": "Nuevo"})

    assert res2.status_code == HTTP_200_OK
    assert res2.data["first_name"] == "Nuevo"


def test_change_password(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, _ = auth_client

    url = reverse("user-change-password")
    res_bad = client.post(url, {"current_password": "mal", "new_password": "xx"})

    assert res_bad.status_code in (HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY)

    res_ok = client.post(
        url, {"current_password": "secret1234", "new_password": "otra_clave_123"}
    )

    assert res_ok.status_code == HTTP_204_NO_CONTENT


def test_user_list_requires_admin(
    auth_client: tuple[APIClient, UserFactory], client: APIClient
) -> None:
    a_client, _ = auth_client

    url = reverse("user-list")

    assert client.get(url).status_code in (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN)
    assert a_client.get(url).status_code in (
        HTTP_401_UNAUTHORIZED,
        HTTP_403_FORBIDDEN,
    )


def test_user_list_as_admin(staff_client: tuple[APIClient, UserFactory]) -> None:
    client, _ = staff_client

    url = reverse("user-list")
    res = client.get(url)

    assert res.status_code == HTTP_200_OK


def test_user_create_is_blocked(staff_client: tuple[APIClient, UserFactory]) -> None:
    client, _ = staff_client

    url = reverse("user-list")
    res = client.post(url, {})

    assert res.status_code == HTTP_405_METHOD_NOT_ALLOWED
