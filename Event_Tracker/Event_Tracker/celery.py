from __future__ import absolute_import, unicode_literals
import os
import ssl
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Tracker.settings')

app = Celery('Event_Tracker')

# Using a string here means the worker doesn't need to serialize
# the configuration object to child processes.
# Load configuration from Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Enable Redis as the broker and result backend
CELERY_BROKER_URL = os.getenv('REDIS_TLS_URL')
CELERY_RESULT_BACKEND = os.getenv('REDIS_TLS_URL')

app.conf.update(
    broker_url=CELERY_BROKER_URL,
    result_backend=CELERY_RESULT_BACKEND,
    accept_content=['json'],
    task_serializer='json',
    result_serializer='json',
    timezone='UTC',
    broker_use_ssl={
        'ssl_cert_reqs': ssl.CERT_NONE  # You can adjust to CERT_REQUIRED if needed
    }
)

# Auto-discover tasks from all registered Django app configs
app.autodiscover_tasks()