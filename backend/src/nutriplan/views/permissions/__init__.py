"""
Permission classes for NutriPlan API endpoints.
"""

from .ownership import CollectionAccessPermission
from .users import UserAccessPermission

__all__: list[str] = ["CollectionAccessPermission", "UserAccessPermission"]
