from __future__ import absolute_import, unicode_literals
import os
import ssl
from celery import Celery

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Event_Tracker.settings')

app = Celery('Event_Tracker')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Celery settings
app.conf.broker_url = os.getenv('REDIS_URL')
app.conf.result_backend = os.getenv('REDIS_URL')

# Add SSL options
app.conf.broker_transport_options = {
    'ssl_cert_reqs': ssl.CERT_REQUIRED,
    # Optional: Specify the path to your CA certificate if needed
    # 'ssl_ca_certs': '/path/to/ca-certificates.crt',
}

app.conf.result_transport_options = {
    'ssl_cert_reqs': ssl.CERT_REQUIRED,
    # Optional: Specify the path to your CA certificate if needed
    # 'ssl_ca_certs': '/path/to/ca-certificates.crt',
}