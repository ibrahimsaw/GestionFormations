from django.contrib import admin
from .models import *
from Utilisateur.models import Etudiant, Enseignant
from Formation.models import Classe

# --------------------------
# Admin Salle
# --------------------------
@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'type', 'capacite', 'batiment', 'etage', 'est_actif')
    list_filter = ('type', 'est_actif', 'batiment')
    search_fields = ('nom', 'batiment')
    ordering = ('nom',)

# --------------------------
# Admin Matiere
# --------------------------
@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code','description')
    search_fields = ('nom', 'code')
    ordering = ('nom',)

# --------------------------
# Admin Chapitre
# --------------------------
@admin.register(Chapitre)
class ChapitreAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere')
    search_fields = ('titre',)
    list_filter = ('matiere',)

# --------------------------
# Admin Evaluation
# --------------------------
@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'classe', 'type', 'date', 'coefficient')
    list_filter = ('type', 'matiere', 'classe', 'date')
    search_fields = ('titre',)
    date_hierarchy = 'date'

# --------------------------
# Admin Note
# --------------------------
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'evaluation', 'note')
    list_filter = ('evaluation',)
    search_fields = ('etudiant__nom', 'evaluation__titre')

# --------------------------
# Admin Cours
# --------------------------
@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ('enseignement', 'salle', 'date', 'heure_debut', 'heure_fin', 'type_cours')
    list_filter = ('enseignement__matiere_classe__matiere', 'enseignement__matiere_classe__classe', 'enseignement__enseignant', 'salle', 'type_cours', 'date')
    search_fields = ('enseignement__matiere_classe__matiere__nom', 'enseignement__matiere_classe__classe__nom', 'enseignement__enseignant__nom')
    date_hierarchy = 'date'

@admin.register(Enseignement)
class EnseignementAdmin(admin.ModelAdmin):
    list_display = ('enseignant', 'matiere_classe', 'annee_academique')
    list_filter = ('annee_academique', 'matiere_classe__matiere', 'matiere_classe__classe')
    search_fields = ('enseignant__nom', 'matiere_classe__matiere__nom', 'matiere_classe__classe__nom')
    ordering = ('annee_academique',)

@admin.register(MatiereClasse)
class MatiereClasseAdmin(admin.ModelAdmin):
    list_display = ('matiere', 'classe', 'coefficient')
    list_filter = ('classe', 'matiere')
    search_fields = ('matiere__nom', 'classe__nom')
    ordering = ('classe', 'matiere')
