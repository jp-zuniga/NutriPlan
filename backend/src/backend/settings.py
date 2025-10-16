"""
Global Django settings for NutriPlan.
"""

from datetime import timedelta
from os import getenv
from pathlib import Path
from sys import argv

from dj_database_url import DBConfig, config as db_config
from dotenv import load_dotenv

########################################################################################

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# 1) env variables: ####################################################################

for var in (
    "DATABASE_URL",
    "SECRET_KEY",
    "GOOGLE_API_KEY",
    "GOOGLE_CLIENT_ID",
    "GOOGLE_CLIENT_SECRET",
):
    if not getenv(var):
        msg = f"Definir `{var}` en variables de entorno."
        raise RuntimeError(msg)

DATABASE_URL = getenv("DATABASE_URL")
DEBUG = getenv("DEBUG", "False").lower() == "true"
GOOGLE_API_KEY = getenv("GOOGLE_API_KEY")
GOOGLE_CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = getenv("SECRET_KEY")
TESTING_DATABASE_URL = getenv("TESTING_DATABASE_URL")

# 2) general project config: ##########################################################

APPEND_SLASH = False
AUTH_USER_MODEL = "nutriplan.CustomUser"
ROOT_URLCONF = "backend.urls"
WSGI_APPLICATION = "backend.wsgi.application"
USE_X_FORWARDED_HOST = True

# 3) localization: ####################################################################

LANGUAGE_CODE = "es-ni"
TIME_ZONE = "America/Managua"
USE_I18N = True
USE_TZ = True

# 4) static config: ####################################################################

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# 5) django env: ######################################################################

INSTALLED_APPS: list[str] = [
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

MIDDLEWARE: list[str] = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# 6) networking: #######################################################################

ALLOWED_HOSTS: list[str] = [
    "localhost",
    "127.0.0.1",
    ".railway.app",
    ".nutri-plan.net",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS: list[str] = [
    "http://localhost:5173",
    "http://localhost:8000",
]

CORS_ALLOWED_ORIGIN_REGEXES: list[str] = [
    r"^https://([a-z0-9-]+\.)?nutri-plan\.net$",
    r"^https://([a-z0-9-]+\.)?railway\.app$",
    r"^https://([a-z0-9-]+\.)?up\.railway\.app$",
]

CSRF_TRUSTED_ORIGINS: list[str] = [
    "https://nutri-plan.net",
    "https://*.nutri-plan.net",
    "https://*.railway.app",
    "https://*.up.railway.app",
]

# 7) db config: ########################################################################

DATABASES: dict[str, DBConfig] = {
    "default": db_config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    )
}

if any("pytest" in arg for arg in argv):
    if TESTING_DATABASE_URL:
        DATABASES["default"] = db_config(
            default=TESTING_DATABASE_URL, conn_max_age=3, conn_health_checks=False
        )
    else:
        msg = "Definir `TESTING_DATABASE_URL` para correr tests."
        raise RuntimeError(msg)

# 8) API config: #######################################################################

COOKIE_SAMESITE = "Lax"
COOKIE_SECURE = not DEBUG
ACCESS_COOKIE_NAME = "access"
REFRESH_COOKIE_NAME = "refresh"


JWT_REFRESH_COOKIE_NAME = "nutriplan_refresh"
JWT_COOKIE_SECURE = not DEBUG
JWT_COOKIE_SAMESITE = "None" if not DEBUG else "Lax"
JWT_COOKIE_DOMAIN = "nutri-plan.net"
JWT_COOKIE_PATH = "/"

REST_FRAMEWORK: dict[str, tuple[str] | list[str] | str] = {
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

SIMPLE_JWT: dict[str, timedelta] = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

# 9) misc: #############################################################################

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = [
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
]

TEMPLATES: list[dict] = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
