"""
Contratos/constantes compartidas entre agente, prompt y herramientas.
"""

from nutriplan.views.recipes import MACRO_FIELD_MAP  # noqa: F401

FINAL_SCHEMA = {
    "status": "final",
    "answer_markdown": "string",
    "recipes": [
        {
            "id": "uuid",
            "slug": "string",
            "name": "string",
            "total_time": 25,
            "servings": 2,
            "primary_image": "url",
            "rating_avg": 4.5,
            "rating_count": 12,
        }
    ],
    "ingredient_names": ["string"],
}

TOOL_REQUEST_SCHEMA: dict[str, str] = {
    "status": "tool_request",
    "tool": "find_recipes | get_recipe_detail | find_ingredients | recommend",
    "args": "object",
}

TOOL_RESULT_ENVELOPE: dict[str, str | bool] = {
    "status": "tool_result",
    "tool": "string",
    "ok": True,
    "data": "any",
}

TOOLS_DOC = """
Herramientas disponibles (usá UNA por vez y respondé SIEMPRE en JSON):
- find_recipes(args: {{
    query?: string,
    categories?: string[],
    include_ingredients?: string[],
    exclude_ingredients?: string[],
    macro?: "calories"|"protein"|"carbs"|"fat"|"sugar",
    time_max?: number
}})
- get_recipe_detail(args: {{ name?: string, id?: string, slug?: string }})
- find_ingredients(args: {{ query: string }})
- recommend(args: {{
    ingredients: string[],
    categories?: string[],
    macro?: "calories"|"protein"|"carbs"|"fat"|"sugar"
}})
"""
