from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Creates admin users for Oliveoshoppe'

    def handle(self, *args, **options):
        admins = [
            {
                'username': 'admin',
                'email': 'admin@oliveoshoppe.com',
                'password': 'Admin@2025'
            },
            {
                'username': 'gordon_admin',
                'email': '202210491@gordoncollege.edu.ph',
                'password': 'pagdilaoOO10491'
            },
            {
                'username': 'testing_admin',
                'email': 'oliveoshoppe.testing@gmail.com',
                'password': 'pagdilaoOO10491'
            }
        ]
        
        for admin_data in admins:
            username = admin_data['username']
            email = admin_data['email']
            password = admin_data['password']
            
            if not User.objects.filter(email=email).exists():
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(
                    f'✓ Admin user "{username}" created ({email})'
                ))
            else:
                # Update password if user exists
                user = User.objects.get(email=email)
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.WARNING(
                    f'! Admin user "{username}" already exists - password updated'
                ))
