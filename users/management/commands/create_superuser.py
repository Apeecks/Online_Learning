from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = "Create superuser"

    def handle(self, *args, **options):
        User = get_user_model()

        email = "admin@example.com"
        password = "Admin12345"

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser {email} уже существует")
            )
            return

        user = User.objects.create(
            email=email,
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password(password)
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Superuser {email} создан"))
