# type: ignore[reportAttributeAccessIssue]

from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from pytest import MonkeyPatch, mark
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_401_UNAUTHORIZED,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
)
from rest_framework.test import APIClient

from nutriplan.models import ChatMessage, ChatRole, ChatThread

from .factories import UserFactory

pytestmark = mark.django_db

User = get_user_model()

EXPECTED_MESSAGE_COUNT = 2


def _mock_agent_response() -> dict:
    return {
        "reply": "¡Ajúa! Te recomiendo **Pollo con arroz integral** 💪🍚",
        "recipes": ["11111111-1111-1111-1111-111111111111"],
        "ingredients": ["Pollo", "Arroz integral"],
        "used_tools": [{"tool": "find_recipes", "args": {"query": "pollo"}}],
    }


def test_create_and_list_threads(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, _user = auth_client

    # Crear
    url_list = reverse("conversation-list")
    res = client.post(url_list, {"title": "Mi hilo con Chefcito"}, format="json")

    assert res.status_code in (HTTP_200_OK, HTTP_201_CREATED), res.data

    thread_id = res.data["id"]

    # Listar (solo del dueño)
    res2 = client.get(url_list)
    assert res2.status_code == HTTP_200_OK

    ids = [it["id"] for it in res2.data]

    assert thread_id in ids


def test_permissions_cannot_access_others_thread(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, _user = auth_client
    other = User.objects.create_user(
        email="other@example.com",
        password="secret12345",
    )

    th = ChatThread.objects.create(owner=other, title="de otro")
    url_detail = reverse("conversation-detail", kwargs={"pk": th.id})
    res = client.get(url_detail)

    assert res.status_code == HTTP_404_NOT_FOUND


def test_send_appends_user_and_assistant_messages(
    monkeypatch: MonkeyPatch, auth_client: tuple[APIClient, UserFactory]
) -> None:
    client, _user = auth_client

    def _fake_chat(
        user: settings.AUTH_USER_MODEL,  # noqa: ARG001
        message: str,
        history: list[dict[str, str]] | None = None,  # noqa: ARG001
    ) -> dict:
        assert isinstance(message, str)
        assert message
        return _mock_agent_response()

    monkeypatch.setattr(
        "nutriplan.views.chat.ChefcitoAgent.chat", _fake_chat, raising=False
    )

    # Crear hilo
    url_list = reverse("conversation-list")
    res = client.post(url_list, {"title": ""}, format="json")

    assert res.status_code in (HTTP_200_OK, HTTP_201_CREATED), res.data

    thread_id = res.data["id"]

    # Enviar mensaje
    url_send = reverse("conversation-send", kwargs={"pk": thread_id})
    payload = {
        "message": "Quiero algo rápido con pollo",
        "title_if_empty": "Recetas con pollo (rápidas)",
    }

    res2 = client.post(url_send, payload, format="json")

    assert res2.status_code == HTTP_201_CREATED, res2.data

    # Respuesta incluye ambas entidades
    assert "message_user" in res2.data
    assert "message_assistant" in res2.data

    msg_user = res2.data["message_user"]
    msg_assist = res2.data["message_assistant"]

    assert msg_user["role"] == ChatRole.USER
    assert "pollo" in msg_user["content"].lower()

    assert msg_assist["role"] == ChatRole.ASSISTANT
    assert "recomiendo" in msg_assist["content"].lower()
    assert "tools" in msg_assist["meta"]
    assert msg_assist["meta"]["recipes"] == _mock_agent_response()["recipes"]

    # Persistencia en DB: 2 mensajes
    th = ChatThread.objects.get(id=thread_id)
    msgs = list(th.messages.order_by("created_at"))

    assert len(msgs) == EXPECTED_MESSAGE_COUNT
    assert msgs[0].role == ChatRole.USER
    assert msgs[1].role == ChatRole.ASSISTANT

    # Título aplicado si estaba vacío
    th.refresh_from_db()

    assert th.title == "Recetas con pollo (rápidas)"


def test_messages_endpoint_ordering(auth_client: tuple[APIClient, UserFactory]) -> None:
    client, user = auth_client
    th = ChatThread.objects.create(owner=user, title="orden")

    # crear 3 mensajes en orden de creación
    ChatMessage.objects.create(thread=th, role=ChatRole.USER, content="1", meta={})
    ChatMessage.objects.create(thread=th, role=ChatRole.ASSISTANT, content="2", meta={})
    ChatMessage.objects.create(thread=th, role=ChatRole.USER, content="3", meta={})

    url = reverse("conversation-messages", kwargs={"pk": th.id})
    res = client.get(url)

    assert res.status_code == HTTP_200_OK

    items = res.data["items"]

    assert [it["content"] for it in items] == ["1", "2", "3"]


def test_delete_thread_cascades_messages(
    auth_client: tuple[APIClient, UserFactory],
) -> None:
    client, user = auth_client
    th = ChatThread.objects.create(owner=user, title="borrar")
    ChatMessage.objects.create(thread=th, role=ChatRole.USER, content="hola", meta={})

    url_detail = reverse("conversation-detail", kwargs={"pk": th.id})
    res = client.delete(url_detail)

    assert res.status_code in (HTTP_200_OK, HTTP_204_NO_CONTENT)

    assert not ChatThread.objects.filter(id=th.id).exists()
    assert not ChatMessage.objects.filter(thread_id=th.id).exists()


def test_stateless_chat_endpoint_allowany(
    auth_client: APIClient, monkeypatch: MonkeyPatch
) -> None:
    """
    POST /chat/chefcito funciona sin autenticación y devuelve el shape esperado.
    """

    client, _user = auth_client

    def _fake_chat(
        user: settings.AUTH_USER_MODEL,  # noqa: ARG001
        message: str,
        history: list[dict[str, str]] | None = None,  # noqa: ARG001
        **kwargs,
    ) -> dict:
        assert isinstance(message, str)
        assert message
        return _mock_agent_response()

    monkeypatch.setattr(
        "nutriplan.views.chat.ChefcitoAgent.chat", _fake_chat, raising=False
    )

    url = reverse("chefcito_chat")
    res = client.post(url, {"message": "Hola Chefcito"}, format="json")

    assert res.status_code == HTTP_200_OK, res.data
    assert "reply" in res.data
    assert res.data["recipes"] == _mock_agent_response()["recipes"]


def test_cannot_send_without_auth() -> None:
    client = APIClient()
    dummy_id = uuid4()
    url_send = reverse("conversation-send", kwargs={"pk": dummy_id})
    res = client.post(url_send, {"message": "hola"}, format="json")

    assert res.status_code in (HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN)
