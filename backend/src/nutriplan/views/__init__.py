"""
Views package with viewsets and authentication endpoints.
"""

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
]
