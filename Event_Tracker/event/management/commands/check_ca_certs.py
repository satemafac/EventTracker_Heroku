# check_ca_certs.py

from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = 'Check if CA certificates file exists'

    def handle(self, *args, **options):
        ca_certs_path = '/etc/ssl/certs/ca-certificates.crt'
        if os.path.exists(ca_certs_path):
            self.stdout.write(self.style.SUCCESS(f'CA certificates found at {ca_certs_path}'))
        else:
            self.stdout.write(self.style.ERROR(f'CA certificates NOT found at {ca_certs_path}'))