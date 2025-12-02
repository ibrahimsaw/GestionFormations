import os
import django
from django.apps import apps

# Initialiser Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PrGestionFormation.settings')
django.setup()

# Actions par défaut
ACTIONS = ['view', 'add', 'change', 'delete']

# Dictionnaire final
PERMISSIONS_DISPONIBLES = {}

# Parcours de toutes les apps installées
for app_config in apps.get_app_configs():
    # Ignore les apps de Django (optionnel)
    if app_config.name.startswith('django.'):
        continue
    
    for model in app_config.get_models():
        modele_nom = model.__name__.lower()  # nom du modèle en minuscule
        PERMISSIONS_DISPONIBLES[modele_nom] = {action: f"{action.capitalize()} {modele_nom}" for action in ACTIONS}

# Affichage
import pprint
pprint.pprint(PERMISSIONS_DISPONIBLES)
