"""
Custom exception handler for NutriPlan.
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context) -> Response:
    """
    Format error requests with more descriptive fields and messages.
    """

    response = exception_handler(exc, context)

    if response is None:
        # Error no manejado por DRF (ej. 500 interno)
        return Response(
            {
                "error": "server_error",
                "message": str(exc),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    # Si DRF ya generó la respuesta, formateamos
    detail = None
    if isinstance(response.data, dict):
        # Si viene un mensaje general ("non_field_errors" o "detail")
        if "detail" in response.data:
            detail = response.data["detail"]
        elif "non_field_errors" in response.data:
            detail = response.data["non_field_errors"][0]
        elif len(response.data) == 1:
            # Extraer el primer mensaje para 'message'
            _key, value = next(iter(response.data.items()))
            detail = value[0] if isinstance(value, list) else value
        else:
            detail = "Error de validación."

    # Construir respuesta uniforme
    formatted = {
        "error": "validation_error",
        "message": detail,
        "fields": response.data,  # conserva info detallada
    }

    response.data = formatted
    return response
