from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from Cours.forms import MatiereForm
from django.apps import apps
from .models import *
from Formation.models import Parcours,Classe,AnneeAcademique
from Finance.models import Inscription
import uuid


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('matricule', 'genre','email', 'telephone', 'first_name', 'last_name','password1', 'password2','date_nais')
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'date_nais': 'Date de Nassance',
            'matricule': 'Matricule',
            'password1': 'Mot de passe',
            'password2': 'Confirmez le mot de passe',
        }
        date_inscription = forms.DateTimeField(
            label='Date d’inscription',
            required=False,
            disabled=True,  # rend le champ non modifiable
        )

    def __init__(self, *args, role=None, **kwargs):
        self.role = role
        super().__init__(*args, **kwargs)
        self.fields['password1'].required = True
        self.fields['password2'].required = True

        if not self.instance.matricule:
            prefix = {
                'ADMIN': 'ADM',
                'AGENT': 'AGT',
                'ENSEIGNANT': 'ENS',
                'ETUDIANT': 'ETU',
                'PARENT': 'PAR'
            }.get(self.role, 'USR')
            self.fields['matricule'].initial = f"{prefix}-{uuid.uuid4().hex[:6].upper()}"
            self.fields['matricule'].disabled = True  # Champ visible mais non modifiable

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.role:
            user.role = self.role

        # S'assurer que le mot de passe est bien défini s'il est fourni
        if password := self.cleaned_data.get('password1'):
            user.set_password(password)

        if commit:
            user.save()
            self.data = self.data.copy()
            self.data['matricule'] = user.matricule
        return user





