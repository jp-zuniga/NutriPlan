"""
NutriPlan Django app configuration.
"""

from django.apps import AppConfig


class NutriplanConfig(AppConfig):
    """
    AppConfig for NutriPlan.

    Sets default auto field and app labels.
    """

    default_auto_field = "django.db.models.BigAutoField"
    label = "nutriplan"
    name = "nutriplan"

    def ready(self) -> None:
        """
        Import application models when the app is ready.
        """

        import nutriplan.models  # noqa: F401, PLC0415
