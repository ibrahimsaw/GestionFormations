navbar = [
    # 1. Administrateur Système 🛠️
    {
        "ul": "Tableau de bord", "bouton": "true", "role": "Administrateur",
        "url": "utilisateur:tableau_de_bord_admin"
    },
    {
        "ul": "Gestion des utilisateurs", "bouton": "false", "role": "Administrateur",
        "liste": [
            {"name": "Création de comptes", "url": "utilisateur:utilisateur_create"},
            {"name": "Liste des utilisateurs", "url": "utilisateur:utilisateur_list"},
            {"name": "Droits d'accès", "url": "Permissions_Manager:permission"}
        ]
    },
    {
        "ul": "Gestion des Formation", "bouton": "false", "role": "Administrateur",
        "liste": [
            {"name": "Création de Formation", "url": "formation:universal-create"},
            {"name": "Liste des Formation", "url": "formation:universal-list"},
        ]
    },
    {
        "ul": "Scolarité", "bouton": "false", "role": "Administrateur",
        "liste": [
            {"name": "Création de Scolarité", "url": "finance:scolarite-create"},
            {"name": "Liste des Scolarités", "url": "finance:scolarite-list"},
        ]
    },
    {
        "ul": "Audit de sécurité", "bouton": "true", "role": "Administrateur",
        "url": "utilisateur:parent"
    },
    {
        "ul": "Etudiant", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:etudiant"
    },
    {
        "ul": "Etudiant 2", "bouton": "true", "role": "Etudiant2",
        "url": "utilisateur:etudiantS"
    },
    {
        "ul": "Cv 1", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:cv"
    },
    {
        "ul": "CV 2", "bouton": "true", "role": "Etudiant2",
        "url": "utilisateur:cvv"
    },
]

navbarEtudiant = [
    {
        "ul": "Liste des utilisateurs", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:utilisateur_list",
        "icon": "bx bx-group"
    },
    {
        "ul": "Tableau de bord", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:tableau_de_bord_etudiant",
        "icon": "bx bx-home me-2"
    },
    {
        "ul": "Calendrier", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:calendrier_etudiant",
        "icon": "bx bx-calendar me-2"
    },
    {
        "ul": "Profil", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:profil_etudiant",
        "icon": "bx bx-user me-2"
    },
    {
        "ul": "Notes", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:notes_etudiant",
        "icon": "bx bx-line-chart me-2"
    },
    {
        "ul": "Cours", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:cours_etudiant",
        "icon": "bx bx-book me-2"
    },
    {
        "ul": "Documents", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:documents_etudiant",
        "icon": "bx bx-file me-2"
    },
    {
        "ul": "Assiduité ", "bouton": "true", "role": "Etudiant",
        "url": "utilisateur:assiduite_etudiant",
        "icon": "bx bx-calendar-check me-2"
    },
    ]

navbarParent = [
    {
        "ul": "Liste des utilisateurs", "bouton": "true", "role": "Parent",
        "url": "utilisateur:utilisateur_list",
        "icon": "bx bx-group"
    },
    {
        "ul": "Tableau de bord", "bouton": "true", "role": "Parent",
        "url": "utilisateur:tableau_de_bord_parent",
        "icon": "bx bx-home me-2"
    },
    {
        "ul": "Profil", "bouton": "true", "role": "Parent",
        "url": "utilisateur:profil_parent",
        "icon": "bx bx-user me-2"
    },
    {
        "ul": "Enfants", "bouton": "true", "role": "Parent",
        "url": "utilisateur:enfants_parent",
        "icon": "bx bx-group me-2"
    },
    ]
navbarAdmin = [
    {
        "ul": "Tableau de bord", "bouton": "true", "role": "Administrateur",
        "url": "utilisateur:bienvenu"
    },
    {
        "ul": "Liste des utilisateurs", "bouton": "true", "role": "Parent",
        "url": "utilisateur:utilisateur_list",
        "icon": "bx bx-group"
    },
    ]
navbarAgent = [
    {
        "ul": "Tableau de bord", "bouton": "true", "role": "Agent Administratif",
        "url": "utilisateur:bienvenu"
    },
    ]
navbarEnseignant = [
    {
        "ul": "Tableau de bord", "bouton": "true", "role": "Enseignant",
        "url": "utilisateur:bienvenu"
    },
    ]

data = {
    "nom":"Scholar",
    "navbar":navbar,
    "title":"title",
}

import contextlib
from datetime import datetime

from django.views.generic.base import ContextMixin


class BaseContextView(ContextMixin):
    def __init__(self):
        self.request = None

    def get_base_context(self):
        user = self.request.user
        message = ""
        if user.is_authenticated:
            message += f"Utilisateur connecté : {user.id} -- "
            message += f"Rôle de l'utilisateur : {user.role} -- "

            if user.role == "ADMIN":
                message += f"Superutilisateur : {user.is_superuser} -- "

            message += f"Membre du personnel : {user.is_staff} -- "
            message += f"Compte actif : {user.is_active} -- "
        else:
            message = "Aucun utilisateur connecté."

        print(message)

        # Choisir le navbar selon le rôle
        role_navbars = {
            "ADMIN": navbarAdmin,
            "AGENT": navbarAgent,
            "ENSEIGNANT": navbarEnseignant,
            "ETUDIANT": navbarEtudiant,
            "PARENT": navbarParent,
        }
        navbar_for_user = role_navbars.get(getattr(user, 'role', None), [])

        # Ajout du nom de la vue courante pour l'activation du menu
        current_url_name = None
        with contextlib.suppress(Exception):
             if hasattr(self.request, 'resolver_match') and self.request.resolver_match:
                 current_url_name = self.request.resolver_match.url_name

        # Construire le JSON dynamique
        data_dynamic = {
            "nom": "Scholar",
            "navbar": navbar_for_user,
            "title": "Bienvenue",
        }

        return {
            "user": user,
            "data": data_dynamic,
            "date": datetime.now(),
            "current_url_name": current_url_name
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_base_context())
        return context

