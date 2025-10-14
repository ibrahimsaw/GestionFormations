# utilisateur/apps.py
from django.apps import AppConfig


class UtilisateurConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Utilisateur'

    def ready(self):
        """Méthode exécutée au chargement de l'application"""
        from . import signals
        try:
            from .models import Role, FonctionAgent
            Role.initialiser_roles()
            FonctionAgent.initialiser_fonctions()
        except:
            # Évite les erreurs lors des migrations initiales
            pass