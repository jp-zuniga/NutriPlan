from django.db.models import QuerySet
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.response import Response

from nutriplan.models import Recipe
from nutriplan.serializers import RecipeSerializer
from nutriplan.services.recipe_service import RecipeService


class RecipeList(generics.ListAPIView):
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]

    def __init__(self) -> None:
        super().__init__()

        self.request: Request

    def get_queryset(self) -> QuerySet[Recipe]:  # type: ignore[reportIncompatibleMethodOverride]
        queryset = Recipe.objects.all()
        category = self.request.query_params.get("category")
        if category:
            queryset = RecipeService.get_recipes_by_category(category)
        return queryset


class RecipeDetail(generics.RetrieveAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [permissions.AllowAny]


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def create_recipe(request: Request) -> Response:
    recipe_data = request.data.get("recipe", {})  # type: ignore[reportAttributeAccessIssue]
    ingredients_data = request.data.get("ingredients", [])  # type: ignore[reportAttributeAccessIssue]

    if (
        not recipe_data.get("name")  # type: ignore[reportAttributeAccessIssue]
        or not recipe_data.get("description")  # type: ignore[reportAttributeAccessIssue]
    ):
        raise ValidationError("Recipe name and description are required")

    try:
        recipe = RecipeService.create_recipe(recipe_data, ingredients_data)
        serializer = RecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except ValueError as e:
        raise ValidationError(str(e))
    except Exception as e:
        return Response(
            {"error": "An error occurred while creating the recipe"},
            status=status.HTTP_400_BAD_REQUEST,
        )
