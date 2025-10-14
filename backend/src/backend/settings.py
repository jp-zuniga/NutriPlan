"""
Global Django settings for NutriPlan.
"""

from datetime import timedelta
from os import getenv
from pathlib import Path
from sys import argv

from dj_database_url import config as db_config
from dotenv import load_dotenv

load_dotenv()

#######################################################################################

ALLOWED_HOSTS = [
    "localhost:5173",
    "localhost:8000",
    "127.0.0.1",
    ".railway.app",
    "nutri-plan.net",
    "api.nutri-plan.net",
    "nightly-api.nutri-plan.net",
    "nightly.nutri-plan.net",
    "www.nutri-plan.net",
]

APPEND_SLASH = False
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
AUTH_USER_MODEL = "nutriplan.CustomUser"
BASE_DIR = Path(__file__).resolve().parent.parent
DEBUG = getenv("DEBUG", "False").lower() == "true"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
GOOGLE_CLIENT_IDS = [
    s for s in (getenv("GOOGLE_CLIENT_IDS", "") or "").split(",") if s.strip()
]

GOOGLE_HD = getenv("GOOGLE_HD", "")
LANGUAGE_CODE = "en-us"
ROOT_URLCONF = "backend.urls"
SECRET_KEY = getenv("SECRET_KEY")
SESSION_ENGINE = "django.contrib.sessions.backends.db"
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
TIME_ZONE = "America/Managua"
USE_I18N = True
USE_TZ = True
USE_X_FORWARDED_HOST = True
WSGI_APPLICATION = "backend.wsgi.application"

#######################################################################################

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1",
    "https://nutri-plan.net",
    "https://api.nutri-plan.net",
    "https://nightly-api.nutri-plan.net",
    "https://nightly.nutri-plan.net",
    "https://www.nutri-plan.net",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.railway\.app$",
    r"^https://.*\.up\.railway\.app$",
]

CSRF_TRUSTED_ORIGINS = [
    "https://*.up.railway.app",
    "https://*.railway.app",
    "https://nutri-plan.net",
    "https://api.nutri-plan.net",
    "https://nightly-api.nutri-plan.net",
    "https://nightly.nutri-plan.net",
    "https://www.nutri-plan.net",
]

DATABASES = {
    "default": db_config(
        default=getenv("DATABASE_URL"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

INSTALLED_APPS = [
    "nutriplan.apps.NutriPlanConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "EXCEPTION_HANDLER": "backend.middleware.custom_exception_handler.custom_exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

#######################################################################################

TESTING_DATABASE_URL = getenv("TESTING_DATABASE_URL")
RUNNING_TESTS = bool(
    getenv("PYTEST_CURRENT_TEST") or any("pytest" in arg for arg in argv)
)

if RUNNING_TESTS:
    if TESTING_DATABASE_URL:
        DATABASES["default"] = db_config(
            default=TESTING_DATABASE_URL, conn_max_age=3, conn_health_checks=False
        )
    else:
        msg = "Define TESTING_DATABASE_URL para tests."
        raise RuntimeError(msg)
