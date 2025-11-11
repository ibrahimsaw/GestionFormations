from django.contrib import admin
from .models import (
    Utilisateur, AdminSysteme, AgentAdministration, Enseignant, Etudiant, Parent,
     FonctionAgent
)


def get_utilisateur_fields(prefix='utilisateur'):
    champs = [
        ('matricule', 'Matricule'),
        ('last_name', 'Nom'),
        ('first_name', 'Prénom'),
        ('email', 'Email'),
        ('telephone', 'Téléphone'),
        ('get_role_display', 'Rôle'),
        ('date_nais', 'Date de naissance'),
        ('date_inscription', "Date d'inscription"),
        ('genre', "Genre"),
    ]

    fonctions = []

    for attr, label in champs:
        def make_func(attr, label):
            def func(self, obj):
                val = getattr(obj.utilisateur, attr)
                return val() if callable(val) else val
            func.short_description = label
            func.__name__ = f"{prefix}_{attr}"
            return func
        fonctions.append(make_func(attr, label))

    return fonctions


@admin.register(AdminSysteme)
class AdminSystemeAdmin(admin.ModelAdmin):
    list_display = [f.__name__ for f in get_utilisateur_fields()]

# Injecter les méthodes dynamiques dans AdminSystemeAdmin
for f in get_utilisateur_fields():
    setattr(AdminSystemeAdmin, f.__name__, f)


@admin.register(AgentAdministration)
class AgentAdministrationAdmin(admin.ModelAdmin):
    list_display = [f.__name__ for f in get_utilisateur_fields()] + ['get_fonctions']

    def get_fonctions(self, obj):
        return ", ".join([f.nom for f in obj.fonctions.all()])
    get_fonctions.short_description = 'Fonctions'

# Injecter les méthodes dynamiques dans AgentAdministrationAdmin
for f in get_utilisateur_fields():
    setattr(AgentAdministrationAdmin, f.__name__, f)



@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('pk', 'matricule', 'first_name', 'last_name', 'email', 'role', 'is_staff','doit_changer_mot_de_passe')
    readonly_fields = ('matricule',)


# @admin.register(AdminSysteme)
# class AdminSystemeAdmin(admin.ModelAdmin):
#     list_display = [f.__name__ for f in get_utilisateur_fields()]
#     for f in get_utilisateur_fields():
#         locals()[f.__name__] = f


# @admin.register(AgentAdministration)
# class AgentAdministrationAdmin(admin.ModelAdmin):
#     list_display = [f.__name__ for f in get_utilisateur_fields()] + ['get_fonctions']
#     for f in get_utilisateur_fields():
#         locals()[f.__name__] = f
#
#     def get_fonctions(self, obj):
#         return ", ".join([f.nom for f in obj.fonctions.all()])
#get_specialite
#     get_fonctions.short_description = 'Fonctions'



@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
    # On génère les colonnes utilisateur dynamiquement
    list_display = [f.__name__ for f in get_utilisateur_fields()] + ['get_matieres', 'autres_matieres']

    # Ajouter dynamiquement les méthodes utilisateur
    for f in get_utilisateur_fields():
        locals()[f.__name__] = f

    # Méthode pour afficher les matières comme texte
    def get_matieres(self, obj):
        return ", ".join([m.nom for m in obj.matieres.all()])
    get_matieres.short_description = "Matières enseignées"



@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = [f.__name__ for f in get_utilisateur_fields()]
    for f in get_utilisateur_fields():
        locals()[f.__name__] = f


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = [f.__name__ for f in get_utilisateur_fields()] + ['enfants_details']
    for f in get_utilisateur_fields():
        locals()[f.__name__] = f

    def enfants_details(self, obj):
        enfants_info = []
        for enfant in obj.enfants.all():
            nom = f"{enfant.utilisateur.last_name} {enfant.utilisateur.first_name}"
            info = nom
            # Tu peux activer ceci si Etudiant a un champ 'niveau'
            # if hasattr(enfant, 'niveau') and enfant.niveau:
            #     info += f" ({enfant.niveau})"
            enfants_info.append(info)
        return ", ".join(enfants_info) if enfants_info else "Aucun enfant"
    enfants_details.short_description = "Enfants"

@admin.register(FonctionAgent)
class FonctionAgentAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'role', 'description')
    filter_horizontal = ('permissions',)
