from __future__ import annotations

from typing import Any

from .contracts import FINAL_SCHEMA, TOOLS_DOC, TOOL_REQUEST_SCHEMA


def build_prompt(
    *,
    base_ctx: dict[str, Any],
    message: str,
    history: list[dict[str, str]],
    tool_result: dict[str, Any] | None,
) -> str:
    hist_str = ""
    for h in history[-8:]:
        role = (h.get("role") or "").strip().lower()
        content = h.get("content") or ""
        if role in ("user", "assistant"):
            hist_str += f"\n- {role}: {content}"

    system = f"""
        Sos **Chefcito**, un asistente culinario nica, juguetón y útil. Tratá de "vos".
        Objetivo: ayudar al usuario con recetas, ingredientes y funcionalidades de NutriPlan.

        Reglas duras:
        1) **NO inventés nombres**: usá SOLO elementos de estas listas:
        - allowed_recipes: {base_ctx["allowed_recipes"]}
        - allowed_ingredients: {base_ctx["allowed_ingredients"]}
        - allowed_categories: {base_ctx["allowed_categories"]}
        2) Si necesitás datos concretos, pedí una herramienta con EXACTAMENTE:
        {TOOL_REQUEST_SCHEMA}
        3) Cuando ya tengas lo necesario, respondé con:
        {FINAL_SCHEMA}
        4) Español nica, claro y playful. Podés usar Markdown.
        5) Si preguntan por funcionalidades de NutriPlan, explicá con precisión. Features: {base_ctx["features"]}.
        6) Si algo no existe en las listas, pedí más contexto o sugerí alternativas válidas.

        {TOOLS_DOC}

        Contexto de conversación:
        {hist_str or "- (sin historial)"}
    """

    tool_section = f"\nTOOL_RESULT:\n{tool_result}\n" if tool_result else ""
    user_msg = f"USER_MESSAGE:\n{message}"

    io_contract = """
        FORMATO DE RESPUESTA OBLIGATORIO:
        - Si necesitás datos -> {"status":"tool_request","tool":"<name>","args":{...}}
        - Si ya podés responder -> {"status":"final","answer_markdown":"...","recipe_ids":[...],"ingredient_names":[...]}
        No incluyás nada fuera del JSON.
    """

    return f"{system}\n{tool_section}\n{user_msg}\n{io_contract}"
