from django.views.generic import TemplateView
from django.shortcuts import render
from .views import *

class EtudiantBaseView(BaseContextView, TemplateView):
    """Classe de base pour toutes les vues Étudiant."""
    
    template_name = 'Utilisateur/Etudiant/default.html'  # template par défaut
    view_name = ""
    page = ""
    bouton = ""
    titre_page = ""
    path = ""
    breadcrumb = []
    message = ""

    # Mapping pour automatiser template et libellé
    view_mapping = {
        'tableau_de_bord_etudiant': {
            'template': 'Utilisateur/Etudiant/tableau_de_bord_etudiant.html',
            'label': 'Tableau de Bord Étudiant',
            'model_type': 'tableau_bord_etudiant'
        },
        'profil_etudiant': {
            'template': 'Utilisateur/Etudiant/profil_etudiant.html',
            'label': 'Profil Étudiant',
            'model_type': 'profil_etudiant'
        },
        'calendrier_etudiant': {
            'template': 'Utilisateur/Etudiant/calendrier_etudiant.html',
            'label': 'Calendrier Étudiant',
            'model_type': 'calendrier_etudiant'
        },
        'notes_etudiant': {
            'template': 'Utilisateur/Etudiant/notes_etudiant.html',
            'label': 'Notes Étudiant',
            'model_type': 'notes_etudiant'
        },
        'cours_etudiant': {
            'template': 'Utilisateur/Etudiant/cours_etudiant.html',
            'label': 'Cours Étudiant',
            'model_type': 'cours_etudiant'
        },
        'documents_etudiant': {
            'template': 'Utilisateur/Etudiant/documents_etudiant.html',
            'label': 'Documents Étudiant',
            'model_type': 'documents_etudiant'
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

        self.message += f"[dispatch] Template sélectionné : {self.template_name}\n"
        self.message += f"[dispatch] Model type : {self.model_type}\n"

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'donne': self.page,
            'model_type': self.model_type,
            'breadcrumb': self.breadcrumb,
            'page': self.page,
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

class ProfilEtudiantView(EtudiantBaseView):
    view_name = 'profil'

class CalendrierEtudiantView(EtudiantBaseView):
    view_name = 'calendrier'

class NotesEtudiantView(EtudiantBaseView):
    view_name = 'notes'

class CoursEtudiantView(EtudiantBaseView):
    view_name = 'cours'

class DocumentsEtudiantView(EtudiantBaseView):
    view_name = 'documents'
