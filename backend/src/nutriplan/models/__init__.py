"""
NutriPlan app models.
"""

from .category import Category
from .collection import CollectionItem, RecipeCollection
from .ingredient import Ingredient
from .recipe import Recipe, RecipeImage, RecipeIngredient
from .user import CustomUser, DietaryRestriction

__all__: list[str] = [
    "Category",
    "CollectionItem",
    "CustomUser",
    "DietaryRestriction",
    "Ingredient",
    "Recipe",
    "RecipeCollection",
    "RecipeImage",
    "RecipeIngredient",
]
