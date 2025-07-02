from django import forms
from .models import (
    TypeFormation,
    Specification,
    Parcours,
    Formation,
    Classe,
    AnneeAcademique
)

class TypeFormationForm(forms.ModelForm):
    class Meta:
        model = TypeFormation
        fields = '__all__'
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 10}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
        }

class SpecificationForm(forms.ModelForm):
    class Meta:
        model = Specification
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'})
        }



class ParcoursForm(forms.ModelForm):
    class Meta:
        model = Parcours
        fields = '__all__'
        widgets = {
            'type_formation': forms.Select(attrs={'class': 'form-control'}),
            'specification': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'code_serie': forms.TextInput(attrs={'class': 'form-control'}),
            'structure_classes': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: ["PS","MS","GS"]'
            }),
            'diplome_final': forms.TextInput(attrs={'class': 'form-control'}),
            'duree_fixe': forms.NumberInput(attrs={'class': 'form-control'})
        }

    def clean_structure_classes(self):
        # Valider que structure_classes est un JSON valide et une liste
        data = self.cleaned_data['structure_classes']
        import json
        try:
            value = json.loads(data) if isinstance(data, str) else data
        except Exception:
            raise forms.ValidationError("Le format doit être une liste JSON valide (ex: [\"PS\", \"MS\", \"GS\"])")
        if not isinstance(value, list):
            raise forms.ValidationError("La structure des classes doit être une liste.")
        return value

class FormationForm(forms.ModelForm):
    class Meta:
        model = Formation
        fields = '__all__'
        widgets = {
            'parcours': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'duree': forms.NumberInput(attrs={'class': 'form-control'}),
            'est_professionnelle': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'avec_classes': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for parcours in self.fields['parcours'].queryset:
            self.fields['parcours'].widget.choices.queryset = self.fields['parcours'].queryset
            self.fields['parcours'].widget.choices.field.empty_label = None
            self.fields['parcours'].widget.attrs.update({'data-type-formation': parcours.type_formation.nom})

class ClasseForm(forms.ModelForm):
    class Meta:
        model = Classe
        fields = '__all__'
        widgets = {
            'formation': forms.Select(attrs={'class': 'form-control'}),
            'annee_academique': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'ordre': forms.NumberInput(attrs={'class': 'form-control'})
        }

class AnneeAcademiqueForm(forms.ModelForm):
    class Meta:
        model = AnneeAcademique
        fields = '__all__'
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'date_fin': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
