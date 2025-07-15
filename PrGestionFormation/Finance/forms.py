from django import forms
from .models import *
from Formation.models import Parcours,Classe,AnneeAcademique
from Utilisateur.forms import CustomUserCreationForm
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory





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
        fields = [
            'statut',
            'etudiant',
            'annee_academique',
            'parcours',
            'classe',
            'resultat_annee_precedente',
            'motif',
            'date_evenement',
            'duree',
            'Etablissement_accuiel',
        ]
        widgets = {
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'etudiant': forms.Select(attrs={'class': 'form-select select2'}),
            'annee_academique': forms.Select(attrs={'class': 'form-select'}),
            'parcours': forms.Select(attrs={'class': 'form-select'}),
            'classe': forms.Select(attrs={'class': 'form-select'}),
            'resultat_annee_precedente': forms.TextInput(attrs={'class': 'form-control'}),
            'motif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_evenement': forms.DateTimeInput(
                format='%d/%m/%Y %H:%M',
                attrs={
                    'class': 'form-control datetimepicker',
                    'placeholder': 'JJ/MM/AAAA HH:MM',
                    'data-inputmask-alias': 'datetime',
                    'data-inputmask-inputformat': 'dd/mm/yyyy HH:MM',
                }
            ),
            'duree': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'Etablissement_accuiel': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Supprimer le statut "inscrit" s’il ne doit pas être choisi manuellement
        self.fields['statut'].choices = [
            (val, label) for val, label in self.fields['statut'].choices
            if val != Inscription.STATUT_INSCRIT
        ]

        # Ajouter la classe Bootstrap à tous les champs (sécurité)
        for name, field in self.fields.items():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean(self):
        cleaned_data = super().clean()
        etudiant = cleaned_data.get('etudiant')
        annee = cleaned_data.get('annee_academique')
        statut = Inscription.STATUT_INSCRIT
        statut_sel = cleaned_data.get('statut')
        if statut == statut_sel :
            if etudiant and annee:
                if Inscription.objects.filter(etudiant=etudiant, annee_academique=annee).exists():
                    raise ValidationError("⚠️ Cet étudiant est déjà inscrit pour cette année académique.")

DocumentInscriptionFormSet = inlineformset_factory(
    Inscription,
    DocumentInscription,
    fields=['type_document', 'fichier'],
    extra=0,  # On génère via JS les documents nécessaires
    can_delete=True,
    widgets={
        'type_document': forms.Select(attrs={'class': 'form-select document-type'}),
        'fichier': forms.FileInput(attrs={'class': 'form-control'}),
    }
)

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