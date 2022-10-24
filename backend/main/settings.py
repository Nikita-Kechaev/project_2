import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third party apps
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "oauth2_provider",
    "social_django",
    "rest_framework_social_oauth2",

    # Local apps
    "api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
DEBUG = int(os.getenv("DJANGO_DEBUG", default=0))
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", default="").split(" ")
ROOT_URLCONF = "main.urls"
WSGI_APPLICATION = "main.wsgi.application"
AUTH_USER_MODEL = 'api.User'

# General
APPEND_SLASH = True
LANGUAGE_CODE = "ru-RU"
LOGIN_REDIRECT_URL = "/"

CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
USE_L10N = True

USE_TZ = True
TIME_ZONE = "Europe/Moscow"

# Postgres
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
       'rest_framework.authentication.TokenAuthentication',
       'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
       'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ]
}

AUTHENTICATION_BACKENDS = [
    'social_core.backends.vk.VKOAuth2',
    'rest_framework_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
]

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv("AUTH_VK_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv("AUTH_VK_SECRET")

# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
#  STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = []
STATIC_URL = "/static/"
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)


# Media files
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
#  MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"


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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# Password validation

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


# Default primary key field type
DJOSER = {
    'USER_CREATE_PASSWORD_RETYPE': True,
    'HIDE_USERS': False,
    'LOGIN_FIELD': 'email',
    'SERIALIZERS': {
        'user': 'api.serializers.CustomUserSerializer',
        'current_user': 'api.serializers.CustomUserSerializer',
        'user_create_password_retype': 'api.serializers.CustomUserCreateSerializer',
    },
}
