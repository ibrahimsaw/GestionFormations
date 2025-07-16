from django.views.generic.base import ContextMixin
from django.views.generic import TemplateView
from datetime import datetime

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
    # {
    #     "ul": "Paramètres système", "bouton": "false", "role": "Administrateur",
    #     "liste": [
    #         {"name": "Configuration générale", "url": "configuration_generale"},
    #         {"name": "Gestion des rôles", "url": "gestion_roles"}
    #     ]
    # },
    # {
    #     "ul": "Rapports", "bouton": "false", "role": "Administrateur",
    #     "liste": [
    #         {"name": "Activité système", "url": "activite_systeme"},
    #         {"name": "Connexions utilisateurs", "url": "connexions_utilisateurs"},
    #         {"name": "Sauvegardes", "url": "sauvegardes"}
    #     ]
    # },
    {
        "ul": "Audit de sécurité", "bouton": "true", "role": "Administrateur",
        "url": "utilisateur:parent"
    },
    {
        "ul": "Audit de sécurité", "bouton": "true", "role": "Administrateur",
        "url": "utilisateur:etudiant"
    },
    # {
    #     "ul": "Maintenance", "bouton": "true", "role": "Administrateur",
    #     "url": "formation:maintenance"
    # },
    # {
    #     "ul": "Support technique", "bouton": "true", "role": "Administrateur",
    #     "url": "support_technique"
    # },
    #
    # # 2. Agent Administratif 📋
    # {
    #     "ul": "Accueil", "bouton": "true", "role": "Agent Administratif",
    #     "url": "accueil_agent"
    # },
    # {
    #     "ul": "Gestion des inscriptions", "bouton": "true", "role": "Agent Administratif",
    #     "url": "gestion_inscriptions"
    # },
    # {
    #     "ul": "Emplois du temps", "bouton": "true", "role": "Agent Administratif",
    #     "url": "emplois_du_temps"
    # },
    # {
    #     "ul": "Ressources pédagogiques", "bouton": "true", "role": "Agent Administratif",
    #     "url": "ressources_pedagogiques"
    # },
    # {
    #     "ul": "Communication", "bouton": "false", "role": "Agent Administratif",
    #     "liste": [
    #         {"name": "Envoi d'annonces", "url": "envoi_annonces"},
    #         {"name": "Messagerie interne", "url": "messagerie_interne"}
    #     ]
    # },
    # {
    #     "ul": "Documents administratifs", "bouton": "true", "role": "Agent Administratif",
    #     "url": "documents_administratifs"
    # },
    # {
    #     "ul": "Archivage", "bouton": "true", "role": "Agent Administratif",
    #     "url": "archivage"
    # },
    # {
    #     "ul": "Statistiques", "bouton": "true", "role": "Agent Administratif",
    #     "url": "statistiques"
    # },
    #
    # # 3. Enseignant 👨‍🏫
    # {
    #     "ul": "Cours", "bouton": "false", "role": "Enseignant",
    #     "liste": [
    #         {"name": "Planning", "url": "planning_enseignant"},
    #         {"name": "Matières enseignées", "url": "matieres_enseignees"},
    #         {"name": "Documents pédagogiques", "url": "documents_pedagogiques"}
    #     ]
    # },
    # {
    #     "ul": "Évaluation", "bouton": "false", "role": "Enseignant",
    #     "liste": [
    #         {"name": "Saisie des notes", "url": "saisie_notes"},
    #         {"name": "Bulletins", "url": "bulletins_enseignant"}
    #     ]
    # },
    # {
    #     "ul": "Élèves", "bouton": "false", "role": "Enseignant",
    #     "liste": [
    #         {"name": "Liste des classes", "url": "liste_classes"},
    #         {"name": "Suivi individuel", "url": "suivi_individuel"}
    #     ]
    # },
    # {
    #     "ul": "Ressources partagées", "bouton": "true", "role": "Enseignant",
    #     "url": "ressources_partagees"
    # },
    # {
    #     "ul": "Forum pédagogique", "bouton": "true", "role": "Enseignant",
    #     "url": "forum_pedagogique"
    # },
    # {
    #     "ul": "Paramètres de notification", "bouton": "true", "role": "Enseignant",
    #     "url": "parametres_notification"
    # },
    #
    # # 4. Étudiant 🎒
    # {
    #     "ul": "Mes cours", "bouton": "false", "role": "Étudiant",
    #     "liste": [
    #         {"name": "Emploi du temps", "url": "emploi_du_temps_etudiant"},
    #         {"name": "Documents de cours", "url": "documents_cours"}
    #     ]
    # },
    # {
    #     "ul": "Notes", "bouton": "false", "role": "Étudiant",
    #     "liste": [
    #         {"name": "Résultats par matière", "url": "resultats_matiere"},
    #         {"name": "Historique", "url": "historique_notes"}
    #     ]
    # },
    # {
    #     "ul": "Ressources", "bouton": "false", "role": "Étudiant",
    #     "liste": [
    #         {"name": "Bibliothèque numérique", "url": "bibliotheque_numerique"},
    #         {"name": "Travaux à rendre", "url": "travaux_a_rendre"}
    #     ]
    # },
    # {
    #     "ul": "Messagerie", "bouton": "true", "role": "Étudiant",
    #     "url": "messagerie_etudiant"
    # },
    # {
    #     "ul": "Événements", "bouton": "true", "role": "Étudiant",
    #     "url": "evenements_etudiant"
    # },
    # {
    #     "ul": "Paramètres de compte", "bouton": "true", "role": "Étudiant",
    #     "url": "parametres_compte_etudiant"
    # },
    #
    # # 5. Parent 👪
    # {
    #     "ul": "Suivi scolaire", "bouton": "false", "role": "Parent",
    #     "liste": [
    #         {"name": "Résultats de mon enfant", "url": "resultats_enfant"},
    #         {"name": "Absences/Retards", "url": "absences_retards"}
    #     ]
    # },
    # {
    #     "ul": "Communication", "bouton": "false", "role": "Parent",
    #     "liste": [
    #         {"name": "Avec les enseignants", "url": "communication_enseignants"},
    #         {"name": "Annonces de l'établissement", "url": "annonces_etablissement"}
    #     ]
    # },
    # {
    #     "ul": "Documents officiels", "bouton": "false", "role": "Parent",
    #     "liste": [
    #         {"name": "Certificats scolaires", "url": "certificats_scolaires"},
    #         {"name": "Factures", "url": "factures_parent"}
    #     ]
    # },
    # {
    #     "ul": "Calendrier scolaire", "bouton": "true", "role": "Parent",
    #     "url": "calendrier_scolaire"
    # },
    # {
    #     "ul": "Alertes", "bouton": "true", "role": "Parent",
    #     "url": "alertes_parent"
    # },
    # {
    #     "ul": "Paramètres", "bouton": "true", "role": "Parent",
    #     "url": "parametres_parent"
    # },
    #
    # # Menu commun à tous les rôles
    # {
    #     "ul": "Profil utilisateur", "bouton": "true", "role": "Commun",
    #     "url": "profil_utilisateur"
    # },
    # {
    #     "ul": "Aide", "bouton": "true", "role": "Commun",
    #     "url": "aide"
    # },
    # {
    #     "ul": "Déconnexion", "bouton": "true", "role": "Commun",
    #     "url": "deconnexion"
    # }
]

data = {
    "nom":"Scholar",
    "navbar":navbar,
    "title":"title",
}

from datetime import datetime
from django.views.generic.base import ContextMixin

class BaseContextView(ContextMixin):
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

        return {
            "user": user,
            "data": data,
            "date": datetime.now()
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_base_context())
        return context
