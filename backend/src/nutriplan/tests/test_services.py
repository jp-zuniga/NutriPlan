from __future__ import annotations

from typing import TYPE_CHECKING

from pytest import mark

from nutriplan.services import RecipeService, UserService

from .factories import IngredientFactory

if TYPE_CHECKING:
    from nutriplan.models import CustomUser

pytestmark = mark.django_db

TEST_EMAIL = "new@example.com"
TEST_DIET_RESTRICTION = "Intolerancia a la lactosa"


def test_user_service_create_and_restriction() -> None:
    user: CustomUser = UserService.create_user(
        {
            "email": TEST_EMAIL,
            "password": "strongpass123",
            "first_name": "New",
            "last_name": "User",
            "phone_number": "8888-8888",
        }
    )

    assert user.email == TEST_EMAIL

    UserService.add_dietary_restriction(user, TEST_DIET_RESTRICTION)
    user.refresh_from_db()

    assert user.dietary_restrictions.filter(name__iexact=TEST_DIET_RESTRICTION).exists()


def test_recipe_service_get_with_ingredients() -> None:
    ing1, ing2 = IngredientFactory(name="Frijol rojo"), IngredientFactory(name="Arroz")
    r1 = RecipeService.create_recipe(
        {"name": "Gallo Pinto", "description": "Tipiquísimo.", "category": "Desayuno"},
        [
            {"ingredient": ing1, "amount": 100, "unit": "g"},
            {"ingredient": ing2, "amount": 100, "unit": "g"},
        ],
    )

    q = RecipeService.get_recipes_with_ingredients(["Arroz"])

    assert r1 in list(q)
