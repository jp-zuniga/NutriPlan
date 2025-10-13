from collections.abc import Generator
from datetime import timedelta
from pathlib import Path
from shutil import rmtree
import tempfile

from django.conf import settings
from freezegun import freeze_time
from pytest import fixture
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .factories import UserFactory


@fixture(autouse=True)
def _clean_media_root() -> Generator:
    root = getattr(settings, "MEDIA_ROOT", None)
    yield
    if root and Path.is_dir(root):
        rmtree(root, ignore_errors=True)
        Path.mkdir(root, parents=True, exist_ok=True)


@fixture(autouse=True, scope="session")
def _settings_for_tests() -> None:
    settings.PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
    tmp = tempfile.mkdtemp()
    settings.MEDIA_ROOT = tmp
    settings.STATIC_ROOT = tmp
    settings.DEBUG = False
    settings.ALLOWED_HOSTS = ["*"]
    settings.CORS_ALLOWED_ORIGIN_REGEXES = [r"^https?://.*$"]
    settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"] = timedelta(minutes=5)


@fixture
def client() -> APIClient:
    return APIClient()


@fixture
def auth_client(client: APIClient) -> APIClient:
    user = UserFactory()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token!s}")
    return client


@fixture
def staff_client(client: APIClient) -> APIClient:
    user = UserFactory(is_staff=True, is_superuser=True)
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token!s}")
    return client


@fixture
def frozen_time() -> Generator:
    with freeze_time("2025-01-01 12:00:00"):
        yield
