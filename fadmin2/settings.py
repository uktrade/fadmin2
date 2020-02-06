"""
Django settings for fadmin2 project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os

import dj_database_url

import environ

AUTH_USER_MODEL = 'core.User'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ENV_FILE = os.path.join(BASE_DIR, '.environ')

if os.path.exists(ENV_FILE):
    environ.Env.read_env(ENV_FILE)

env = environ.Env(
    DEBUG=(bool, False),
    RESTRICT_ADMIN=(bool, False)
)

DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

# ALLOWED_HOSTS = ['financeadmin-dev.cloudapps.digital','d3sy7fs6o4dizv.cloudfront.net',
# 'fadmin2.uat.uktrade.io','fna.uat.uktrade.io']

# Application definition

INSTALLED_APPS = [
    'authbroker_client',
    'custom_usermodel',
    # 'admintool_support.apps.AdmintoolSupportConfig',
    'downloadsupport.apps.DownloadSupportConfig',
    'forecast.apps.ForecastConfig',
    # 'dit_user_management',
    'gifthospitality.apps.GifthospitalityConfig',
    'payroll.apps.PayrollConfig',
    'costcentre.apps.CostCentreConfig',
    'chartofaccountDIT.apps.ChartAccountConfig',
    'treasuryCOA.apps.TreasuryCOAConfig',
    'treasurySS.apps.TreasurySSConfig',
    'core.apps.CoreConfig',
    'django_extensions',
    'django_tables2',
    'django_filters',
    'django_admin_listfilter_dropdown',
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'bootstrap4',
    'bootstrap_datepicker_plus'  # https://pypi.org/project/django-bootstrap-datepicker-plus/
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'core.middleware.ThreadLocalMiddleware',
    'authbroker_client.middleware.ProtectAllViewsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'fadmin2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'fadmin2.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

if 'VCAP_SERVICES' in os.environ:
    services = json.loads(os.getenv('VCAP_SERVICES'))
    DATABASE_URL = services['postgres'][0]['credentials']['uri']
else:
    DATABASE_URL = os.getenv('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL)
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-gb'  # must be gb for date entry to work

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


# Remove extra details in the label for the filter fields, it does not says 'contains' or similar
def FILTERS_VERBOSE_LOOKUPS():
    from django_filters.conf import DEFAULTS

    verbose_lookups = DEFAULTS['VERBOSE_LOOKUPS'].copy()
    verbose_lookups.update({
        'icontains': '',
        'contains': '',
        'startswith': '',
        'istartswith': '',
    })
    return verbose_lookups


AUTH_USER_MODEL = 'custom_usermodel.User'

AUTHBROKER_URL = env('AUTHBROKER_URL')
AUTHBROKER_CLIENT_ID = env('AUTHBROKER_CLIENT_ID')
AUTHBROKER_CLIENT_SECRET = env('AUTHBROKER_CLIENT_SECRET')
AUTHBROKER_SCOPES = 'read write'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'authbroker_client.backends.AuthbrokerBackend',
]


GIT_COMMIT = env('GIT_COMMIT')
LOGIN_URL = '/auth/login'
LOGIN_REDIRECT_URL = 'index'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# for debug_toolbar, to activate it only on localhost
INTERNAL_IPS = ['127.0.0.1']
