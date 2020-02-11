from .base import *  # noqa
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

MIDDLEWARE += [
    "authbroker_client.middleware.ProtectAllViewsMiddleware",
]

AUTHENTICATION_BACKENDS += [
    "authbroker_client.backends.AuthbrokerBackend",
]

STATICFILES_DIRS = ("/app/front_end/build/static",)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

IGNORE_ANTI_VIRUS = False

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': CELERY_BROKER_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'cache_'
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': env('DJANGO_LOG_LEVEL', default='INFO'),
        },
    },
}

SENTRY_KEY = env("SENTRY_KEY", default=None)
SENTRY_PROJECT = env("SENTRY_PROJECT", default=None)

if SENTRY_KEY and SENTRY_PROJECT:
    sentry_sdk.init(
        dsn=f"https://{SENTRY_KEY}@sentry.ci.uktrade.io/{SENTRY_PROJECT}",
        integrations=[DjangoIntegration()]
    )

# HSTS (https://man.uktrade.io/docs/procedures/1st-go-live.html)
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = True

# ## IHTC compliance

# Only use cookies with https
CSRF_COOKIE_SECURE = True

# Make browser end session when user closes browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Set cookie expiry to 4 hours
SESSION_COOKIE_AGE = 4 * 60 * 60  # 4 hours in seconds

# Set session cookie to be secure
SESSION_COOKIE_SECURE = True

# Prevent client side JS from accessing CRSF token
CSRF_COOKIE_HTTPONLY = True

# Prevent client side JS from accessing session cookie (true by default)
SESSION_COOKIE_HTTPONLY = True

# Set content to no sniff
SECURE_CONTENT_TYPE_NOSNIFF = True
