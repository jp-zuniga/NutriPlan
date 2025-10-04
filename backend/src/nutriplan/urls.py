"""
URL and routing configuration.
"""

from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from nutriplan.views.auth import login_user, register_user
from nutriplan.views.categories import CategoryViewSet
from nutriplan.views.ingredients import IngredientViewSet
from nutriplan.views.recipes import RecipeViewSet
from nutriplan.views.user import UserViewSet

router = DefaultRouter(trailing_slash=r"/?")
router.register("categories", CategoryViewSet, basename="category")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("users", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    re_path(r"^auth/register/?$", register_user),
    re_path(r"^auth/login/?$", login_user),
    re_path(r"^auth/refresh/?$", TokenRefreshView.as_view()),
    re_path(r"^auth/verify/?$", TokenVerifyView.as_view()),
]
