from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    dietary_restrictions = models.ManyToManyField(
        "DietaryRestriction", blank=True, related_name="users"
    )

    def __str__(self) -> str:
        return self.email


class DietaryRestriction(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name
