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
    'forecast.apps.ForecastConfig',
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
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


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
