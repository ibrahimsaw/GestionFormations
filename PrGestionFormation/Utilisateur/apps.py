# utilisateur/apps.py
from django.apps import AppConfig


class UtilisateurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Utilisateur'

    def ready(self):
        """
        Méthode exécutée automatiquement au démarrage de Django.
        On initialise :
        - les rôles
        - les fonctions
        - les permissions associées à chaque rôle
        """
        from . import signals  # Assure le chargement des signaux

        try:
            from .models import Role, FonctionAgent, RolePermission

            # Initialisation des rôles de base
            Role.initialiser_roles()

            # Initialisation des fonctions agents
            FonctionAgent.initialiser_fonctions()

            # ✅ Initialisation des permissions par rôle
            RolePermission.init_permissions()

        except Exception:
            # On ignore les erreurs pendant makemigrations / migrate
            pass
