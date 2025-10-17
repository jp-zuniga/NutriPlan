"""
Permission classes for NutriPlan API endpoints.
"""

from .articles import ArticleDeletePermission, ArticleWritePermission
from .chat import ChatAccessPermission
from .collections import CollectionAccessPermission
from .reviews import ReviewAccessPermission
from .users import UserAccessPermission

__all__: list[str] = [
    "ArticleDeletePermission",
    "ArticleWritePermission",
    "ChatAccessPermission",
    "CollectionAccessPermission",
    "ReviewAccessPermission",
    "UserAccessPermission",
]
