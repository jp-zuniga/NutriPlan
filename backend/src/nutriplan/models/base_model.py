"""
Base model definition for NutriPlan.

Provides an abstract base model with a UUID primary key for all models.
"""

from uuid import uuid4

from django.db.models import Model, UUIDField


class BaseModel(Model):
    """
    Abstract base model that provides a UUID primary key field.
    """

    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        """
        Abstract base model with UUID primary key.
        """

        abstract = True
