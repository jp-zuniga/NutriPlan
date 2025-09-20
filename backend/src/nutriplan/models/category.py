from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    friendly_name = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["friendly_name"]

    def __str__(self) -> str:
        return self.friendly_name or self.name
