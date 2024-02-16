from pathlib import Path
from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = config("DEBUG", default=True, cast=bool)

SECRET_KEY = config("SECRET_KEY", default="development-secret-key")

ALLOWED_HOSTS = ["*"] if DEBUG else config("ALLOWED_HOSTS", cast=lambda hosts: [host.strip() for host in hosts.split(",") if host])

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # EXTERNAL APPS
    "debug_toolbar",

    # INTERNAL APPS
    "apps.core.apps.CoreConfig",
    "apps.user.apps.UserConfig",
    "apps.product.apps.ProductConfig",
    "apps.discount.apps.DiscountConfig",
    "apps.comment.apps.CommentConfig",
    "apps.order.apps.OrderConfig",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",

    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# INTERNATIONALIZATION
LANGUAGE_CODE = config("LANGUAGE_CODE", default="en-us")
TIME_ZONE = config("TIME_ZONE", default="en-us")
USE_I18N = True
USE_TZ = True

# STATIC
STATIC_URL = "static/"

# MEDIA
MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

if DEBUG:
    STATICFILES_DIRS = [BASE_DIR / 'static']

    # CACHE
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }

    # EMAIL
    EMAIL_USE_TLS = False
    EMAIL_HOST = "localhost"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""
    EMAIL_PORT = 25

    # DATABASE
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

    # DEBUG TOOLBAR
    INTERNAL_IPS = [
        "127.0.0.1",
    ]
else:
    STATIC_ROOT = BASE_DIR / "static"

    # REDIS
    REDIS_HOST = config("REDIS_HOST")
    REDIS_PORT = config("REDIS_PORT")
    REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    # CASHE
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": REDIS_URL,
        }
    }

    # EMAIL
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT")
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
    EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")

    # DATABASE POSTGRESQL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config("DB_NAME"),
            "USER": config("DB_USER"),
            "PASSWORD": config("DB_PASSWORD"),
            "HOST": config("DB_HOST"),
            "PORT": config("DB_PORT"),
        },
    }

# AUTH CONFIG
AUTH_USER_MODEL = "user.User"