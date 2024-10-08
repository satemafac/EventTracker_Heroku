from __future__ import absolute_import, unicode_literals
import os
import ssl
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Tracker.settings')

app = Celery('Event_Tracker')

# Using a string here means the worker doesn't need to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Configure Celery to use Redis over SSL
BROKER_URL = os.getenv('REDIS_TLS_URL')
CELERY_BROKER_URL = BROKER_URL
CELERY_RESULT_BACKEND = BROKER_URL

# SSL configuration
BROKER_USE_SSL = {
    'ssl_cert_reqs': ssl.CERT_NONE  # Change to ssl.CERT_REQUIRED if you need strict SSL
}

# Optional: specify Celery result and task serialization
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'