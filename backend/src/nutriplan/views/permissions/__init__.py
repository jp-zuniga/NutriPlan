"""
Permission classes for NutriPlan API endpoints.
"""

from .ownership import IsOwnerOrAdmin
from .users import IsSelfOrAdmin

__all__: list[str] = ["IsOwnerOrAdmin", "IsSelfOrAdmin"]
