# Utilisateur/management/commands/createsuperuser_custom.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from Utilisateur.models import Role


class Command(BaseCommand):
    help = 'Crée un superutilisateur avec un rôle par code'

    def handle(self, *args, **options):
        User = get_user_model()
        matricule = input("Matricule: ")
        role_code = input("Role (code): ")

        try:
            role = Role.objects.get(code=role_code)
        except Role.DoesNotExist:
            self.stderr.write(f"Le rôle avec code '{role_code}' n'existe pas")
            return

        password = input("Password: ")
        User.objects.create_superuser(matricule=matricule, password=password, role=role)
        self.stdout.write(self.style.SUCCESS('Superutilisateur créé avec succès'))