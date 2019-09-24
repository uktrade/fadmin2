from .base import *  # noqa

CAN_ELEVATE_SSO_USER_PERMISSIONS = True

INSTALLED_APPS += (
    'forecast_prototype',
    'webpack_loader',
)

STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "front_end", "fido", "build", "static"),
    "/front_end/fido/build/static",
    #"/fido/front_end/fido/dist/static",
)

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "build/",  # must end with slash
        "STATS_FILE": "/front_end/fido/config/webpack-stats.json"  #os.path.join(BASE_DIR, "front_end", "fido", "build", "webpack-stats.json"),
    }
}

# for debug_toolbar, to activate it only on localhost
INTERNAL_IPS = ['127.0.0.1']


SASS_PROCESSOR_INCLUDE_DIRS = [
    os.path.join('/node_modules'),
]
