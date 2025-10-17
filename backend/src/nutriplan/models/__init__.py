"""
NutriPlan app models.
"""

from .article import Article, ArticleRecipe
from .category import Category
from .chat import ChatMessage, ChatRole, ChatThread
from .collection import CollectionItem, RecipeCollection
from .ingredient import Ingredient
from .recipe import Image, Recipe, RecipeImage, RecipeIngredient
from .review import Review
from .social import Provider, SocialAccount
from .user import CustomUser, DietaryRestriction

__all__: list[str] = [
    "Article",
    "ArticleRecipe",
    "Category",
    "ChatMessage",
    "ChatRole",
    "ChatThread",
    "CollectionItem",
    "CustomUser",
    "DietaryRestriction",
    "Image",
    "Ingredient",
    "Provider",
    "Recipe",
    "RecipeCollection",
    "RecipeImage",
    "RecipeIngredient",
    "Review",
    "SocialAccount",
]
