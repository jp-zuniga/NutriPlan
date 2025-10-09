"""
Views package with viewsets and authentication endpoints.
"""

from .auth import get_user_profile, google_sign_in, login_user, register_user
from .categories import CategoryViewSet
from .collections import RecipeCollectionViewSet
from .ingredients import IngredientViewSet
from .recipes import RecipeViewSet
from .user import UserViewSet

__all__: list[str] = [
    "CategoryViewSet",
    "IngredientViewSet",
    "RecipeCollectionViewSet",
    "RecipeViewSet",
    "UserViewSet",
    "get_user_profile",
    "google_sign_in",
    "login_user",
    "register_user",
]
