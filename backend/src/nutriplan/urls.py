"""
URL and routing configuration.
"""

from django.urls import include, path, re_path
from django.urls.resolvers import URLPattern, URLResolver
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from backend.custom_router import CustomRouter
from nutriplan.views import (
    CategoryViewSet,
    IngredientViewSet,
    RecipeCollectionViewSet,
    RecipeViewSet,
    UserViewSet,
    login_user,
    register_user,
)

router = CustomRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("collections", RecipeCollectionViewSet, basename="collection")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("users", UserViewSet, basename="user")

urlpatterns: list[URLResolver | URLPattern] = [
    path("", include(router.urls)),
    re_path(r"^auth/register/?$", register_user),
    re_path(r"^auth/login/?$", login_user),
    re_path(r"^auth/refresh/?$", TokenRefreshView.as_view()),
    re_path(r"^auth/verify/?$", TokenVerifyView.as_view()),
]
