# celery.py

import os
from celery import Celery

# Set the default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Tracker.settings')

app = Celery('Event_Tracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Retrieve Redis URL from environment
CELERY_BROKER_URL = os.getenv('REDIS_URL')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL')

# Optional: Address Celery deprecation warning
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Update Celery configuration
app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    broker_use_ssl=None,  # Remove SSL config if not using TLS
    redis_backend_use_ssl=None,  # Remove SSL config if not using TLS
    task_default_queue='celery',
    task_track_started=True,
)