class AdminSystemeForm(forms.ModelForm):
    class Meta:
        model = AdminSysteme
        fields = []  # on enlève le champ utilisateur, il sera géré séparément

    def __init__(self, *args, **kwargs):
        self.utilisateur_data = kwargs.pop('utilisateur_data', None)
        super().__init__(*args, **kwargs)
        self.utilisateur_form = CustomUserCreationForm(
            data=self.utilisateur_data,
            prefix='utilisateur',
            role = 'ADMIN'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        return super().save(commit=commit)


class AgentAdministrationForm(forms.ModelForm):
    fonctions = forms.ModelMultipleChoiceField(
        queryset=FonctionAgent.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Fonctions"
    )

    class Meta:
        model = AgentAdministration
        fields = ['fonctions']

    # Reste du code pareil...

    def __init__(self, *args, **kwargs):
        self.utilisateur_data = kwargs.pop('utilisateur_data', None)
        super().__init__(*args, **kwargs)
        self.utilisateur_form = CustomUserCreationForm(
            data=self.utilisateur_data,
            prefix='utilisateur',
            role='AGENT'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        return super().save(commit=commit)



Matiere = apps.get_model('Cours', 'Matiere')

class EnseignantForm(forms.ModelForm):
    nouvelle_matiere = forms.CharField(
        required=False,
        label="Nouvelle matière à ajouter",
        help_text="Laissez vide si aucune nouvelle matière à créer"
    )

    class Meta:
        model = Enseignant
        fields = ['matieres', 'autres_matieres', 'bureau','date_embauche','grade']
        widgets = {
            'matieres': forms.CheckboxSelectMultiple(),
            'autres_matieres': forms.TextInput(
                attrs={'placeholder': 'Autres matières (séparées par des virgules)'}
            ),
            'date_embauche': forms.DateInput(attrs={'type': 'date'}),
            'bureau': forms.TextInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.utilisateur_data = kwargs.pop('utilisateur_data', None)
        super().__init__(*args, **kwargs)
        self.fields['matieres'].queryset = Matiere.objects.all()
        self.matiere_form = MatiereForm(prefix='matiere')
        self.utilisateur_form = CustomUserCreationForm(
            data=self.utilisateur_data,
            prefix='utilisateur',
            role='ENSEIGNANT'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        # Sauvegarde l'utilisateur
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur

        # Sauvegarde l'enseignant
        instance = super().save(commit=False)

        # Gestion de la nouvelle matière
        nouvelle_matiere = self.cleaned_data.get('nouvelle_matiere')
        if nouvelle_matiere and nouvelle_matiere.strip():
            matiere, created = Matiere.objects.get_or_create(
                nom=nouvelle_matiere.strip()
            )
            instance.matieres.add(matiere)

        if commit:
            instance.save()
            self.save_m2m()  # Important pour les relations ManyToMany

        return instance

    def clean(self):
        cleaned_data = super().clean()
        print("EnseignantForm cleaned_data:", cleaned_data)
        return cleaned_data

class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        self.utilisateur_data = kwargs.pop('utilisateur_data', None)
        super().__init__(*args, **kwargs)
        self.utilisateur_form = CustomUserCreationForm(
            data=self.utilisateur_data,
            prefix='utilisateur',
            role = 'ETUDIANT'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        return super().save(commit=commit)

class EtudiantInscriptionForm(forms.ModelForm):
    parcours = forms.ModelChoiceField(
        queryset=Parcours.objects.all(),
        required=True
    )
    classe = forms.ModelChoiceField(
        queryset=Classe.objects.all(),
        required=True
    )
    annee_academique = forms.ModelChoiceField(
        queryset=AnneeAcademique.objects.all(),
        required=True
    )

    class Meta:
        model = Etudiant
        fields = '__all__'
        exclude = ['utilisateur']  # utilisateur géré par CustomUserCreationForm

    def __init__(self, *args, **kwargs):
        self.utilisateur_data = kwargs.pop('utilisateur_data', None)
        super().__init__(*args, **kwargs)

        # Formulaire utilisateur lié
        self.utilisateur_form = CustomUserCreationForm(
            data=self.utilisateur_data,
            prefix='utilisateur',
            role='ETUDIANT'
        )

        # Remplissage statique des champs liés
        self.fields['parcours'].queryset = Parcours.objects.all()
        self.fields['classe'].queryset = Classe.objects.all()
        self.fields['annee_academique'].queryset = AnneeAcademique.objects.all()

    def is_valid(self):
        valid = super().is_valid()
        utilisateur_valid = self.utilisateur_form.is_valid()

        if not valid:
            print("❌ Erreurs Étudiant :", self.errors)
        if not utilisateur_valid:
            print("❌ Erreurs Utilisateur :", self.utilisateur_form.errors)

        return valid and utilisateur_valid

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)

        etudiant = super().save(commit=False)
        etudiant.utilisateur = utilisateur

        if commit:
            etudiant.save()

            # Création d’une inscription automatique
            Inscription.objects.create(
                etudiant=etudiant,
                parcours=self.cleaned_data['parcours'],
                classe=self.cleaned_data['classe'],
                annee_academique=self.cleaned_data['annee_academique'],
                statut=Inscription.STATUT_INSCRIT
            )

        return etudiant


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['enfants']
    def __init__(self, *args, **kwargs):
        self.utilisateur_data = kwargs.pop('utilisateur_data', None)
        super().__init__(*args, **kwargs)
        self.utilisateur_form = CustomUserCreationForm(
            data=self.utilisateur_data,
            prefix='utilisateur',
            role = 'PARENT'
        )
    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        return super().save(commit=commit)


##*********************************

class CustomUserChangeForm(UserChangeForm):
    date_nais = forms.DateField(
        label="Date de naissance",
        widget=forms.DateInput(
            attrs={'type': 'date'},  # HTML5 date picker
            format='%Y-%m-%d'
        ),
        required=False
    )
    class Meta:
        model = Utilisateur
        fields = ('matricule', 'genre', 'email', 'telephone', 'first_name', 'last_name', 'date_nais')
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'date_nais': 'Date de naissance',
            'matricule': 'Matricule',
        }
        widgets = {
            'date_nais': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Supprimer les champs liés au mot de passe
        self.fields.pop('password', None)
        if 'date_nais' in self.fields and self.instance.date_nais:
            self.fields['date_nais'].initial = self.instance.date_nais.strftime('%Y-%m-%d')

        # Rendre le champ matricule non modifiable
        if 'matricule' in self.fields:
            self.fields['matricule'].disabled = True
            self.fields['matricule'].required = False


class FonctionAgentForm(forms.ModelForm):
    class Meta:
        model = FonctionAgent
        fields = ['nom', 'description']
        labels = {
            'nom': 'Nom de la fonction',
            'description': 'Description',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si tu veux afficher le rôle en lecture seule (valeur fixe AGENT)
        self.fields['nom'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

class AdminSystemeUpdateForm(forms.ModelForm):
    class Meta:
        model = AdminSysteme
        fields = []  # Pas de champ spécifique ici

    def __init__(self, *args, **kwargs):
        utilisateur_instance = kwargs.pop('utilisateur_instance', None)
        data = kwargs.get('data')  # ✔️ Récupère POST ou None
        super().__init__(*args, **kwargs)

        self.utilisateur_form = CustomUserChangeForm(
            data=data,
            instance=utilisateur_instance,
            prefix='utilisateur'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        return super().save(commit=commit)

# class AgentAdministrationUpdateForm(forms.ModelForm):
#     class Meta:
#         model = AgentAdministration
#         fields = ['fonctions']
#
#     def __init__(self, *args, **kwargs):
#         self.utilisateur_instance = kwargs.pop('utilisateur_instance', None)
#         super().__init__(*args, **kwargs)
#         self.utilisateur_form = CustomUserChangeForm(
#             instance=self.utilisateur_instance,
#             prefix='utilisateur'
#         )
#
#     def is_valid(self):
#         return super().is_valid() and self.utilisateur_form.is_valid()
#
#     def save(self, commit=True):
#         utilisateur = self.utilisateur_form.save(commit=commit)
#         self.instance.utilisateur = utilisateur
#         return super().save(commit=commit)
class AgentAdministrationUpdateForm(forms.ModelForm):
    fonctions = forms.ModelMultipleChoiceField(
        queryset=FonctionAgent.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Fonctions"
    )

    class Meta:
        model = AgentAdministration
        fields = ['fonctions']

    def __init__(self, *args, **kwargs):
        utilisateur_instance = kwargs.pop('utilisateur_instance', None)
        data = kwargs.get('data')  # ✔️ Récupère POST ou None
        super().__init__(*args, **kwargs)

        self.utilisateur_form = CustomUserChangeForm(
            data=data,
            instance=utilisateur_instance,
            prefix='utilisateur'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        return super().save(commit=commit)


class EnseignantUpdateForm(forms.ModelForm):
    nouvelle_matiere = forms.CharField(
        required=False,
        label="Nouvelle matière à ajouter",
        help_text="Laissez vide si aucune nouvelle matière à créer"
    )

    class Meta:
        model = Enseignant
        fields = ['matieres', 'autres_matieres','bureau','date_embauche','grade']
        widgets = {
            'matieres': forms.CheckboxSelectMultiple,
            'autres_matieres': forms.TextInput(attrs={'placeholder': 'Autres matières (séparées par des virgules)'}),
        }

    def __init__(self, *args, **kwargs):
        utilisateur_instance = kwargs.pop('utilisateur_instance', None)
        data = kwargs.get('data')  # ✔️ Récupère POST ou None
        super().__init__(*args, **kwargs)

        self.utilisateur_form = CustomUserChangeForm(
            data=data,
            instance=utilisateur_instance,
            prefix='utilisateur'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur

        instance = super().save(commit=False)
        if nouvelle_specialite := self.cleaned_data.get('nouvelle_matiere'):
            specialite, _ = Matiere.objects.get_or_create(nom=nouvelle_specialite.strip())
            instance.specialites.add(specialite)

        if commit:
            instance.save()
            self.save_m2m()

        return instance

class EtudiantUpdateForm(forms.ModelForm):
    parcours = forms.ModelChoiceField(queryset=Parcours.objects.all(), required=True)
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), required=True)
    annee_academique = forms.ModelChoiceField(queryset=AnneeAcademique.objects.all(), required=True)

    class Meta:
        model = Etudiant
        exclude = ['utilisateur']

    def __init__(self, *args, **kwargs):
        utilisateur_instance = kwargs.pop('utilisateur_instance', None)
        self.utilisateur_data = kwargs.get('data')
        super().__init__(*args, **kwargs)

        self.utilisateur_form = CustomUserChangeForm(
            data=self.utilisateur_data,
            instance=utilisateur_instance,
            prefix='utilisateur'
        )

        # Préremplissage automatique depuis la dernière inscription
        if self.instance and self.instance.pk:
            inscription = self.instance.inscriptions.order_by('-annee_academique').first()
            if inscription:
                self.fields['parcours'].initial = inscription.parcours
                self.fields['classe'].initial = inscription.classe
                self.fields['annee_academique'].initial = inscription.annee_academique

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        etudiant = super().save(commit=commit)

        if commit:
            inscription = etudiant.inscriptions.order_by('-annee_academique').first()
            if inscription:
                inscription.parcours = self.cleaned_data['parcours']
                inscription.classe = self.cleaned_data['classe']
                inscription.annee_academique = self.cleaned_data['annee_academique']
                inscription.save()

        return etudiant


class ParentUpdateForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ['enfants']

    def __init__(self, *args, **kwargs):
        utilisateur_instance = kwargs.pop('utilisateur_instance', None)
        data = kwargs.get('data')  # ✔️ Récupère POST ou None
        super().__init__(*args, **kwargs)

        self.utilisateur_form = CustomUserChangeForm(
            data=data,
            instance=utilisateur_instance,
            prefix='utilisateur'
        )

    def is_valid(self):
        return super().is_valid() and self.utilisateur_form.is_valid()

    def save(self, commit=True):
        utilisateur = self.utilisateur_form.save(commit=commit)
        self.instance.utilisateur = utilisateur
        return super().save(commit=commit)





