from decimal import Decimal

from django.db import IntegrityError
from pytest import mark, raises

from nutriplan.models import RecipeIngredient, Review

from .factories import IngredientFactory, RecipeFactory, ReviewFactory

pytestmark = mark.django_db

TEST_RATING = 5
TEST_RECIPE_NAME = "Gallo Pinto"

TEST_INGREDIENT_AMOUNT = 10
TEST_INGREDIENT_UNIT = "g"

TEST_CALORIES = Decimal("123.45")
TEST_SERVINGS = 3
TEST_TOTAL_CALORIES = TEST_SERVINGS * TEST_CALORIES

TEST_COOK_TIME = 13
TEST_PREP_TIME = 7
TEST_TOTAL_TIME = 20


def test_recipe_total_time_persisted() -> None:
    r = RecipeFactory(prep_time=TEST_PREP_TIME, cook_time=TEST_COOK_TIME)
    r.refresh_from_db()

    assert r.total_time == TEST_TOTAL_TIME


def test_recipe_total_calories_persisted() -> None:
    r = RecipeFactory(servings=TEST_SERVINGS, calories_per_serving=TEST_CALORIES)
    r.refresh_from_db()

    assert r.total_calories == TEST_TOTAL_CALORIES


def test_recipe_slug_autoincrement_when_duplicate_names() -> None:
    r1 = RecipeFactory(name=TEST_RECIPE_NAME, slug="")
    r2 = RecipeFactory(name=TEST_RECIPE_NAME, slug="")

    assert r1.slug != r2.slug


def test_recipe_ingredient_unique_per_recipe() -> None:
    r = RecipeFactory()
    ing = IngredientFactory()
    RecipeIngredient.objects.create(
        recipe=r,
        ingredient=ing,
        amount=TEST_INGREDIENT_AMOUNT,
        unit=TEST_INGREDIENT_UNIT,
    )

    with raises(IntegrityError):
        RecipeIngredient.objects.create(
            recipe=r,
            ingredient=ing,
            amount=TEST_INGREDIENT_AMOUNT * 2,
            unit=TEST_INGREDIENT_UNIT,
        )


def test_review_rating_constraint() -> None:
    review = ReviewFactory(rating=TEST_RATING)
    assert review.rating == TEST_RATING

    with raises(IntegrityError):
        Review.objects.create(user=review.user, recipe=review.recipe, rating=6)
