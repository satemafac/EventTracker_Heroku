# test_redis_ssl.py

from django.core.management.base import BaseCommand
import os
import redis
import ssl

class Command(BaseCommand):
    help = 'Test Redis SSL connection'

    def handle(self, *args, **options):
        REDIS_TLS_URL = os.getenv('REDIS_TLS_URL')
        try:
            r = redis.from_url(
                REDIS_TLS_URL,
                ssl=True,
                ssl_cert_reqs=ssl.CERT_REQUIRED,
                ssl_ca_certs='/etc/ssl/certs/ca-certificates.crt',
            )
            r.ping()
            self.stdout.write(self.style.SUCCESS('Successfully connected to Redis with SSL.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to connect to Redis: {e}'))