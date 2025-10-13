from django.urls import reverse
from pytest import mark
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_204_NO_CONTENT,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from .factories import ReviewFactory

pytestmark = mark.django_db


def test_list_reviews_public(client: APIClient) -> None:
    ReviewFactory.create_batch(3)
    url = reverse("reviews-list")
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    body = res.json()

    assert "results" in body or isinstance(body, list)


def test_update_delete_permissions(client: APIClient) -> None:
    review = ReviewFactory(user=client.user)
    url = reverse("reviews-detail", kwargs={"pk": review.id})
    res = client.patch(url, {"comment": "editado"})

    assert res.status_code == HTTP_200_OK

    res2 = client.delete(url)

    assert res2.status_code == HTTP_204_NO_CONTENT


def test_cannot_modify_others_review(client: APIClient) -> None:
    review = ReviewFactory()
    url = reverse("reviews-detail", kwargs={"pk": review.id})

    assert client.patch(url, {"comment": "nope"}).status_code in (
        HTTP_403_FORBIDDEN,
        HTTP_404_NOT_FOUND,
    )
