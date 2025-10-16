from __future__ import annotations

from typing import Any

from nutriplan.services.llm.gemini import GeminiClient

from .context import build_base_context
from .contracts import TOOL_REQUEST_SCHEMA
from .prompt import build_prompt
from .tools import (
    tool_find_ingredients,
    tool_find_recipes,
    tool_get_recipe_detail,
    tool_recommend,
)


class ChefcitoAgent:
    """
    Orquestador de diálogo con herramientas controladas y contexto NutriPlan.
    """

    def __init__(self, client: GeminiClient | None = None) -> None:
        self.client = client or GeminiClient()
        self.max_recipes = 220
        self.max_ingredients = 450
        self.max_categories = 80
        self.max_iters = 3

    def chat(
        self,
        user,
        message: str,
        history: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        if not message or not isinstance(message, str):
            return {"error": "message requerido."}

        used_tools: list[dict[str, Any]] = []
        tool_result_payload: dict[str, Any] | None = None

        base_ctx = build_base_context(
            user,
            max_recipes=self.max_recipes,
            max_ingredients=self.max_ingredients,
            max_categories=self.max_categories,
        )

        for _ in range(self.max_iters):
            prompt = build_prompt(
                base_ctx=base_ctx,
                message=message,
                history=history or [],
                tool_result=tool_result_payload,
            )

            llm_out = self.client.generate_json(prompt)
            if not isinstance(llm_out, dict):
                return {
                    "reply": "Ups, tuve un enredo interpretando la respuesta. Probá de nuevo 🤏"
                }

            status = (llm_out.get("status") or "").strip().lower()

            if status == "final":
                reply = (llm_out.get("answer_markdown") or "").strip() or "¡Listo!"
                return {
                    "reply": reply,
                    "recipes": llm_out.get("recipe_ids") or [],
                    "ingredients": llm_out.get("ingredient_names") or [],
                    "used_tools": used_tools,
                }

            if status == "tool_request":
                tool = (llm_out.get("tool") or "").strip()
                args = llm_out.get("args") or {}
                result_env = self._run_tool(tool, args, base_ctx)
                used_tools.append({"tool": tool, "args": args})
                tool_result_payload = result_env
                continue

            # si no respeta contrato, devolvemos ayuda
            return {
                "reply": (
                    "Te escucho 👩‍🍳 ¿Qué querés cocinar hoy? "
                    "Pedime recetas, filtros o recomendaciones por ingredientes."
                ),
                "recipes": [],
                "ingredients": [],
                "used_tools": used_tools,
            }

        return {
            "reply": "Voy a necesitar un poquito más de detalle para ayudarte mejor 😊",
            "recipes": [],
            "ingredients": [],
            "used_tools": used_tools,
        }

    # -------------------- ejecución de herramientas --------------------

    def _run_tool(
        self,
        tool: str,
        args: dict[str, Any],
        base_ctx: dict[str, Any],
    ) -> dict[str, Any]:
        handlers = {
            "find_recipes": lambda: tool_find_recipes(args),
            "get_recipe_detail": lambda: tool_get_recipe_detail(args),
            "find_ingredients": lambda: tool_find_ingredients(args),
            "recommend": lambda: tool_recommend(
                args,
                dietary_restriction_ids=(base_ctx.get("user") or {}).get(
                    "dietary_restriction_ids"
                ),
            ),
        }

        fn = handlers.get(tool)
        if not fn:
            return {
                "status": "tool_result",
                "tool": tool,
                "ok": False,
                "error": "tool desconocida",
            }

        try:
            data = fn()
            return {"status": "tool_result", "tool": tool, "ok": True, "data": data}
        except Exception as e:  # noqa: BLE001
            return {
                "status": "tool_result",
                "tool": tool,
                "ok": False,
                "error": f"falló {tool}: {e}",
                "hint": f"Respetá el esquema {TOOL_REQUEST_SCHEMA}",
            }
