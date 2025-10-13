from django.test.client import RequestFactory
from pytest import mark, raises
from rest_framework.serializers import ValidationError

from nutriplan.serializers import (
    RecipeSerializer,
    ReviewSerializer,
    UserRegistrationSerializer,
)

from .factories import RecipeFactory, UserFactory

pytestmark = mark.django_db

TEST_RECIPE_AVG_RATING = 4.3
TEST_RECIPE_RATING_COUNT = 11


def test_user_registration_password_mismatch() -> None:
    ser = UserRegistrationSerializer(
        data={
            "full_name": "Juan Perez",
            "email": "jp@example.com",
            "phone_number": "",
            "password": "abc12345",
            "password_confirm": "abc00000",
        }
    )

    with raises(ValidationError):
        ser.is_valid(raise_exception=True)


def test_review_serializer_create_ok() -> None:
    user = UserFactory()
    recipe = RecipeFactory()
    rf = RequestFactory()

    req = rf.post("/fake")
    req.user = user
    ser = ReviewSerializer(
        data={"recipe_id": str(recipe.id), "rating": 4, "comment": "Buenísima."},
        context={"request": req},
    )

    assert ser.is_valid(), ser.errors
    obj = ser.save()

    assert obj.user_id == user.id
    assert obj.recipe_id == recipe.id


def test_recipe_serializer_includes_annotations() -> None:
    recipe = RecipeFactory()
    recipe.rating_avg = TEST_RECIPE_AVG_RATING
    recipe.rating_count = TEST_RECIPE_RATING_COUNT

    data = RecipeSerializer(recipe).data

    assert data["rating_avg"] == TEST_RECIPE_AVG_RATING
    assert data["rating_count"] == TEST_RECIPE_RATING_COUNT
