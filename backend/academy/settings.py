from pathlib import Path
from datetime import timedelta
from decouple import config

BASE_DIR=Path(__file__).resolve().parent.parent

# SECRET_KEY = config("SECRET_KEY")

SECRET_KEY=config(
    "SECRET_KEY",
    default="django-insecure-temporary-secret-key"
)

DEBUG=config("DEBUG",default=True,cast=bool)

ALLOWED_HOSTS=config(
    "ALLOWED_HOSTS",
    default="127.0.0.1,localhost",
    cast=lambda v: [host.strip() for host in v.split(",")],
)

# ALLOWED_HOSTS = config(
#     "ALLOWED_HOSTS",
#     default="127.0.0.1,localhost,python-academy-backend.onrender.com",
#     cast=lambda v: [host.strip() for host in v.split(",")],
# )








# ------------------------------------------------------------------------------
# Applications
# ------------------------------------------------------------------------------

INSTALLED_APPS=[

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party Apps
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "corsheaders",

    # Local Apps
    "accounts",
    "courses",
    "lessons",
    "enrollments",
    "certificates",
    "dashboard",
    "chatbot",
    "core",
]

# ------------------------------------------------------------------------------
# Middleware
# ------------------------------------------------------------------------------

MIDDLEWARE=[
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF="academy.urls"

TEMPLATES=[
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION="academy.wsgi.application"

# ------------------------------------------------------------------------------
# Database
# ------------------------------------------------------------------------------

DATABASES={
    "default":{
        "ENGINE":"django.db.backends.sqlite3",
        "NAME":BASE_DIR/"db.sqlite3",
    }
}

# ------------------------------------------------------------------------------
# Password Validation
# ------------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS=[
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# ------------------------------------------------------------------------------
# Internationalization
# ------------------------------------------------------------------------------

LANGUAGE_CODE="en-us"
TIME_ZONE="Asia/Kolkata"
USE_I18N=True
USE_TZ=True

# ------------------------------------------------------------------------------
# Static & Media
# ------------------------------------------------------------------------------

STATIC_URL="static/"

STATICFILES_DIRS=[
    BASE_DIR/"static",
]

STATIC_ROOT=BASE_DIR/"staticfiles"
MEDIA_URL="/media/"
MEDIA_ROOT=BASE_DIR/"media"

# ------------------------------------------------------------------------------
# Default Primary Key
# ------------------------------------------------------------------------------

AUTH_USER_MODEL="accounts.User"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------------------

CORS_ALLOWED_ORIGINS=[
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]

# ------------------------------------------------------------------------------
# REST Framework
# ------------------------------------------------------------------------------

REST_FRAMEWORK={
    "DEFAULT_AUTHENTICATION_CLASSES":(
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES":(
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS":"drf_spectacular.openapi.AutoSchema",
}

# ------------------------------------------------------------------------------
# JWT
# ------------------------------------------------------------------------------

SIMPLE_JWT={
    "ACCESS_TOKEN_LIFETIME":timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME":timedelta(days=7),
    "AUTH_HEADER_TYPES":("Bearer",),
}

# ------------------------------------------------------------------------------
# Swagger
# ------------------------------------------------------------------------------

SPECTACULAR_SETTINGS={
    "TITLE":"Python Academy API",
    "DESCRIPTION":"Production Ready Django REST API",
    "VERSION":"1.0.0",
}