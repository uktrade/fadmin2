from .base import *  # noqa

#
# SASS_PROCESSOR_INCLUDE_DIRS = [
#     os.path.join(env('NODE_PATH'), '/govuk-frontend/govuk/all'),
# ]

# WEBPACK_LOADER = {
#     "DEFAULT": {
#         "CACHE": not DEBUG,
#         "BUNDLE_DIR_NAME": "build/",  # must end with slash
#         "STATS_FILE": "/app/front_end/config/webpack-stats.json"  #os.path.join(BASE_DIR, "front_end", "fido", "build", "webpack-stats.json"),
#     }
# }

STATICFILES_DIRS = ("/app/front_end/build/static",)

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

CLAM_AV_USERNAME = "TODO"
CLAM_AV_PASSWORD = "TODO"
CLAM_AV_URL = "https:clamav.london.cloudapps.digital/v2/scan"

IGNORE_ANTI_VIRUS = False
