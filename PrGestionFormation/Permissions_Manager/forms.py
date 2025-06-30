from django import forms
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from Utilisateur.models import Utilisateur, FonctionAgent, AgentAdministration,RolePermission
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _




ROLE_PERMISSIONS_MAPPING = {
    'ADMIN': {
        '*': ['add', 'change', 'delete', 'view']
    },
    'AGENT': {
        'formation': ['add', 'change', 'view'],
        'classe': ['add', 'change', 'view'],
        'utilisateur': ['view']
    },
    'ENSEIGNANT': {
        'cours': ['add', 'change', 'delete', 'view'],
        'evaluation': ['view', 'change'],
        'emploidutemps': ['view']
    },
    'ETUDIANT': {
        'notes': ['view'],
        'emploidutemps': ['view']
    },
    'PARENT': {
        'notes': ['view']
    }
}


class UserRolePermissionForm(forms.ModelForm):
    fonction_agent = forms.ModelMultipleChoiceField(
        queryset=FonctionAgent.objects.all(),
        required=False,
        label="Fonctions administratives",
        help_text="Sélectionnez une ou plusieurs fonctions pour les agents administratifs",
        widget=forms.CheckboxSelectMultiple  # ✅ Widget cases à cocher
    )

    user_permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'permission-checkbox'}),
        required=False,
        label="Permissions"
    )

    class Meta:
        model = Utilisateur
        fields = ['user_permissions', 'groups']
        widgets = {
            'groups': forms.CheckboxSelectMultiple(attrs={'class': 'group-checkbox'}),
        }
        help_texts = {
            'user_permissions': "Sélectionnez les permissions spécifiques pour cet utilisateur",
            'groups': "Sélectionnez les groupes d'appartenance",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        role = self.instance.role
        role_name = role.name if hasattr(role, 'name') else role

        if role_name in ROLE_PERMISSIONS_MAPPING:
            role_perms = ROLE_PERMISSIONS_MAPPING[role_name]

            if '*' in role_perms:
                actions = role_perms['*']
                self.fields['user_permissions'].queryset = Permission.objects.filter(
                    codename__regex=r'^({})_'.format('|'.join(actions))
                )
            else:
                filters = []
                for model, actions in role_perms.items():
                    for action in actions:
                        filters.append(f"{action}_{model}")
                self.fields['user_permissions'].queryset = Permission.objects.filter(
                    codename__in=filters
                ).select_related('content_type')

        # Masquer ou afficher fonction_agent selon le rôle
        if role_name != 'AGENT':
            self.fields.pop('fonction_agent', None)
        else:
            self.fields['fonction_agent'].queryset = FonctionAgent.objects.filter(
                role=Utilisateur.Role.AGENT
            )

    def get_grouped_permissions(self):
        grouped = defaultdict(list)
        action_labels = {
            'add': 'Ajouter',
            'change': 'Modifier',
            'delete': 'Supprimer',
            'view': 'Voir',
        }

        for perm in self.fields['user_permissions'].queryset:
            model = perm.content_type.model  # ex: frais
            app = perm.content_type.app_label  # ex: finance
            codename_parts = perm.codename.split('_')
            if len(codename_parts) >= 2:
                action = codename_parts[0]
                label = action_labels.get(action, perm.name)
                grouped[(app, model)].append((perm.id, label))

        return grouped

    def save(self):
        user = super().save(commit=True)
        print(user)
        fonctions = self.cleaned_data.get('fonction_agent')  # liste ou queryset de fonctions
        print(fonctions)
        # Vérifie si un AgentAdministration existe déjà
        agent, created = AgentAdministration.objects.get_or_create(utilisateur=user)

        # Met à jour les fonctions
        if fonctions:
            agent.fonctions.set(fonctions)  # met à jour ManyToManyField
        else:
            agent.fonctions.clear()  # ou garde tel quel si tu préfères

        return user


# class UserRolePermissionForm(forms.ModelForm):
#
#     user_permissions = forms.ModelMultipleChoiceField(
#         queryset=Permission.objects.all(),
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'permission-checkbox'}),
#         required=False,
#         label="Permissions"
#     )
#
#     class Meta:
#         model = Utilisateur
#         fields = ['user_permissions', 'groups']
#         widgets = {
#             'groups': forms.CheckboxSelectMultiple(attrs={'class': 'group-checkbox'}),
#         }
#         help_texts = {
#             'user_permissions': "Sélectionnez les permissions spécifiques pour cet utilisateur",
#             'groups': "Sélectionnez les groupes d'appartenance",
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#         role = self.instance.role
#         role_name = role.name if hasattr(role, 'name') else role
#
#         if role_name in ROLE_PERMISSIONS_MAPPING:
#             role_perms = ROLE_PERMISSIONS_MAPPING[role_name]
#
#             if '*' in role_perms:
#                 actions = role_perms['*']
#                 self.fields['user_permissions'].queryset = Permission.objects.filter(
#                     codename__regex=r'^({})_'.format('|'.join(actions))
#                 )
#             else:
#                 filters = []
#                 for model, actions in role_perms.items():
#                     for action in actions:
#                         filters.append(f"{action}_{model}")
#                 self.fields['user_permissions'].queryset = Permission.objects.filter(
#                     codename__in=filters
#                 ).select_related('content_type')
#
#         # Dynamically add fonction_agent only for AGENT role
#         if role_name == 'AGENT':
#             self.fields['fonction_agent'] = forms.ModelMultipleChoiceField(
#                 queryset=FonctionAgent.objects.filter(role=Utilisateur.Role.AGENT),
#                 required=False,
#                 label="Fonctions administratives",
#                 help_text="Sélectionnez une ou plusieurs fonctions pour les agents administratifs",
#                 widget=forms.CheckboxSelectMultiple
#             )
#
#             # Pré-remplir les fonctions si une instance est fournie
#             if self.instance.pk:
#                 self.fields['fonction_agent'].initial = FonctionAgent.objects.filter(
#                     agentadministration__utilisateur=self.instance
#                 )
#
#     def save(self, commit=True):
#         user = super().save(commit=False)
#
#         if commit:
#             user.save()
#             self.save_m2m()
#
#             # Sauvegarder les fonctions sélectionnées
#             if user.role == Utilisateur.Role.AGENT and 'fonction_agent' in self.cleaned_data:
#                 fonctions = self.cleaned_data['fonction_agent']
#                 AgentAdministration.objects.filter(utilisateur=user).delete()
#                 for fonction in fonctions:
#                     AgentAdministration.objects.create(utilisateur=user, fonction=fonction)
#
#         return user


class AssignFonctionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.none(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'permission-checkbox'}),
        required=False,
        label="Permissions associées"
    )

    class Meta:
        model = FonctionAgent
        fields = ['code', 'nom', 'description', 'responsabilites', 'controles', 'protocoles', 'permissions']
        widgets = {
            'code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: SECRETARIAT_ADMIN'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Secrétaire administratif'
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Décrire les missions principales...'
            }),
            'responsabilites': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Liste des responsabilités...'
            }),
            'controles': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Liste des contrôles...'
            }),
            'protocoles': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Liste des protocoles...'
            }),
        }
        help_texts = {
            'code': "Code unique (3 caractères minimum)",
            'nom': "Nom complet de la fonction",
            'description': "Description détaillée du rôle",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # On limite aux permissions définies dans PERMISSIONS_DISPONIBLES
        valid_permissions = [
            f"{action}_{model}"
            for model, actions in FonctionAgent.PERMISSIONS_DISPONIBLES.items()
            for action in actions.keys()
        ]

        self.fields['permissions'].queryset = Permission.objects.filter(
            codename__in=valid_permissions
        ).select_related('content_type').order_by('content_type__model', 'codename')

        # Organisation des permissions par modèle pour un meilleur affichage
        self.fields['permissions'].choices = self._get_grouped_permissions()

        if self.instance.pk:
            self.fields['permissions'].initial = self.instance.permissions.all()

    def _get_grouped_permissions(self):
        """Organise les permissions par modèle pour le template"""
        grouped = {}
        for perm in self.fields['permissions'].queryset:
            model = perm.content_type.model
            if model not in grouped:
                grouped[model] = []
            grouped[model].append((perm.id, perm.name))

        return sorted(grouped.items())

    def save(self, commit=True):
        fonction = super().save(commit=False)

        if commit:
            fonction.save()
            self.save_m2m()  # Pour sauvegarder les relations ManyToMany

        return fonction


# class CustomPermissionForm(forms.ModelForm):
#     roles_autorises = forms.MultipleChoiceField(
#         choices=Utilisateur.Role.choices,
#         widget=forms.CheckboxSelectMultiple(attrs={'class': 'role-checkbox'}),
#         required=True,
#         label="Rôles autorisés"
#     )
#
#     description = forms.CharField(
#         widget=forms.Textarea(attrs={'rows': 3}),
#         required=False,
#         help_text="Description complète de ce que permet cette permission"
#     )
#
#     class Meta:
#         model = Permission
#         fields = ['name', 'codename', 'content_type']
#         widgets = {
#             'content_type': forms.Select(attrs={'class': 'select2'}),
#         }
#         help_texts = {
#             'name': "Nom lisible pour la permission (ex: 'Peut publier des articles')",
#             'codename': "Code technique utilisé dans le code (ex: 'publish_article')",
#             'content_type': "Modèle auquel cette permission s'applique",
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['content_type'].queryset = ContentType.objects.all().order_by('app_label', 'model')
#
#     def clean_codename(self):
#         codename = self.cleaned_data['codename']
#         if not codename.isidentifier():
#             raise forms.ValidationError(
#                 "Le code doit être un identifiant Python valide (lettres, chiffres, underscores)"
#             )
#         return codename
#
#     def clean(self):
#         cleaned_data = super().clean()
#         print("=== VALIDATION DU FORMULAIRE ===")
#
#         codename = cleaned_data.get('codename')
#         content_type = cleaned_data.get('content_type')
#
#         if codename and content_type:
#             print(f"Vérification de l'existence de la permission: {codename} pour {content_type}")
#
#             # Vérifie si la permission existe déjà
#             permission_exists = Permission.objects.filter(
#                 codename=codename,
#                 content_type=content_type
#             ).exists()
#
#             print(f"Permission existe déjà ? {permission_exists}")
#
#             if permission_exists:
#                 # Si on est en mode édition, on vérifie que ce n'est pas la même permission
#                 if hasattr(self, 'instance') and self.instance:
#                     existing_perm = Permission.objects.get(
#                         codename=codename,
#                         content_type=content_type
#                     )
#                     if existing_perm.id == self.instance.id:
#                         print("Même permission - autorisé pour l'édition")
#                         return cleaned_data
#
#                 print("Erreur: Permission déjà existante")
#                 raise forms.ValidationError(
#                     "Une permission avec ce code existe déjà pour ce type de contenu"
#                 )
#
#         return cleaned_data
#
#     def save(self):
#         print("=== DEBUT DE LA METHODE SAVE ===")
#         print("Données nettoyées:", self.cleaned_data)
#
#         try:
#             print("Tentative de création de la permission...")
#             permission = Permission.objects.create(
#                 name=self.cleaned_data['name'],
#                 codename=self.cleaned_data['codename'],
#                 content_type=self.cleaned_data['content_type']
#             )
#             print("Permission créée avec succès:", permission)
#         except Exception as e:
#             print("ERREUR lors de la création de la permission:", str(e))
#             raise
#
#         try:
#             print("Tentative de création de MetaPermission...")
#             from .models import MetaPermission
#             meta, created = MetaPermission.objects.get_or_create(
#                 permission=permission,
#                 defaults={
#                     'description': self.cleaned_data.get('description', ''),
#                     'roles_autorises': ','.join(self.cleaned_data['roles_autorises'])
#                 }
#             )
#             print("MetaPermission créée avec succès:", meta)
#         except Exception as e:
#             print("ERREUR lors de la création de MetaPermission:", str(e))
#             raise
#
#         print("=== FIN DE LA METHODE SAVE ===")
#         return permission


class CustomPermissionForm(forms.ModelForm):
    roles_autorises = forms.MultipleChoiceField(
        choices=[],  # Définies dynamiquement
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'role-checkbox',
            'disabled': 'disabled'
        }),
        required=False,
        label=_("Rôles utilisant cette permission")
    )

    class Meta:
        model = Permission
        fields = ['name', 'codename', 'content_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.name:
            self.initial['name'] = self.translate_permission_name(self.instance.name)

        if self.instance and self.instance.content_type:
            self.initial['content_type'] = str(self.instance.content_type)

        # 💡 Rechercher les rôles qui ont cette permission

        roles_ayant_permission = RolePermission.objects.filter(permissions=self.instance)
        role_choices = [(rp.role, rp.get_role_display()) for rp in roles_ayant_permission]

        self.fields['roles_autorises'].choices = role_choices
        self.initial['roles_autorises'] = [rp.role for rp in roles_ayant_permission]

        # Rendre tous les champs désactivés (lecture seule)
        for field in self.fields.values():
            field.disabled = True

    def translate_permission_name(self, name):
        translations = {
            'Can add': 'Ajouter',
            'Can change': 'Modifier',
            'Can delete': 'Supprimer',
            'Can view': 'Voir',
        }
        for eng, fr in translations.items():
            name = name.replace(eng, fr)
        return name

    def get_content_type_display(self):
        if self.instance and self.instance.content_type:
            return f"{self.instance.content_type.app_label}.{self.instance.content_type.model}"
        return ""

    def clean(self):
        return self.cleaned_data

    def save(self, commit=True):
        raise NotImplementedError("Ce formulaire est en lecture seule")
