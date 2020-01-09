from .base import *  # noqa
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

STATICFILES_DIRS = ("/app/front_end/build/static", "/app/node_modules/govuk-frontend")

# for debug_toolbar, to activate it only on localhost
INTERNAL_IPS = ["127.0.0.1"]

SASS_PROCESSOR_INCLUDE_DIRS = [os.path.join("/node_modules")]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "core.middleware.ThreadLocalMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authbroker_client.backends.AuthbrokerBackend",
    "guardian.backends.ObjectPermissionBackend",
]

ASYNC_FILE_UPLOAD = True

IGNORE_ANTI_VIRUS = True

SENTRY_KEY = env("SENTRY_KEY", default=None)
SENTRY_PROJECT = env("SENTRY_PROJECT", default=None)

sentry_sdk.init(
    dsn=f"https://{SENTRY_KEY}@sentry.ci.uktrade.io/{SENTRY_PROJECT}",
    integrations=[DjangoIntegration()]
)
