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




def get_group_permission_count(user):
    return Permission.objects.filter(group__user=user).distinct().count()



class GestionPermissionsView(BaseContextView,LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue basée sur une classe pour la gestion des permissions
    """
    permission_required = 'utilisateur.view_utilisateur'
    template_name = 'Permissions_Manager/dashboard.html'
    model_type = None
    view_name = ""
    message = ""
    page = ""
    bouton = ""
    titre_page = ""
    path = ""
    breadcrumb = []

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
        self.message = getattr(self, 'message', '')
        self.view_name = request.resolver_match.view_name.split(':')[-1]
        self.model_type = kwargs.get('type')

        titre_mapping = {
            'tableau_bord': "Tableau de bord",
            'users': "Gestionnaire d'utilisateur",
            'permissions': "Gestion des Permissions",
            'fonction': "Gestion des Fonctions"
        }

        self.titre_page = titre_mapping.get(self.model_type)
        self.message += f"[dispatch] View name: {self.view_name}\n"
        self.message += f"[dispatch] Type reçu : {self.model_type}\n"
        role = self.model_type
        self.path = request.path
        path = request.path.strip('/').split('/')
        cumulative_path = ''
        self.breadcrumb = []
        for i, part in enumerate(path):
            cumulative_path += '/' + part
            print('name :', part.capitalize())
            print('url :', cumulative_path)
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

        # type_name = self.get_type_name()
        # suffix = 'es' if type_name.endswith('t') else 's'

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Prépare le contexte pour le template"""
        context = super().get_context_data(**kwargs)  # Toujours hériter en premier

        # Debug : affichage du type de modèle
        self.model_type = self.kwargs.get('type')
        print(f"[get_context_data] model_type: {self.model_type}")

        # Chargement des données de base
        context.update(self.get_querysets())

        # Contexte statique ou provenant d'attributs d'instance
        context.update({
            'bouton': getattr(self, 'bouton', None),
            'path': getattr(self, 'path', None),
            'titre_page': self.titre_page,
            # 'role_utilisateur': type_name,  # Assure-toi que `type_name` est défini globalement
            'model_type': self.model_type,
            'navbar': globals().get('navbar', None),  # Précaution si 'navbar' n’est pas défini
            'page': getattr(self, 'page', None),
            'message_debug': getattr(self, 'message', ''),
            'breadcrumb': getattr(self, 'breadcrumb', []),
            'active_tab': self.request.GET.get('tab', 'dashboard'),
            'page_title': 'Gestion des Permissions',
        })

        # Calcul des permissions par utilisateur
        users_by_role = context.get('users_by_role', {})
        permission_counts = {
            user.id: Permission.objects.filter(group__user=user).distinct().count()
            for users in users_by_role.values()
            for user in users
        }

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






class GererPermissionsUtilisateurView(BaseContextView, LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue pour gérer les permissions d'un utilisateur spécifique
    """
    permission_required = 'utilisateur.change_utilisateur'
    template_name = 'Permissions_Manager/gerer_utilisateur.html'
    form_class = UserRolePermissionForm

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
            'active_tab': kwargs.get('active_tab', 'users')
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











class GererFonctionView(BaseContextView,LoginRequiredMixin, PermissionRequiredMixin, View):
    """
    Vue pour créer ou modifier une fonction d'agent
    """
    permission_required = 'auth.change_permission'
    template_name = 'Permissions_Manager/gerer_fonction.html'
    form_class = AssignFonctionForm

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
        print("[get_context_data] Contexte envoyé :")
        for key, value in context.items():
            print(f"    {key}: {value}")
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



# class CreerPermissionView(BaseContextView,LoginRequiredMixin, PermissionRequiredMixin, View):
#     """
#     Vue pour créer ou modifier une permission
#     """
#     permission_required = 'auth.add_permission'
#     template_name = 'Permissions_Manager/creer_permission.html'
#     form_class = CustomPermissionForm
#
#     def get_permission(self, permission_id):
#         if permission_id:
#             return get_object_or_404(
#                 Permission.objects.select_related('content_type', 'meta'),
#                 pk=permission_id
#             )
#         return None
#
#     def get_initial(self, permission):
#         if not permission:
#             return {}
#
#         try:
#             meta = permission.meta
#             return {
#                 'description': meta.description,
#                 'roles_autorises': meta.roles_autorises.split(',')
#             }
#         except AttributeError:
#             return {}
#
#     def get(self, request, permission_id=None, *args, **kwargs):
#         permission = self.get_permission(permission_id)
#         form = self.form_class(instance=permission, initial=self.get_initial(permission))
#         context = {
#             'form': form,
#             'editing': permission is not None
#         }
#         context.update(super().get_context_data(**kwargs))
#         print("[get_context_data] Contexte envoyé :")
#         for key, value in context.items():
#             print(f"    {key}: {value}")
#         return render(request, self.template_name, context)
#
#
#     def post(self, request, permission_id=None, *args, **kwargs):
#         permission = self.get_permission(permission_id)
#         form = self.form_class(request.POST, instance=permission)
#
#         if form.is_valid():
#             try:
#                 form.save()
#                 messages.success(request, "Permission enregistrée avec succès")
#                 return redirect('Permissions_Manager:dashboard')
#             except Exception as e:
#                 messages.error(request, f"Erreur: {str(e)}")
#         else:
#             messages.error(request, "Veuillez corriger les erreurs")
#
#         return render(request, self.template_name, {
#             'form': form,
#             'editing': permission is not None
#         })


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


# class ModifierPermissionView(BaseContextView,LoginRequiredMixin, PermissionRequiredMixin, View):
#     """
#     Vue pour modifier une permission existante
#     """
#     permission_required = 'auth.change_permission'
#     template_name = 'Permissions_Manager/detail_permission.html'
#     form_class = CustomPermissionForm
#
#     def get_permission(self, permission_id):
#         return get_object_or_404(
#             Permission.objects.select_related('content_type', 'meta'),
#             pk=permission_id
#         )
#
#     def get_initial(self, permission):
#         try:
#             meta = permission.meta
#             return {
#                 'description': meta.description,
#                 'roles_autorises': meta.roles_autorises.split(',')
#             }
#         except AttributeError:
#             return {}
#
#     def get(self, request, permission_id, *args, **kwargs):
#         permission = self.get_permission(permission_id)
#         form = self.form_class(instance=permission, initial=self.get_initial(permission))
#         context = {
#             'form': form,
#             'permission': permission,
#             'active_tab': 'permissions'
#         }
#         context.update(super().get_context_data(**kwargs))
#         print("[get_context_data] Contexte envoyé :")
#         for key, value in context.items():
#             print(f"    {key}: {value}")
#         return render(request, self.template_name, context)
#
#     def post(self, request, permission_id, *args, **kwargs):
#         permission = self.get_permission(permission_id)
#         form = self.form_class(request.POST, instance=permission)
#
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Permission mise à jour avec succès")
#             return redirect('Permissions_Manager:dashboard')
#
#         return render(request, self.template_name, {
#             'form': form,
#             'permission': permission,
#             'active_tab': 'permissions'
#         })

class DetailPermissionView(BaseContextView, LoginRequiredMixin, PermissionRequiredMixin, View):
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

    def get(self, request, permission_id, *args, **kwargs):
        permission = self.get_permission(permission_id)
        form = self.form_class(instance=permission)

        # Pré-remplir les rôles si MetaPermission existe
        if hasattr(permission, 'meta'):
            form.initial['roles_autorises'] = permission.meta.roles_autorises.split(',')

        context = {
            'form': form,
            'permission': permission,
            'active_tab': 'permissions'
        }
        context.update(super().get_context_data(**kwargs))

        return render(request, self.template_name, context)