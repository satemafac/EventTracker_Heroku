# test_redis_ssl.py

from django.core.management.base import BaseCommand
import os
import redis

class Command(BaseCommand):
    help = 'Test Redis SSL connection'

    def handle(self, *args, **options):
        REDIS_TLS_URL = os.getenv('REDIS_TLS_URL')
        try:
            # No need for explicit ssl=True as it's handled via URL
            r = redis.from_url(
                REDIS_TLS_URL,
                ssl_cert_reqs=None  # Optional: Remove if default SSL checks work
            )
            r.ping()
            self.stdout.write(self.style.SUCCESS('Successfully connected to Redis with SSL.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Redis: {e}'))