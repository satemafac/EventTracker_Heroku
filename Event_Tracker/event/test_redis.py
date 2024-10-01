# event/management/commands/test_redis.py

from django.core.management.base import BaseCommand
import redis
from django.conf import settings

class Command(BaseCommand):
    help = 'Test connection to Redis'

    def handle(self, *args, **kwargs):
        redis_url = settings.CELERY_BROKER_URL
        self.stdout.write(f'Connecting to Redis at {redis_url}')

        try:
            client = redis.StrictRedis.from_url(redis_url)
            client.ping()
            self.stdout.write(self.style.SUCCESS('Successfully connected to Redis!'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Failed to connect to Redis: {e}'))