"""
URL and routing configuration.
"""

from django.urls import include, path, re_path
from django.urls.resolvers import URLPattern, URLResolver
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from backend.custom_router import CustomRouter
from nutriplan.views import (
    CategoryViewSet,
    ChatThreadViewSet,
    IngredientViewSet,
    RecipeCollectionViewSet,
    RecipeViewSet,
    ReviewViewSet,
    UserViewSet,
    chefcito_chat,
)
from nutriplan.views.auth import (
    RefreshCookieView,
    google_sign_in,
    login_user,
    logout_user,
    register_user,
)

router = CustomRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("conversations", ChatThreadViewSet, basename="conversation")
router.register("collections", RecipeCollectionViewSet, basename="collection")
router.register("ingredients", IngredientViewSet, basename="ingredient")
router.register("recipes", RecipeViewSet, basename="recipe")
router.register("reviews", ReviewViewSet, basename="reviews")
router.register("users", UserViewSet, basename="user")

urlpatterns: list[URLResolver | URLPattern] = [
    path("", include(router.urls)),
    re_path(r"^auth/google/?$", google_sign_in, name="google_sign_in"),
    re_path(r"^auth/login/?$", login_user, name="login_user"),
    re_path(r"^auth/logout/?$", logout_user, name="logout_user"),
    re_path(r"^auth/register/?$", register_user, name="register_user"),
    re_path(r"^auth/refresh/?$", TokenRefreshView.as_view(), name="token_refresh"),
    re_path(
        r"^auth/refresh-cookie/?$",
        RefreshCookieView.as_view(),
        name="token_refresh_cookie",
    ),
    re_path(r"^auth/verify/?$", TokenVerifyView.as_view(), name="token_verify"),
    re_path(r"^chefcito/chat/?$", chefcito_chat, name="chefcito_chat"),
]
