from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates a superuser admin account if it does not exist'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@oliveoshoppe.com'
        password = 'Admin@2025'
        
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
            self.stdout.write(self.style.SUCCESS(f'Login with username: {username}, password: {password}'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser "{username}" already exists.'))
