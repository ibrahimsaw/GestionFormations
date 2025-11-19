from django import forms
from .models import Salle, Matiere, Evaluation, Note, Cours, MatiereClasse, Enseignement
from Utilisateur.models import Etudiant, Enseignant
from Formation.models import Classe,AnneeAcademique


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
            'annee_academique': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ---- CHAMP ANNEE ACADEMIQUE ----
        self.fields['annee_academique'].queryset = AnneeAcademique.objects.all()

        # ---- FILTRAGE DES ENSEIGNANTS ----
        # Récupération de matiere_classe depuis initial ou POST
        matiere_classe_id = (
            self.data.get('matiere_classe')
            or self.initial.get('matiere_classe')
        )

        if matiere_classe_id:
            mc = MatiereClasse.objects.filter(pk=matiere_classe_id).first()
            if mc:
                # Filtrer uniquement les enseignants qui enseignent cette matière
                self.fields['enseignant'].queryset = Enseignant.objects.filter(
                    matieres=mc.matiere
                )
            else:
                self.fields['enseignant'].queryset = Enseignant.objects.none()
        else:
            # Si pas encore de matière choisie → aucun enseignant
            self.fields['enseignant'].queryset = Enseignant.objects.none()
            self.fields['enseignant'].widget.attrs['disabled'] = True


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
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=False,
        label="Classe",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    matiere = forms.ModelChoiceField(
        queryset=Matiere.objects.all(),
        required=False,
        label="Matière",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    enseignant = forms.ModelChoiceField(
        queryset=Enseignant.objects.all(),
        required=False,
        label="Enseignant",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Evaluation
        fields = ["classe", "matiere", "enseignant", "titre", "type", "date"]
        widgets = {
            'titre': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        classe = self.data.get("classe") or (self.instance.pk and self.instance.enseignement.classe.id)
        matiere = self.data.get("matiere") or (self.instance.pk and self.instance.enseignement.matiere_classe.matiere.id)
        enseignant = self.data.get("enseignant") or (self.instance.pk and self.instance.enseignement.enseignant.id)

        # ------------------------
        # Filtrage dynamique des querysets
        # ------------------------

        if classe:
            self.fields["matiere"].queryset = Matiere.objects.filter(
                id__in=MatiereClasse.objects.filter(classe_id=classe).values("matiere")
            )
            self.fields["enseignant"].queryset = Enseignant.objects.filter(
                id__in=Enseignement.objects.filter(matiere_classe__classe_id=classe).values("enseignant")
            )

        if matiere:
            self.fields["classe"].queryset = Classe.objects.filter(
                id__in=MatiereClasse.objects.filter(matiere_id=matiere).values("classe")
            )
            self.fields["enseignant"].queryset = Enseignant.objects.filter(
                id__in=Enseignement.objects.filter(matiere_classe__matiere_id=matiere).values("enseignant")
            )

        if enseignant:
            self.fields["classe"].queryset = Classe.objects.filter(
                id__in=Enseignement.objects.filter(enseignant_id=enseignant).values("matiere_classe__classe")
            )
            self.fields["matiere"].queryset = Matiere.objects.filter(
                id__in=Enseignement.objects.filter(enseignant_id=enseignant).values("matiere_classe__matiere")
            )

    # ------------------------
    # Validation : on construit l'enseignement
    # ------------------------
    def clean(self):
        cleaned_data = super().clean()
        classe = cleaned_data.get("classe")
        matiere = cleaned_data.get("matiere")
        enseignant = cleaned_data.get("enseignant")

        if not (classe and matiere and enseignant):
            raise forms.ValidationError("Vous devez choisir la classe, la matière et l’enseignant.")

        # Trouver le MatiereClasse correspondant
        try:
            mc = MatiereClasse.objects.get(classe=classe, matiere=matiere)
        except MatiereClasse.DoesNotExist:
            raise forms.ValidationError("Cette matière n’existe pas pour cette classe.")

        # Trouver l’enseignement correspondant
        try:
            enseignement = Enseignement.objects.get(enseignant=enseignant, matiere_classe=mc)
        except Enseignement.DoesNotExist:
            raise forms.ValidationError("Cet enseignant n’enseigne pas cette matière dans cette classe.")

        cleaned_data["enseignement"] = enseignement
        return cleaned_data

    # ------------------------
    # Save : injecter l’enseignement
    # ------------------------
    def save(self, commit=True):
        evaluation = super().save(commit=False)
        evaluation.enseignement = self.cleaned_data["enseignement"]
        if commit:
            evaluation.save()
        return evaluation


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
