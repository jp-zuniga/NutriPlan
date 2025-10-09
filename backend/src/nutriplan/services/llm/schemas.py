"""
JSON schemas for validating LLM responses.
"""

from typing import Any

CATEGORY_SCHEMA: dict[str, list[dict[str, Any]]] = {
    "items": [
        {
            "name": "Ensaladas",
            "friendly_name": "Ensaladas",
            "description": "Platos fríos o templados a base de vegetales.",
        }
    ]
}

INGREDIENT_SCHEMA: dict[str, list[dict[str, Any]]] = {
    "items": [
        {
            "name": "Tomate",
            "description": "Tomate rojo fresco, común en ensaladas y salsas.",
            "nutrition_per_100g": {
                "calories": 18,
                "protein_g": 0.9,
                "carbs_g": 3.9,
                "fat_g": 0.2,
                "sugar_g": 2.6,
            },
        }
    ]
}

RECIPE_SCHEMA: dict[str, list[dict[str, Any]]] = {
    "items": [
        {
            "name": "Ensalada de Tomate Sencilla",
            "description": "Ensalada fresca con tomates maduros.",
            "category_name": "Ensaladas",
            "servings": 2,
            "prep_time": 10,
            "cook_time": 0,
            "ingredients": [
                {"name": "Tomate", "amount": 200, "unit": "g"},
                {"name": "Aceite de oliva", "amount": 1, "unit": "tbsp"},
                {"name": "Sal", "amount": 1, "unit": "pinch"},
            ],
        }
    ]
}
