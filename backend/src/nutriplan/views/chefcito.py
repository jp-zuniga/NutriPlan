from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from nutriplan.services.llm.chefcito import ChefcitoAgent


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def chefcito_chat(request: Request) -> Response:
    data = request.data or {}
    message = (data.get("message") or "").strip()  # type: ignore[reportAttributeAccessIssue]

    if not message:
        return Response({"error": "message requerido."}, status=HTTP_400_BAD_REQUEST)

    history = data.get("history") or []  # type: ignore[reportAttributeAccessIssue]
    agent = ChefcitoAgent()
    res = agent.chat(
        request.user if getattr(request.user, "is_authenticated", False) else None,
        message,
        history=history,  # type: ignore[reportArgumentType]
    )

    status = (
        HTTP_200_OK if "reply" in res or "error" not in res else HTTP_400_BAD_REQUEST
    )

    return Response(res, status=status)
