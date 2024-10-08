from __future__ import absolute_import, unicode_literals
import os
import ssl
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Tracker.settings')

app = Celery('Event_Tracker')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Redis URLs for both the broker and backend
CELERY_BROKER_URL = os.getenv('REDIS_TLS_URL')
CELERY_RESULT_BACKEND = os.getenv('REDIS_TLS_URL')

# Celery SSL configuration for both broker and backend
ssl_config = {
    'ssl_cert_reqs': ssl.CERT_NONE  # Change to ssl.CERT_REQUIRED if you need strict SSL checks
}

app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    broker_use_ssl=ssl_config,
    redis_backend_use_ssl=ssl_config,  # This ensures the backend also uses SSL settings
)

# Auto-discover tasks from all registered Django app configs
app.conf.task_default_queue = 'celery'
app.autodiscover_tasks()