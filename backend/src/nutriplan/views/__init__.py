"""
Views package with viewsets and authentication endpoints.
"""

from .auth import get_user_profile, login_user, register_user
from .categories import CategoryViewSet
from .ingredients import IngredientViewSet
from .recipes import RecipeViewSet

__all__ = [
    "CategoryViewSet",
    "IngredientViewSet",
    "RecipeViewSet",
    "get_user_profile",
    "login_user",
    "register_user",
]
