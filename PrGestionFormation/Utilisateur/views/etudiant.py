from django.views.generic import TemplateView
from django.shortcuts import render
from .views import *


@access_required(roles=['ADMIN', 'AGENT', 'ETUDIANT', 'PARENT'])
class EtudiantBaseView(BaseContextView, TemplateView):
    """Classe de base pour toutes les vues Étudiant."""
    
    template_name = 'Utilisateur/Etudiant/default.html'  # template par défaut
    view_name = ""
    page = ""
    info = ""
    icon = ""
    bouton = ""
    titre_page = ""
    path = ""
    breadcrumb = []
    message = ""

    # Mapping pour automatiser template et libellé
    view_mapping = {
        'tableau_de_bord_etudiant': {
            'template': 'Utilisateur/Etudiant/tableau_de_bord_etudiant.html',
            'label': 'Tableau de Bord',
            'model_type': 'tableau_bord_etudiant',
            'info': 'Aperçu général des informations importantes',
            'icon': 'bx bx-home'
        },
        'profil_etudiant': {
            'template': 'Utilisateur/Etudiant/profil_etudiant.html',
            'label': 'Profil',
            'model_type': 'profil_etudiant',
            'info': 'Informations personnelles de l\'étudiant',
            'icon': 'bx bx-user'
        },
        'calendrier_etudiant': {
            'template': 'Utilisateur/Etudiant/calendrier_etudiant.html',
            'label': 'Calendrier',
            'model_type': 'calendrier_etudiant',
            'info': 'Informations sur les Événements, les Examens et les Devoirs',
            'icon': 'bx bx-calendar'
        },
        'notes_etudiant': {
            'template': 'Utilisateur/Etudiant/notes_etudiant.html',
            'label': 'Notes et Résultats',
            'model_type': 'notes_etudiant',
            'info': 'Informations sur les Notes, les Moyennes et les Résultats',
            'icon': 'bx bx-bar-chart-alt-2'
        },
        'cours_etudiant': {
            'template': 'Utilisateur/Etudiant/cours_etudiant.html',
            'label': 'Mes Cours',
            'model_type': 'cours_etudiant',
            'info': 'Informations sur les modules,leurs Progression et le Prochaine courses',
            'icon': 'bx bx-book'
            
        },
        'documents_etudiant': {
            'template': 'Utilisateur/Etudiant/documents_etudiant.html',
            'label': 'Mes Documents',
            'model_type': 'documents_etudiant',
            'info': 'Informations sur les modules,leurs Progression et le Prochaine courses',
            'icon': 'bx bx-folder-open'
        },
        'assiduite_etudiant': {
            'template': 'Utilisateur/Etudiant/assiduite_etudiant.html',
            'label': 'Assiduité',
            'model_type': 'assiduite_etudiant',
            'info': 'Informations sur les Retards, l\'Absences et les Présences',
            'icon': 'bx bx-check-shield'
        },
    }

    def dispatch(self, request, *args, **kwargs):
        self.message = getattr(self, 'message', '')
        self.view_name = request.resolver_match.view_name.split(':')[-1]

        self.message += f"[dispatch] View name: {self.view_name}\n"

        # Gestion du breadcrumb
        self.path = request.path
        path_parts = self.path.strip('/').split('/')
        cumulative_path = ''
        self.breadcrumb = []
        for i, part in enumerate(path_parts):
            cumulative_path += f'/{part}'
            self.breadcrumb.append({
                'name': part.capitalize(),
                'url': cumulative_path,
                'is_first': i == 0,
                'is_last': i == len(path_parts) - 1
            })

        # Vérification du mapping
        print(self.view_name)
        print(self.view_mapping)
        if self.view_name not in self.view_mapping:
            self.message += "[dispatch] Vue non reconnue, chargement erreur.\n"
            return render(request, 'Utilisateur/Etudiant/error.html', {
                'erreur': "Vue inconnue.",
                'message': self.message,
                'page': self.page,
                'titre_page': self.titre_page,
                'path': self.path,
            })

        # Récupération automatique du template et des infos
        self.template_name = self.view_mapping[self.view_name]['template']
        self.page = self.view_mapping[self.view_name]['label']
        self.titre_page = self.page
        self.model_type = self.view_mapping[self.view_name]['model_type']
        self.info = self.view_mapping[self.view_name]['info']
        self.icon = self.view_mapping[self.view_name]['icon']

        self.message += f"[dispatch] Template sélectionné : {self.template_name}\n"
        self.message += f"[dispatch] Model type : {self.model_type}\n"

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'label': self.page,
            'model_type': self.model_type,
            'breadcrumb': self.breadcrumb,
            'page': self.page,
            'info': self.info,
            'icon': self.icon,
            'titre_page': self.titre_page,
            'path': self.path,
            'message_debug': self.message,
            'navbar': navbar,  # Assure-toi que 'navbar' est bien défini
        })
        return context


# -------------------------
# Vues Étudiant spécifiques
# -------------------------

class TableauBordEtudiantView(EtudiantBaseView):
    view_name = 'tableau_bord'

class ProfilEtudiantView(UtilisateurDetailView):
    model_type = 'etudiant'
    view_name = 'utilisateur_detail'
    context_object_name = 'agent'
    template_detail = 'Utilisateur/Etudiant/profil_etudiant.html'

    def get_object(self, queryset=None):
        """
        Retourne l'étudiant lié à l'utilisateur connecté.
        """
        model = self.get_model_class()
        utilisateur = self.request.user  # user connecté
        
        # Si ton modèle Etudiant possède un champ OneToOne vers Utilisateur :
        return model.objects.get(utilisateur=utilisateur)




class CalendrierEtudiantView(EtudiantBaseView):
    view_name = 'calendrier'

class NotesEtudiantView(EtudiantBaseView):
    view_name = 'notes'

class CoursEtudiantView(EtudiantBaseView):
    view_name = 'cours'

class DocumentsEtudiantView(EtudiantBaseView):
    view_name = 'documents'

class AssiduiteEtudiantView(EtudiantBaseView):
    view_name = 'assiduite'
