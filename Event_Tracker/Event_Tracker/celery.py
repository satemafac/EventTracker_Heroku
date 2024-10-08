from __future__ import absolute_import, unicode_literals
import os
import ssl
from celery import Celery
from django.conf import settings


# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Tracker.settings')

app = Celery('Event_Tracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()