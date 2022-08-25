"""
Django settings for podd_api project.

Generated by 'django-admin startproject' using Django 4.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from firebase_admin import initialize_app, credentials


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(
    BASE_DIR,
    "static",
)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-n1)2=u0#ol2=8v&wer-gg+w66y^=8bq2lr4+*0pt_5*1!&ca!o"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [".opensur.test", "localhost", ".ngrok.io"]


# Application definition
SHARED_APPS = (
    "accounts",
    "django_tenants",
    "tenants",
    "django_filters",
    "pagination",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.gis",
    "graphene_django",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "graphql_playground",
    "channels",
    "reports",
    "cases",
    "notifications",
    "summaries",
    "threads",
    "easy_thumbnails",
)

TENANT_APPS = (
    "django.contrib.contenttypes",
    "accounts",
    "reports",
    "cases",
    "notifications",
    "summaries",
    "threads",
    "easy_thumbnails",
)

INSTALLED_APPS = list(SHARED_APPS) + [
    app for app in TENANT_APPS if app not in SHARED_APPS
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django_tenants.middleware.main.TenantMainMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
]

# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.opensurclient\.test$",
#     r"^https://opensurclient\.test$",
#     r"^http://localhost:3000$",
# ]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = "podd_api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "podd_api.wsgi.application"
ASGI_APPLICATION = "podd_api.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django_tenants.postgresql_backend",
        "NAME": "open_surveillance",
        "USER": "pphetra",
        "PASSWORD": "1234",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

ORIGINAL_BACKEND = "django.contrib.gis.db.backends.postgis"

DATABASE_ROUTERS = ("django_tenants.routers.TenantSyncRouter",)

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "accounts.User"

GRAPHENE = {
    "SCHEMA": "podd_api.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

GRAPHQL_JWT = {
    "JWT_COOKIE_SAMESITE": "None",
    "JWT_COOKIE_SECURE": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(minutes=30),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=14),
    "JWT_PAYLOAD_HANDLER": "accounts.utils.custom_jwt_payload",
}


AUTO_LOGIN_AFTER_REGISTER = True

TENANT_MODEL = "tenants.Client"  # app.Model
TENANT_DOMAIN_MODEL = "tenants.Domain"  # app.Model

SHOW_PUBLIC_IF_NO_TENANT_FOUND = True

MEDIA_ROOT = BASE_DIR / "medias"

FIXTURE_DIRS = ["account/fixtures"]

CELERY_TASK_ALWAYS_EAGER = True

# begin ----override this firebase setup in local.py
credentials_config = {}
if credentials_config:
    FIREBASE_APP = initialize_app(credentials.Certificate(credentials_config))

# end ----

USE_S3 = os.getenv("USE_S3") == "TRUE"
if USE_S3:
    MEDIA_BUCKET_NAME = "ohtk-media-bucket"
    DEFAULT_FILE_STORAGE = "common.storage.S3MediaStorage"
    THUMBNAIL_DEFAULT_STORAGE = "common.storage.MediaStorage"
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = (
        os.getenv("AWS_STORAGE_BUCKET_NAME") or "ohtk-media-bucket"
    )
else:
    MEDIA_URL = "/medias/"
    MEDIA_BUCKET_NAME = ""
    DEFAULT_FILE_STORAGE = "common.storage.SimpleFileMediaStorage"
    THUMBNAIL_DEFAULT_STORAGE = "common.storage.SimpleFileMediaStorage"

THUMBNAIL_ALIASES = {
    "accounts.User.avatar": {
        "thumbnail": {"size": (50, 50), "crop": True},
    },
    "accounts.AuthorityUser.avatar": {
        "thumbnail": {"size": (50, 50), "crop": True},
    },
    "reports.Image.file": {
        "thumbnail": {"size": (200, 0), "crop": "smart"},
    },
    "threads.CommentAttachment.file": {
        "thumbnail": {"size": (200, 200), "crop": "smart"},
    },
}

FCM_DRY_RUN = True

try:
    from .local import *
except ImportError:
    pass
