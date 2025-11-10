from django.views.generic import TemplateView
from django.shortcuts import render
from .views import *


@access_required(roles=['ADMIN', 'AGENT', 'ETUDIANT', 'PARENT'])
class ParentBaseView(BaseContextView, TemplateView):
    """Classe de base pour toutes les vues Étudiant."""
    
    template_name = 'Utilisateur/Parent/default.html'  # template par défaut
    view_name = ""
    page = ""
    bouton = ""
    titre_page = ""
    path = ""
    breadcrumb = []
    message = ""

    # Mapping pour automatiser template et libellé
    view_mapping = {
        'tableau_de_bord_parent': {
            'template': 'Utilisateur/Parent/tableau_de_bord_parent.html',
            'label': 'Tableau de Bord Parent',
            'model_type': 'tableau_bord_parent'
        },
        'profil_parent': {
            'template': 'Utilisateur/Parent/profil_parent.html',
            'label': 'Profil Parent',
            'model_type': 'profil_parent'
        },
        'enfants_parent': {
            'template': 'Utilisateur/Parent/enfants.html',
            'label': 'Enfants Parent',
            'model_type': 'enfants_parent'
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
            return render(request, 'Utilisateur/Parent/error.html', {
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

class TableauBordParentView(ParentBaseView):
    view_name = 'tableau_de_bord_parent'
    

class ProfilParentView(UtilisateurDetailView):
    model_type = 'parent'
    view_name = 'utilisateur_detail'
    context_object_name = 'agent'
    template_detail = 'Utilisateur/Parent/profil_parent.html'

    def get_object(self, queryset=None):
        """
        Retourne l'étudiant lié à l'utilisateur connecté.
        """
        model = self.get_model_class()
        utilisateur = self.request.user  # user connecté
        
        # Si ton modèle Etudiant possède un champ OneToOne vers Utilisateur :
        return model.objects.get(utilisateur=utilisateur)

class EnfantsParentView(ParentBaseView):
    view_name = 'enfants_parent'
    

class EnfantDetailView(TemplateView):
    template_name = "Utilisateur/Parent/enfants.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        enfant = get_object_or_404(Etudiant, utilisateur__pk=self.kwargs["pk"])
        context["enfant"] = enfant
        context["active_view"] = self.request.GET.get("view", "profil")
        return context
