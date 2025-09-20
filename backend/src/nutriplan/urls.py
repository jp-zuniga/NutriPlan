from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from nutriplan.views import (
    CategoryList,
    RecipeDetail,
    RecipeList,
    create_recipe,
    get_user_profile,
    login_user,
    register_user,
)

urlpatterns = [
    path("auth/register/", register_user, name="register"),
    path("auth/login/", login_user, name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/profile/", get_user_profile, name="profile"),
    path("recipes/", RecipeList.as_view(), name="recipe-list"),
    path("recipes/create/", create_recipe, name="recipe-create"),
    path("recipes/<str:pk>/", RecipeDetail.as_view(), name="recipe-detail"),
    path("categories/", CategoryList.as_view(), name="category-list"),
]
