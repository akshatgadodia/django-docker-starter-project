import os
from decouple import config

from backend.settings.base import BASE_DIR


LOGS_DIR = os.path.join(BASE_DIR, config('LOGS_DIR', default='logs'))
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logs_file_size = config('MAX_LOGS_FILE_SIZE_IN_MB', cast=int, default=2)
logs_file_backup_count = config('MAX_LOGS_FILE_TO_STORED', cast=int, default=5)

logging = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'sql_queries_tracking_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': logs_file_size * 1024 * 1024,
            'backupCount': logs_file_backup_count,
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'sql_queries.log'),
        },
        'api_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': logs_file_size * 1024 * 1024,
            'backupCount': logs_file_backup_count,
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'api.log'),
        },
        'celery_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': logs_file_size * 1024 * 1024,
            'backupCount': logs_file_backup_count,
            'filename': os.path.join(LOGS_DIR, 'celery.log'),
            'formatter': 'verbose',
        },
        'debug_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': logs_file_size * 1024 * 1024,
            'backupCount': logs_file_backup_count,
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'debug.log'),
        },
        'warning_handler': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': logs_file_size * 1024 * 1024,
            'backupCount': logs_file_backup_count,
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'warning.log'),
        },
        'error_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': logs_file_size * 1024 * 1024,
            'backupCount': logs_file_backup_count,
            'formatter': 'verbose',
            'filename': os.path.join(LOGS_DIR, 'error.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['debug_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'api': {
            'handlers': ['api_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['warning_handler', 'error_handler'],
            'level': 'WARNING',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['sql_queries_tracking_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['celery_file', 'console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
