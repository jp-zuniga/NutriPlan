"""
Serializers for NutriPlan app models.
"""

from .category import CategorySerializer
from .collection import (
    AddRemoveRecipeSerializer,
    CollectionItemReadSerializer,
    RecipeCollectionSerializer,
    ReorderItemsSerializer,
)
from .ingredient import IngredientSerializer
from .recipe import RecipeSerializer, RecommendationRecipeSerializer
from .review import ReviewReadSerializer, ReviewSerializer
from .user import (
    ChangePasswordSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
)

__all__: list[str] = [
    "AddRemoveRecipeSerializer",
    "CategorySerializer",
    "ChangePasswordSerializer",
    "CollectionItemReadSerializer",
    "IngredientSerializer",
    "RecipeCollectionSerializer",
    "RecipeSerializer",
    "RecommendationRecipeSerializer",
    "ReorderItemsSerializer",
    "ReviewReadSerializer",
    "ReviewSerializer",
    "UserProfileSerializer",
    "UserRegistrationSerializer",
]
