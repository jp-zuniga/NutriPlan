"""
URL and routing configuration.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from nutriplan.views.categories import CategoryViewSet
from nutriplan.views.ingredients import IngredientViewSet
from nutriplan.views.recipes import RecipeViewSet
from nutriplan.views.user import UserViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
]
