import os
from pathlib import Path
from datetime import timedelta
from decouple import config
import dj_database_url

BASE_DIR=Path(__file__).resolve().parent.parent

# SECRET_KEY = config("SECRET_KEY")

SECRET_KEY = config("SECRET_KEY")

COURSE_DIAGNOSTIC_TOKEN = config("COURSE_DIAGNOSTIC_TOKEN", default="")

DEBUG=config("DEBUG",default=False,cast=bool)

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
    "cloudinary_storage",
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

# DATABASES={
#     "default":{
#         "ENGINE":"django.db.backends.sqlite3",
#         "NAME":BASE_DIR/"db.sqlite3",
#     }
# }

DATABASE_URL = config("DATABASE_URL", default="")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
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

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Cloudinary configuration
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME", default=""),
    "API_KEY": config("CLOUDINARY_API_KEY", default=""),
    "API_SECRET": config("CLOUDINARY_API_SECRET", default=""),
    "PREFIX": "",
}
CLOUDINARY_URL = (
    f"cloudinary://{config('CLOUDINARY_API_KEY', default='')}:"
    f"{config('CLOUDINARY_API_SECRET', default='')}@"
    f"{config('CLOUDINARY_CLOUD_NAME', default='')}"
)

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# ------------------------------------------------------------------------------
# Default Primary Key
# ------------------------------------------------------------------------------

AUTH_USER_MODEL="accounts.User"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"

# ------------------------------------------------------------------------------
# CORS
# ------------------------------------------------------------------------------

# CORS_ALLOW_ALL_ORIGINS = True



CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://python-academy-plum.vercel.app",
    "https://python-academy-5aev.onrender.com",
]

# ------------------------------------------------------------------------------
# REST Framework
# ------------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_RATES": {
        "anon": "10/hour",
        "user": "1000/hour",
    },
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


# ------------------------------------------------------------------------------
# Forgot Password - Email Configuration
# ------------------------------------------------------------------------------

FRONTEND_URL = config("FRONTEND_URL",default="https://python-academy-plum.vercel.app",
    # default="http://localhost:3000"
)

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST",default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT",default=587,cast=int)
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = config("EMAIL_HOST_USER",default="",)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD",default="")
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL",default=EMAIL_HOST_USER)
