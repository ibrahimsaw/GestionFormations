# utilisateur/management/commands/init_roles.py
from django.core.management.base import BaseCommand
from Utilisateur.models import FonctionAgent, Genre,RolePermission
from Formation.models import TypeFormation, Specification


class Command(BaseCommand):
    help = 'Initialise les rôles, genres, types de formation et spécifications par défaut.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("📦 Début de l'initialisation des données par défaut..."))

        # Liste des tâches à exécuter
        tasks = [
            ("fonctions des agents", FonctionAgent.initialiser_fonctions),
            ("genres", Genre.initialiser_genres),
            ("types de formation", TypeFormation.initialiser_types_par_defaut),
            ("spécifications", Specification.initialiser_specifications_par_defaut),
            ("Permission pas Role", RolePermission.init_permissions),
        ]

        for description, function in tasks:
            try:
                self.stdout.write(f"➤ Initialisation des {description}...")
                count = function()
                self.stdout.write(self.style.SUCCESS(f"   ✔ {count} {description} initialisé(e)s avec succès."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"   ❌ Erreur lors de l'initialisation des {description} : {e}"))

        self.stdout.write(self.style.SUCCESS("✅ Initialisation terminée."))
