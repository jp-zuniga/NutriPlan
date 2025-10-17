"""
CRUD and messaging endpoints for Chefcito conversations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from django.db.models import Prefetch, QuerySet
from rest_framework.decorators import action
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from nutriplan.models import ChatMessage, ChatRole, ChatThread
from nutriplan.serializers.chat import (
    ChatMessageSerializer,
    ChatThreadSerializer,
    SendMessageSerializer,
)
from nutriplan.services.llm.chefcito import ChefcitoAgent, summarize_recipes_by_ids

from .permissions import ChatAccessPermission

if TYPE_CHECKING:
    from rest_framework.request import Request


class ChatThreadViewSet(ModelViewSet):
    """
    Conversations CRUD.

    Routes:
      - GET    /conversations
      - POST   /conversations
      - GET    /conversations/{id}
      - PATCH  /conversations/{id}
      - DELETE /conversations/{id}

    Extra actions:
      - GET    /conversations/{id}/messages
      - POST   /conversations/{id}/send
    """

    serializer_class = ChatThreadSerializer
    permission_classes: ClassVar[list[type[BasePermission]]] = [IsAuthenticated]

    def get_queryset(self) -> QuerySet[ChatThread]:  # type: ignore[override]
        user = self.request.user
        qs = ChatThread.objects.select_related("owner").prefetch_related(
            Prefetch("messages", queryset=ChatMessage.objects.order_by("created_at"))
        )

        return qs if user.is_staff else qs.filter(owner=user)

    def get_permissions(self) -> list[BasePermission]:
        if self.action in (
            "retrieve",
            "update",
            "partial_update",
            "destroy",
            "messages",
            "send",
        ):
            return [IsAuthenticated(), ChatAccessPermission()]
        return [IsAuthenticated()]

    @action(detail=True, methods=["get"])
    def messages(self, request: Request, pk: str | None = None) -> Response:  # noqa: ARG002
        """
        Return all messages of the thread (oldest first).
        """

        thread = self.get_object()
        limit = int(request.query_params.get("limit", 100))
        offset = int(request.query_params.get("offset", 0))

        qs = thread.messages.all().order_by("created_at")
        if offset:
            qs = qs[offset:]
        if limit:
            qs = qs[:limit]

        data = ChatMessageSerializer(qs, many=True).data
        return Response({"items": data, "count": len(data)}, status=HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def send(self, request: Request, pk: str | None = None) -> Response:  # noqa: ARG002
        """
        Append a user message and get Chefcito's reply. Persists both.

        Body: {
            "thread_id": <uuid>,
            "message": str,
            "history"?: [...],
            "title_if_empty"?: str
        }

        """

        thread = self.get_object()
        payload = request.data.copy()
        payload["thread_id"] = str(thread.id)
        ser = SendMessageSerializer(data=payload, context={"request": request})
        ser.is_valid(raise_exception=True)

        msg_text: str = ser.validated_data["message"]  # type: ignore[index]
        title_if_empty: str = ser.validated_data.get("title_if_empty") or ""  # type: ignore[assignment]

        # Create user message
        user_msg = ChatMessage.objects.create(
            thread=thread,
            role=ChatRole.USER,
            content=msg_text,
            meta={},
        )

        # If first title
        if title_if_empty and not (thread.title or "").strip():
            thread.title = title_if_empty.strip()[:120]
            thread.save(update_fields=["title"])

        # Build history from persisted messages (last 12, user/assistant only)
        prev = ChatMessage.objects.filter(
            thread=thread, role__in=[ChatRole.USER, ChatRole.ASSISTANT]
        ).order_by("-created_at")[:12]
        history = [{"role": m.role, "content": m.content} for m in reversed(list(prev))]

        agent = ChefcitoAgent()
        result = agent.chat(request.user, msg_text, history=history)

        # --- NORMALIZAR/HIDRATAR RECETAS PARA LA UI ---
        recipes_payload = result.get("recipes") or result.get("recipe_ids") or []
        recipes_full: list[dict] = []

        if isinstance(recipes_payload, list) and recipes_payload:
            # Si ya vienen objetos con 'id', los pasamos directo
            if isinstance(recipes_payload[0], dict) and "id" in recipes_payload[0]:
                recipes_full = recipes_payload
            # Si vienen como IDs (str), hidrátalos a resúmenes
            elif isinstance(recipes_payload[0], str):
                recipes_full = summarize_recipes_by_ids(recipes_payload)

        # Reescribir para que el frontend reciba objetos siempre
        result["recipes"] = recipes_full

        # Persist assistant message (y log de herramientas)
        assistant_meta = {
            "tools": result.get("used_tools") or [],
            "recipes": recipes_full,  # <-- ahora objetos, no solo IDs
            "ingredients": result.get("ingredients") or [],
        }
        assistant_msg = ChatMessage.objects.create(
            thread=thread,
            role=ChatRole.ASSISTANT,
            content=result.get("reply") or "",
            meta=assistant_meta,
        )

        # Update thread last activity
        thread.touch()

        return Response(
            {
                "thread": ChatThreadSerializer(thread).data,
                "message_user": ChatMessageSerializer(user_msg).data,
                "message_assistant": ChatMessageSerializer(assistant_msg).data,
                "recipes": recipes_full,
            },
            status=HTTP_201_CREATED,
        )

    def destroy(
        self,
        request: Request,  # noqa: ARG002
        *args,  # noqa: ANN002, ARG002
        **kwargs,  # noqa: ANN003, ARG002
    ) -> Response:
        thread = self.get_object()
        self.perform_destroy(thread)
        return Response(status=HTTP_204_NO_CONTENT)
