from datetime import timedelta
from decouple import config

# REST Framework Settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'EXCEPTION_HANDLER': 'base.exceptions.custom_exception_handler'
}

# Simple JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=int(config('JWT_ACCESS_TOKEN_LIFETIME_IN_HOURS'))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(config('JWT_REFRESH_TOKEN_LIFETIME_IN_DAYS'))),
    "UPDATE_LAST_LOGIN": True,
    "SIGNING_KEY": config('JWT_SECRET_KEY'),
}