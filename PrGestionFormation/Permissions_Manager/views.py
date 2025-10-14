from django.contrib.auth.decorators import login_required, permission_required
from Permissions_Manager.forms import (
    AssignFonctionForm,
    CustomPermissionForm,
    UserRolePermissionForm
)
from config.globals import *
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import Permission, Group
from django.db.models import Prefetch
from Utilisateur.models import Utilisateur, FonctionAgent, AgentAdministration
from .forms import UserRolePermissionForm, AssignFonctionForm, CustomPermissionForm
from .models import MetaPermission
from django.contrib.contenttypes.models import ContentType
from collections import defaultdict
from django.db.models import Count


def get_group_permission_count(user):
    return Permission.objects.filter(group__user=user).distinct().count()

class GestionPermissionsBaseView(BaseContextView):
    """Classe de base pour toutes les vues utilisateur avec gestion des templates dynamiques."""

    model_type = None
    view_name = None
    template_form = 'Formation/formulaire.html'
    template_list = 'Formation/liste.html'
    template_detail = 'Formation/detail.html'
    # template_delete = 'Formation/confirm_delete.html'
    message = ""
    page = None
    bouton = None
    titre_page = None
    entete = None
    path = None
    breadcrumb = []

    def dispatch(self, request, *args, **kwargs):
        self.message = getattr(self, 'message', '')
        self.view_name = request.resolver_match.view_name.split(':')[-1]
        self.model_type = kwargs.get('type')

        self.message += f"[dispatch] View name: {self.view_name}\n"
        self.message += f"[dispatch] Type reçu : {self.model_type}\n"

        titre_mapping = {
            'tableau_bord': "Tableau de bord Permissions",
            'users': "Gestionnaire d'utilisateur",
            'permissions': "Gestion des Permissions",
            'fonction': "Gestion des Fonctions"
        }

        if self.view_name == "permission":
            self.titre_page = titre_mapping.get(self.model_type)
            self.entete= 'Gestion des Permissions',
        if self.view_name == "gerer_permissions_utilisateur":
            self.titre_page = "Gestion des Permissions de Utilisateur"
            self.entete = 'Permissions',
        if self.view_name == "creer_fonction":
            self.titre_page = "Creation d'une Fonction d'Agent"
            self.entete = "Créer une Fonction d'Agent"
        if self.view_name == "modifier_fonction":
            self.titre_page = "Modification d'une Fonction d'Agent"
            self.entete = "Modifier une Fonction d'Agent"
        if self.view_name == "permission_detail":
            self.titre_page = "Détail d'une permission"
            self.entete = "Détail de la permission"




        role = self.model_type
        self.path = request.path
        path = request.path.strip('/').split('/')
        cumulative_path = ''
        self.breadcrumb = []
        for i,part in enumerate(path):
            cumulative_path += '/' + part
            print('name :', part.capitalize())
            print('url :',cumulative_path)
            self.breadcrumb.append({
            'name': part.capitalize(),
            'url': cumulative_path,
            'is_first': i == 0,
            'is_last': i == len(path) - 1
            })
        print("Chemin de la requête :", request.path)
        print("Méthode HTTP :", request.method)
        print("Nom de la vue :", request.resolver_match.view_name)
        print("Paramètre GET 'name' :", request.GET.get('name'))
        self.message += f"[dispatch] Action détectée : {self.page}\n"
        print(self.message)
        if not request.user.is_staff:  # ou tout autre test de rôle
            return render(request, 'errors/403.html', status=403)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'bouton' : self.bouton,
            'path' : self.path,
            'titre_page' : self.titre_page,
            # 'role_utilisateur': type_name,
            'model_type': self.model_type,
            'navbar': navbar,  # Assure-toi que 'navbar' est bien défini globalement
            'page': self.page,
            'message_debug': self.message,  # Optionnel : pour affichage dans le template
            'breadcrumb': self.breadcrumb,
            'entete': self.entete,
        })
        return context



