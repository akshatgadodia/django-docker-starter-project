from decouple import config

# Media Files
MEDIA_ROOT = config('MEDIA_ROOT', default='')
MEDIA_URL = '/media/'
DATA_UPLOAD_MAX_MEMORY_SIZE = config('MAX_UPLOAD_SIZE', default=5242880)

# AWS_S3_SIGNATURE_NAME = config("AWS_S3_SIGNATURE_NAME")
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
# AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL")
# AWS_DEFAULT_ACL = config("AWS_DEFAULT_ACL", default=None)
# AWS_QUERYSTRING_AUTH = config("AWS_QUERYSTRING_AUTH", default=True, cast=bool)
# AWS_S3_FILE_OVERWRITE = config("AWS_S3_FILE_OVERWRITE", default=False, cast=bool)
# AWS_S3_ACCELERATE = config("AWS_S3_ACCELERATE", default=False, cast=bool)
#
# MEDIAFILES_LOCATION = ''
# DEFAULT_FILE_STORAGE = 'common.storage_backends.MediaStorage'
#
# MEDIA_URL = f'{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/'
