"""
Views package with viewsets and authentication endpoints.
"""

from .categories import CategoryViewSet
from .chefcito import chefcito_chat
from .collections import RecipeCollectionViewSet
from .ingredients import IngredientViewSet
from .recipes import RecipeViewSet
from .reviews import ReviewViewSet
from .users import UserViewSet

__all__: list[str] = [
    "CategoryViewSet",
    "IngredientViewSet",
    "RecipeCollectionViewSet",
    "RecipeViewSet",
    "ReviewViewSet",
    "UserViewSet",
    "chefcito_chat",
]
