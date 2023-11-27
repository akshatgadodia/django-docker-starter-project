import os
from celery import Celery
from celery.signals import setup_logging
from logging.config import dictConfig
from django.conf import settings

# Set the default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Create a Celery instance and configure it
app = Celery("backend")

# Load Celery configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")


# Define a signal handler to configure logging when Celery starts
@setup_logging.connect
def config_loggers(*args, **kwargs):
    dictConfig(settings.LOGGING)  # Use Django settings for logging configuration


# Auto-discover and register tasks from all installed apps
app.autodiscover_tasks()

