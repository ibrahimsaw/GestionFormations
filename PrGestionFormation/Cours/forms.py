from django import forms
from .models import Salle, Matiere, Evaluation, Note, Cours, MatiereClasse, Enseignement
from Utilisateur.models import Etudiant, Enseignant
from Formation.models import Classe

# --------------------------
# Formulaire Salle
# --------------------------
class SalleForm(forms.ModelForm):
    class Meta:
        model = Salle
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control'}),
            'batiment': forms.TextInput(attrs={'class': 'form-control'}),
            'etage': forms.NumberInput(attrs={'class': 'form-control'}),
            'projecteur': forms.CheckboxInput(),
            'climatisation': forms.CheckboxInput(),
            'ordinateurs': forms.CheckboxInput(),
            'tableau_blanc': forms.CheckboxInput(),
            'est_actif': forms.CheckboxInput(),
        }

# --------------------------
# Formulaire Matiere
# --------------------------
class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }

class MatiereClasseForm(forms.ModelForm):
    class Meta:
        model = MatiereClasse
        fields = '__all__'
        widgets = {
            'matiere': forms.Select(attrs={'class': 'form-select'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control'}),
            'volume_horaire': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class EnseignementForm(forms.ModelForm):
    class Meta:
        model = Enseignement
        fields = '__all__'
        widgets = {
            'enseignant': forms.Select(attrs={'class': 'form-select'}),
            'matiere_classe': forms.Select(attrs={'class': 'form-select'}),
            'annee_scolaire': forms.TextInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Si une matière est déjà sélectionnée (dans le POST ou l’instance)
        matiere_classe = self.initial.get('matiere_classe') or self.data.get('matiere_classe')

        if matiere_classe := self.initial.get('matiere_classe') or self.data.get('matiere_classe'):
            mc = MatiereClasse.objects.filter(pk=matiere_classe).first()
            if mc:
                # On filtre les enseignants qui enseignent cette matière
                self.fields['enseignant'].queryset = Enseignant.objects.filter(matieres=mc.matiere)
            else:
                self.fields['enseignant'].queryset = Enseignant.objects.none()
        else:
            # Par défaut, on affiche tous les enseignants
            self.fields['enseignant'].queryset = Enseignant.objects.all()
# --------------------------
# Formulaire Chapitre
# --------------------------
# class ChapitreForm(forms.ModelForm):
#     class Meta:
#         model = Chapitre
#         fields = '__all__'
#         widgets = {
#             'matiere': forms.Select(attrs={'class': 'form-select'}),
#             'titre': forms.TextInput(attrs={'class': 'form-control'}),
#             'objectifs': forms.Textarea(attrs={'class': 'form-control'}),
#         }

# --------------------------
# Formulaire Evaluation
# --------------------------
class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = '__all__'
        widgets = {
            'matiere': forms.Select(attrs={'class': 'form-select'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# --------------------------
# Formulaire Note
# --------------------------
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = '__all__'
        widgets = {
            'evaluation': forms.Select(attrs={'class': 'form-select'}),
            'etudiant': forms.Select(attrs={'class': 'form-select'}),
            'note': forms.NumberInput(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control'}),
        }

# --------------------------
# Formulaire Cours
# --------------------------
class CoursForm(forms.ModelForm):
    class Meta:
        model = Cours
        fields = '__all__'
        widgets = {
            'enseignement': forms.Select(attrs={'class': 'form-select'}),
            'salle': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'heure_debut': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'heure_fin': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'type_cours': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }
