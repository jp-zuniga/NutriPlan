# type: ignore[reportAttributeAccessIssue]

from django.urls import reverse
from pytest import mark
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
)
from rest_framework.test import APIClient

from .factories import ReviewFactory, UserFactory

pytestmark = mark.django_db


def test_list_reviews_public(client: APIClient) -> None:
    ReviewFactory.create_batch(3)
    url = reverse("reviews-list")
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    body = res.data

    assert "results" in body or isinstance(body, list)


def test_update_delete_permissions(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, user = auth_client

    review = ReviewFactory(user=user)
    url = reverse("reviews-detail", kwargs={"pk": review.id})
    res = client.patch(url, {"comment": "editado"})

    assert res.status_code == HTTP_200_OK

    res2 = client.delete(url)

    assert res2.status_code == HTTP_204_NO_CONTENT


def test_cannot_modify_others_review(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, _ = auth_client

    review = ReviewFactory()
    url = reverse("reviews-detail", kwargs={"pk": review.id})

    assert client.patch(url, {"comment": "nope"}).status_code in (
        HTTP_401_UNAUTHORIZED,
        HTTP_403_FORBIDDEN,
    )
