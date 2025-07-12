from django import forms
from .models import *
from Formation.models import Parcours,Classe,AnneeAcademique
# from Utilisateur.models import
from Utilisateur.forms import CustomUserCreationForm





class FraisForm(forms.ModelForm):
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Entrez la description ici...'})
    )
    class Meta:
        model = Frais
        fields = '__all__'
        widgets = {
            'montant': forms.NumberInput(attrs={'step': '0.01'})
        }

    def clean_montant(self):
        cleaned_data = super().clean()
        libelle = cleaned_data.get('libelle')
        description = cleaned_data.get('description')
        montant = self.cleaned_data.get('montant')

        if libelle == 'AUTRE' and not description:
            raise forms.ValidationError("La description est obligatoire quand le libellé est 'Autre'.")

        if isinstance(montant, str):
            try:
                return Decimal(montant.replace(',', '.'))
            except:
                raise forms.ValidationError("Format invalide. Exemple: 15000.50")
        return montant

class InscriptionForm(forms.ModelForm):
    class Meta:
        model = Inscription
        fields = '__all__'
        widgets = {
            'date_inscription': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Retirer "inscrit" des choix de statut
        self.fields['statut'].choices = [
            (val, label)
            for val, label in self.fields['statut'].choices
            if val != Inscription.STATUT_INSCRIT
        ]

        # Appliquer Bootstrap à tous les champs
        for champ, field in self.fields.items():
            if champ != 'statut':
                field.widget.attrs['class'] = 'form-control'


class PaiementForm(forms.ModelForm):
    class Meta:
        model = Paiement
        fields = '__all__'
        widgets = {
            'date_paiement': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class DevoirForm(forms.ModelForm):
    class Meta:
        model = Devoir
        fields = '__all__'
        widgets = {
            'date_rendu': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'

class EtudiantInscriptionForm(forms.ModelForm):
    parcours = forms.ModelChoiceField(queryset=Parcours.objects.all())
    classe = forms.ModelChoiceField(queryset=Classe.objects.all())
    annee_academique = forms.ModelChoiceField(queryset=AnneeAcademique.objects.all())

    class Meta:
        model = Etudiant
        fields = '__all__'
        exclude = ['utilisateur']  # on ne le montre pas dans le formulaire
    def __init__(self, *args, **kwargs):
        self.utilisateur_data = kwargs.pop('utilisateur_data', None)
        super().__init__(*args, **kwargs)
        self.utilisateur_form = CustomUserCreationForm(
            data=self.utilisateur_data,
            prefix='utilisateur',
            role = 'ETUDIANT'
        )

    def is_valid(self):
        print("==> Validation EtudiantInscriptionForm")
        valid = super().is_valid()
        utilisateur_valid = self.utilisateur_form.is_valid()
        print("==> Étudiant Form valid ?", valid)
        print("==> Utilisateur Form valid ?", utilisateur_valid)
        if not valid:
            print("==> Erreurs Étudiant :", self.errors)
        if not utilisateur_valid:
            print("==> Erreurs Utilisateur :", self.utilisateur_form.errors)
        return valid and utilisateur_valid

    def save(self, commit=True):
        print("==> Sauvegarde EtudiantInscriptionForm")
        utilisateur = self.utilisateur_form.save(commit=commit)
        print("==> Utilisateur sauvegardé :", utilisateur)

        etudiant = super().save(commit=False)
        etudiant.utilisateur = utilisateur
        if commit:
            etudiant.save()
            print("==> Étudiant sauvegardé :", etudiant)

            inscription = Inscription.objects.create(
                etudiant=etudiant,
                parcours=self.cleaned_data['parcours'],
                classe=self.cleaned_data['classe'],
                annee_academique=self.cleaned_data['annee_academique'],
                statut=Inscription.STATUT_INSCRIT
            )
            print("==> Inscription créée :", inscription)
        return etudiant