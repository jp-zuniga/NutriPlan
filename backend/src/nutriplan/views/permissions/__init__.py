"""
Permission classes for NutriPlan API endpoints.
"""

from .chat import ChatAccessPermission
from .collections import CollectionAccessPermission
from .reviews import ReviewAccessPermission
from .users import UserAccessPermission

__all__: list[str] = [
    "ChatAccessPermission",
    "CollectionAccessPermission",
    "ReviewAccessPermission",
    "UserAccessPermission",
]
