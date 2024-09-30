import sys

if 'celery' in sys.modules:
    from .celery import app as celery_app
    __all__ = ('celery_app',)
else:
    celery_app = None