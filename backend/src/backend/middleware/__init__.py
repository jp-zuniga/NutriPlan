"""
Middleware package for NutriPlan.

This package provides custom middleware components such as exception handlers.
"""

from .custom_exception_handler import custom_exception_handler

__all__ = ["custom_exception_handler"]
