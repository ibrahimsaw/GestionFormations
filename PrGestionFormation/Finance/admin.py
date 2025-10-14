from django.contrib import admin
from .forms import *
from .models import *


@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'etudiant',
   'type_formation',
    'parcours',
    'classe',
    'annee_academique',
    'date_inscription',
    'statut',
    )





@admin.register(Frais)
class FraisAdmin(admin.ModelAdmin):
    list_display = ('libelle_display', 'montant_display', 'classe', 'recurrent')
    list_filter = ('libelle', 'recurrent', 'classe__formation')
    search_fields = ('libelle', 'classe__nom')

    def libelle_display(self, obj):
        return obj.get_libelle_display()

    libelle_display.short_description = 'Libellé'

    def montant_display(self, obj):
        return f"{obj.montant:.2f} FCFA"

    montant_display.short_description = 'Montant'

    def save_model(self, request, obj, form, change):
        if isinstance(obj.montant, str):
            obj.montant = Decimal(obj.montant.replace(',', '.'))
        super().save_model(request, obj, form, change)

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'frais', 'montant', 'methode', 'reference', 'date_paiement')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('titre', 'type', 'auteur', 'date_upload')

@admin.register(Devoir)
class DevoirAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_rendu', 'est_rendu')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'type', 'date_envoi', 'est_lu')
