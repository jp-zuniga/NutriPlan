"""
Define a custom router that allows URLs to optionally end with a trailing slash.
"""

from rest_framework.routers import DefaultRouter


class CustomRouter(DefaultRouter):
    """
    Custom DRF router that makes trailing slashes in URLs optional.
    """

    def __init__(self, *args, **kwargs) -> None:  # noqa: ANN002, ANN003
        """
        Set `self.trailing_slash` as optional.
        """

        super().__init__(*args, **kwargs)
        self.trailing_slash = r"/?"