class GestionPermissionsView(GestionPermissionsBaseView,LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue basée sur une classe pour la gestion des permissions
    """
    permission_required = 'utilisateur.view_utilisateur'
    template_name = 'Permissions_Manager/dashboard.html'


    def get_querysets(self):
        """Retourne tous les querysets nécessaires"""
        # Utilisateurs par rôle
        users_by_role = {
            role_name: Utilisateur.objects.filter(role=role_code)
                .select_related('genre')
                .prefetch_related('groups', 'user_permissions')
            for role_code, role_name in Utilisateur.Role.choices
        }

        # Fonctions avec permissions
        fonctions = FonctionAgent.objects.all().prefetch_related(
            Prefetch('permissions',
                    queryset=Permission.objects.select_related('content_type'),
                    to_attr='permissions_list')
        )
        return {
            'users_by_role': users_by_role,
            'fonctions': fonctions,
            'permissions': Permission.objects.select_related('content_type')
                              .order_by('content_type__app_label', 'codename'),
            'groups': Group.objects.prefetch_related('permissions').all(),
            'content_types': ContentType.objects.all()  # Pour le formulaire de permission
        }

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:  # ou tout autre test de rôle
            return render(request, 'errors/403.html', status=403)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Prépare le contexte pour le template"""
        context = super().get_context_data(**kwargs)  # Toujours hériter en premier


        # Chargement des données de base
        context.update(self.get_querysets())

        # Contexte statique ou provenant d'attributs d'instance
        context.update({
            'active_tab': self.request.GET.get('tab', 'dashboard'),
        })

        # Calcul des permissions par utilisateur
        users_by_role = context.get('users_by_role', {})
        permission_counts = {
            user.id: Permission.objects.filter(group__user=user).distinct().count()
            for users in users_by_role.values()
            for user in users
        }
        models_list = (
            Permission.objects.values_list('content_type__model', flat=True)
            .distinct()
            .order_by('content_type__model')
        )

        context['models_list'] = models_list

        # Ajout des permissions à chaque utilisateur
        for users in users_by_role.values():
            for user in users:
                user.group_permission_count = permission_counts.get(user.id, 0)

        # Debug final : aperçu du contexte
        print("[get_context_data] Contexte final envoyé :")
        for key, value in context.items():
            print(f"    {key}: {value}")

        return context

    def get(self, request, *args, **kwargs):
        """Gère les requêtes GET"""
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        """Gère les requêtes POST"""
        # Logique pour gérer les soumissions de formulaire si nécessaire
        return redirect('dashboard')




class GererPermissionsUtilisateurView(GestionPermissionsBaseView, LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue pour gérer les permissions d'un utilisateur spécifique
    """
    permission_required = 'utilisateur.change_utilisateur'
    template_name = 'Permissions_Manager/gerer_utilisateur.html'
    form_class = UserRolePermissionForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_user(self, user_id):
        return get_object_or_404(
            Utilisateur.objects.select_related('genre')
            .prefetch_related('user_permissions', 'groups__permissions'),
            pk=user_id
        )

    def get_initial(self, user):
        initial = {}
        if hasattr(user, 'agentadministration'):
            initial['fonction_agent'] = user.agentadministration.fonctions.all()  # ✅ Important
        return initial

    def handle_agent_fonction(self, user, form_data):
        fonctions = form_data.get('fonction_agent')  # Doit être un queryset ou une liste de FonctionAgent

        # Récupère ou crée l'AgentAdministration lié à l'utilisateur
        agent_admin, created = AgentAdministration.objects.get_or_create(utilisateur=user)

        if fonctions:
            # Remplace toutes les fonctions assignées par celles sélectionnées
            agent_admin.fonctions.set(fonctions)  # set() remplace l'ancien contenu
        else:
            # Si aucune fonction n'est sélectionnée, on vide le champ ManyToMany
            agent_admin.fonctions.clear()

        agent_admin.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = kwargs.get('user') or self.request.user

        # Définir les permissions par groupe
        permissions_by_group = {
            group.name: group.permissions.all()
            for group in user.groups.all()
        }

        # Ajouter dynamiquement à l'utilisateur
        user.permissions_by_group = permissions_by_group
        context['page_title'] = 'Gestion des Permissions Utilisateur'

        # Mettre à jour le contexte
        fonctions = FonctionAgent.objects.filter(agentadministration__utilisateur=user).prefetch_related('permissions')

        context.update({
            'user': user,
            'form': kwargs.get('form'),
            'fonctions_avec_permissions' : fonctions,
        })
        return context

    def get(self, request, user_id, *args, **kwargs):
        user = self.get_user(user_id)
        form = self.form_class(instance=user, initial=self.get_initial(user))
        context = self.get_context_data(form=form, user=user, active_tab='users')
        return render(request, self.template_name, context)

    def post(self, request, user_id, *args, **kwargs):
        user = self.get_user(user_id)
        form = self.form_class(request.POST, instance=user)

        if form.is_valid():
            form.save()
            if user.role == Utilisateur.Role.AGENT:
                self.handle_agent_fonction(user, form.cleaned_data)

            messages.success(request, f"Permissions mises à jour pour {user.matricule}")
            return redirect('Permissions_Manager:permission')

        context = self.get_context_data(form=form, user=user, active_tab='users')
        return render(request, self.template_name, context)

class GererFonctionView(GestionPermissionsBaseView,LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue pour créer ou modifier une fonction d'agent
    """
    permission_required = 'auth.change_permission'
    template_name = 'Permissions_Manager/gerer_fonction.html'
    form_class = AssignFonctionForm

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_fonction(self, fonction_id):
        if fonction_id:
            return get_object_or_404(
                FonctionAgent.objects.prefetch_related('permissions'),
                pk=fonction_id
            )
        return None

    def get_success_message(self, is_update):
        return "Fonction mise à jour" if is_update else "Fonction créée"

    def get(self, request, fonction_id=None, *args, **kwargs):
        fonction = self.get_fonction(fonction_id)
        form = self.form_class(instance=fonction)
        context = {
            'form': form,
            'fonction': fonction,
            'active_tab': 'fonctions',
        }
        context.update(super().get_context_data(**kwargs))
        return render(request, self.template_name, context)

    def post(self, request, fonction_id=None, *args, **kwargs):
        fonction = self.get_fonction(fonction_id)
        form = self.form_class(request.POST, instance=fonction)

        if form.is_valid():
            form.save()
            messages.success(request, f"{self.get_success_message(fonction_id is not None)} avec succès")
            return redirect('Permissions_Manager:permission')

        return render(request, self.template_name, {
            'form': form,
            'fonction': fonction,
            'active_tab': 'fonctions'
        })


class SupprimerFonctionView(BaseContextView,LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue pour supprimer une fonction d'agent
    """
    permission_required = 'auth.delete_permission'
    template_name = 'Permissions_Manager/confirmer_suppression.html'

    def get_fonction(self, fonction_id):
        return get_object_or_404(FonctionAgent, pk=fonction_id)

    def get(self, request, fonction_id, *args, **kwargs):
        fonction = self.get_fonction(fonction_id)
        context = {
            'objet': fonction,
            'type_objet': 'fonction',
            'back_url': 'Permissions_Manager:dashboard'
        }
        context.update(super().get_context_data(**kwargs))
        print("[get_context_data] Contexte envoyé :")
        for key, value in context.items():
            print(f"    {key}: {value}")
        return render(request, self.template_name, context)

    def post(self, request, fonction_id, *args, **kwargs):
        fonction = self.get_fonction(fonction_id)
        fonction.delete()
        messages.success(request, f"La fonction {fonction.nom} a été supprimée avec succès")
        return redirect('Permissions_Manager:dashboard')


class DetailPermissionView(GestionPermissionsBaseView, LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue pour afficher les détails d'une permission avec formulaire en lecture seule
    """
    permission_required = 'auth.view_permission'
    template_name = 'Permissions_Manager/detail_permission.html'
    form_class = CustomPermissionForm  # Utilisez le formulaire en lecture seule que je vous ai fourni précédemment

    def get_permission(self, permission_id):
        return get_object_or_404(
            Permission.objects.select_related('content_type', 'meta'),
            pk=permission_id
        )

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, permission_id, *args, **kwargs):
        permission = self.get_permission(permission_id)
        form = self.form_class(instance=permission)

        # Pré-remplir les rôles si MetaPermission existe
        if hasattr(permission, 'meta'):
            form.initial['roles_autorises'] = permission.meta.roles_autorises.split(',')

        context = {
            'form': form,
            'permission': permission,
            'active_tab': 'permissions',
        }
        context.update(super().get_context_data(**kwargs))

        return render(request, self.template_name, context)

def historique_utilisateur(request, pk):
    paginate_by = 10
    utilisateur = get_object_or_404(Utilisateur, pk=pk)
    historique = utilisateur.history.all().order_by('-history_date')
    return render(request, 'Permissions_Manager/utilisateur/historique.html', {
        'utilisateur': utilisateur,
        'historique': historique,
        'paginate_by' : 10
    })

from django.apps import apps

def get_all_historical_entries_by_user(user):
    historiques = []
    for model in apps.get_models():
        # On cherche les modèles avec un champ 'history'
        if hasattr(model, 'history'):
            try:
                historiques += list(model.history.filter(history_user=user))
            except Exception:
                pass
    historiques.sort(key=lambda x: x.history_date, reverse=True)
    return historiques

def historique_actions_par_utilisateur(request, utilisateur_pk):
    utilisateur = get_object_or_404(Utilisateur, pk=utilisateur_pk)
    historiques = get_all_historical_entries_by_user(utilisateur)

    for entry in historiques:
        try:
            entry.model_name = entry.instance._meta.verbose_name.title()
        except:
            entry.model_name = "Objet inconnu"

    return render(request, 'Permissions_Manager/utilisateur/historique_actions.html', {
        'utilisateur': utilisateur,
        'historiques': historiques,
    })

from django.views.generic import DetailView
from django.views.generic.list import MultipleObjectMixin
from django.apps import apps
from django.shortcuts import get_object_or_404
from .models import Utilisateur


class HistoriqueUtilisateurView(BaseContextView, DetailView, MultipleObjectMixin):
    model = Utilisateur
    template_name = 'Permissions_Manager/utilisateur/historique_unifie.html'
    context_object_name = 'utilisateur'
    paginate_by = 10

    def get_all_actions_done_by_user(self, user):
        historiques = []

        for model in apps.get_models():
            if hasattr(model, 'history'):
                try:
                    historiques += list(model.history.filter(history_user=user))
                except Exception:
                    pass

        for entry in historiques:
            try:
                entry.model_name = entry.instance._meta.verbose_name.title()
            except Exception:
                entry.model_name = "Objet inconnu"

        return sorted(historiques, key=lambda x: x.history_date, reverse=True)

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        role = self.kwargs.get('type', 'moi')

        # Récupération de l'historique selon le rôle
        if role == 'action':
            historique = self.get_all_actions_done_by_user(self.object)
        else:
            historique = self.object.history.all().order_by('-history_date')
            for entry in historique:
                try:
                    entry.model_name = entry.instance._meta.verbose_name.title()
                except Exception:
                    entry.model_name = "Utilisateur"

        # Ajout de la liste paginée à context
        context = super().get_context_data(object_list=historique, **kwargs)
        context['historiques'] = context['object_list']
        context['role'] = role
        return context

