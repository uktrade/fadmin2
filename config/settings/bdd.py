from .base import *  # noqa

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

INSTALLED_APPS += ("behave_django",)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "../front_end/build/static"),
    os.path.join(BASE_DIR, "../node_modules/govuk-frontend"),
)

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
    "simple_history.middleware.HistoryRequestMiddleware",
    "defender.middleware.FailedLoginMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "guardian.backends.ObjectPermissionBackend",
]

SELENIUM_HOST = env("SELENIUM_HOST", default="fido")
SELENIUM_ADDRESS = env("SELENIUM_ADDRESS", default="selenium-hub")

ASYNC_FILE_UPLOAD = True

IGNORE_ANTI_VIRUS = False

USE_SELENIUM_HUB = env("USE_SELENIUM_HUB", default=True)


# Only use cookies with https
CSRF_COOKIE_SECURE = True

# Make browser end session when user closes browser
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Set cookie expiry to 4 hours
SESSION_COOKIE_AGE = 4 * 60 * 60  # 4 hours

# Prevent client side JS from accessing CRSF token
CSRF_COOKIE_HTTPONLY = True

# Set content to no sniff
SECURE_CONTENT_TYPE_NOSNIFF = True

# Set HSTS (only allow access over https)
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
