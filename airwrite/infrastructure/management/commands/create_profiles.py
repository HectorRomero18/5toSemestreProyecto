from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from airwrite.infrastructure.models import PerfilUsuario

User = get_user_model()

class Command(BaseCommand):
    help = 'Create PerfilUsuario for users who don\'t have one'

    def handle(self, *args, **options):
        users_without_profile = User.objects.filter(perfilusuario__isnull=True)
        created_count = 0

        for user in users_without_profile:
            PerfilUsuario.objects.create(
                user=user,
                nombre=user.username,  # Use username as default name
                xp=0,
                nivel=1
            )
            created_count += 1
            self.stdout.write(f'Created profile for user: {user.username}')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} user profiles'))