from django.contrib import admin
from .models import Salle, Matiere, Chapitre, Evaluation, Note, Cours
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
    list_display = ('nom', 'code', 'coefficient', 'volume_horaire')
    list_filter = ('classes',)
    search_fields = ('nom', 'code')
    filter_horizontal = ('classes',)  # pratique pour ManyToMany

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
    list_display = ('matiere', 'classe', 'enseignant', 'salle', 'date', 'heure_debut', 'heure_fin', 'type_cours')
    list_filter = ('matiere', 'classe', 'enseignant', 'salle', 'type_cours', 'date')
    search_fields = ('matiere__nom', 'classe__nom', 'enseignant__nom')
    date_hierarchy = 'date'
