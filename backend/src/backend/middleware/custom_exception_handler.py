"""
Custom exception handler for NutriPlan.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc: Exception, context: str) -> Response:
    """
    Custom exception handler for Django REST Framework (DRF) exceptions.

    Args:
        exc: Exception instance raised during request processing.
        context: Additional context about the exception.

    Returns:
        Response: A DRF Response object with a standardized error format:
                 "error": <error_type>,
                 "message": <human_readable_message>,
                 "fields": <detailed_error_information>

    """

    response = exception_handler(exc, context)

    if response is None:
        return Response(
            {
                "error": "server_error",
                "message": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    detail = None
    if isinstance(response.data, dict):
        if "detail" in response.data:
            detail = response.data["detail"]
        elif "non_field_errors" in response.data:
            detail = response.data["non_field_errors"][0]
        elif len(response.data) == 1:
            _key, value = next(iter(response.data.items()))
            detail = value[0] if isinstance(value, list) else value
        else:
            detail = "Error de validación."

    formatted = {
        "error": "validation_error",
        "message": detail,
        "fields": response.data,
    }

    response.data = formatted
    return response
