from collections.abc import Callable, Generator
from datetime import timedelta
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

from django.conf import settings
from freezegun import freeze_time
from pytest import fixture
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import UserFactory

TokenApplier = Callable[[APIClient, str, str], APIClient]


@fixture(autouse=True)
def _clean_media_root() -> Generator:
    root = getattr(settings, "MEDIA_ROOT", None)
    yield
    if root and Path.is_dir(root):
        rmtree(root, ignore_errors=True)
        Path.mkdir(root, parents=True, exist_ok=True)


@fixture(autouse=True, scope="session")
def _settings_for_tests() -> None:
    settings.MEDIA_ROOT = Path(mkdtemp())
    settings.STATIC_ROOT = Path(mkdtemp())

    settings.ALLOWED_HOSTS = ["*"]
    settings.CORS_ALLOWED_ORIGIN_REGEXES = [r"^https?://.*$"]
    settings.DEBUG = False
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=5)
    settings.STATICFILES_STORAGE = (
        "django.contrib.staticfiles.storage.StaticFilesStorage"
    )


@fixture
def apply_tokens_to_client() -> TokenApplier:
    def _apply(client: APIClient, access: str, refresh: str) -> APIClient:
        client.cookies[settings.ACCESS_COOKIE_NAME] = access
        client.cookies[settings.REFRESH_COOKIE_NAME] = refresh
        return client

    return _apply


@fixture
def client() -> APIClient:
    return APIClient()


@fixture
def auth_client(client: APIClient) -> tuple[APIClient, UserFactory]:
    user = UserFactory()
    user.set_password("secret1234")
    user.save(update_fields=["password"])

    refresh = RefreshToken.for_user(user)
    client.cookies[settings.ACCESS_COOKIE_NAME] = str(refresh.access_token)
    client.cookies[settings.REFRESH_COOKIE_NAME] = str(refresh)

    return client, user


@fixture
def staff_client(client: APIClient) -> tuple[APIClient, UserFactory]:
    user = UserFactory(is_staff=True, is_superuser=True)
    user.set_password("secret1234")
    user.save(update_fields=["password"])

    refresh = RefreshToken.for_user(user)
    client.cookies[settings.ACCESS_COOKIE_NAME] = str(refresh.access_token)
    client.cookies[settings.REFRESH_COOKIE_NAME] = str(refresh)

    return client, user


@fixture
def frozen_time() -> Generator:
    with freeze_time("2025-01-01 12:00:00"):
        yield
