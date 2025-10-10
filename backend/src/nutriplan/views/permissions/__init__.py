"""
Permission classes for NutriPlan API endpoints.
"""

from .collections import CollectionAccessPermission
from .reviews import ReviewAccessPermission
from .users import UserAccessPermission

__all__: list[str] = [
    "CollectionAccessPermission",
    "ReviewAccessPermission",
    "UserAccessPermission",
]
