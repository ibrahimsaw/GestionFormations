from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render ,redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
from Formation.models import AnneeAcademique, Classe,Formation
# from etablissements.views import BaseContextView, data
from config.globals import *
from django.db import transaction
from decimal import Decimal




class ScolariteBaseView(BaseContextView):
    model_type = None
    template_form = 'Scolarite/formulaire.html'
    template_list = 'Scolarite/liste.html'
    template_detail = 'Scolarite/detail.html'
    template_delete = 'Scolarite/confirm_delete.html'

    model_mapping = {
        'frais': (Frais, FraisForm, "Frais"),
        'paiement': (Paiement, PaiementForm, "Paiement"),
        'inscription': (Inscription, EtudiantInscriptionForm, "Inscription"),
        'reinscription': (Inscription, InscriptionForm, "Réinscription"),
    }

    def dispatch(self, request, *args, **kwargs):
        view_name = request.resolver_match.view_name
        # print(view_name)

        if view_name == 'finance:scolarite-create':
            tample = self.template_form
        elif view_name == 'finance:scolarite-list':
            tample = self.template_list
        elif view_name == 'finance:scolarite-detail':
            tample = self.template_detail
        elif view_name == 'finance:scolarite-update':
            tample = self.template_form
        elif view_name == 'finance:scolarite-delete':
            tample = self.template_delete
        else:
            tample = self.template_form
        self.model_type = kwargs.get('type')
        print(self.model_type)
        if self.model_type not in self.model_mapping:
            return render(request, tample, {'data': data, 'erreur': "Type inconnu."})
        return super().dispatch(request, *args, **kwargs)

    def get_model_class(self):
        return self.model_mapping[self.model_type][0]

    def get_form_class(self):
        return self.model_mapping[self.model_type][1]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _, _, titre = self.model_mapping[self.model_type]
        context.update({
            'role' : self.model_type,
            'titre_formulaire': f"{titre} - Formulaire",
            'titre_liste': f"Liste des {titre}s",
            'titre_detail': f"Détails {titre}",
            'titre_suppression': f"Supprimer {titre}",
            'fonction': f"Créer un {titre}",
            'bouttonvalide': "Valider",
            'model_type': self.model_type
        })
        return context



from django.shortcuts import redirect
from django.db import transaction
from decimal import Decimal

class ScolariteCreateView(ScolariteBaseView, CreateView):

    def dispatch(self, request, *args, **kwargs):
        self.model_type = self.kwargs.get('type')  # Assure-toi que dans urls c’est 'type'
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        return [self.template_form]

    def get_queryset(self):
        return self.get_model_class().objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.model_type == 'frais':
            context['annees'] = AnneeAcademique.objects.all()
            context['formations'] = []
            context['classes'] = []
        return context

    def get_success_url(self):
        if self.model_type == 'frais':
            return reverse('finance:scolarite-list', kwargs={'type': 'frais'})
        else:
            return reverse('finance:scolarite-detail', kwargs={
                'type': self.model_type,
                'pk': self.object.pk
            })


    def post(self, request, *args, **kwargs):
        self.object = None

        if self.model_type == 'frais':
            print("📥 POST reçu pour les frais")
            libelle = request.POST.get('libelle')
            annee_id = request.POST.get('annee_id')
            formation_id = request.POST.get('formation_id')
            description = request.POST.get('description', '').strip() or None
            recurrent = request.POST.get('recurrent') == 'on'

            print(f"🔹 Libellé : {libelle}")
            print(f"🔹 Année : {annee_id}, Formation : {formation_id}")
            print(f"🔹 Description : {description}")
            print(f"🔹 Récurrent : {recurrent}")

            if not annee_id or not formation_id:
                messages.error(request, "Veuillez sélectionner une année et une formation")
                return self.form_invalid(self.get_form())

            classes = Classe.objects.filter(
                annee_academique_id=annee_id,
                formation_id=formation_id
            )

            print(f"📚 {classes.count()} classes récupérées")

            created_count = 0
            updated_count = 0

            with transaction.atomic():
                for classe in classes:
                    montant_str = request.POST.get(f'montant_{classe.id}')
                    print(f"\n➡️ Classe : {classe.nom} | Montant : {montant_str}")

                    if montant_str:
                        try:
                            montant = Decimal(montant_str.replace(',', '.'))
                            if montant > Decimal('0'):
                                frais = Frais.objects.filter(
                                    libelle=libelle,
                                    classe=classe,
                                    description=description
                                ).first()

                                if frais:
                                    print("✏️ Mise à jour d'un enregistrement existant")
                                    frais.montant = montant
                                    frais.recurrent = recurrent
                                    frais.save()
                                    updated_count += 1
                                else:
                                    print("➕ Création d'un nouvel enregistrement")
                                    Frais.objects.create(
                                        libelle=libelle,
                                        montant=montant,
                                        classe=classe,
                                        recurrent=recurrent,
                                        description=description
                                    )
                                    created_count += 1
                        except Exception as e:
                            print(f"⚠️ Erreur pour la classe {classe.nom} : {e}")
                            continue

            messages.success(request, f"{created_count} frais créés, {updated_count} frais mis à jour.")
            return redirect('finance:scolarite-list', type='frais')

        print("🔁 Redirection vers post parent")
        return super().post(request, *args, **kwargs)


class ScolariteListView(ScolariteBaseView, ListView):
    def get_template_names(self):
        return [self.template_list]

    def get_queryset(self):
        return self.get_model_class().objects.all()


class ScolariteDetailView(ScolariteBaseView, DetailView):
    def get_template_names(self):
        return [self.template_detail]

    def get_queryset(self):
        return self.get_model_class().objects.all()


class ScolariteUpdateView(ScolariteBaseView, UpdateView):
    def get_template_names(self):
        return [self.template_form]

    def get_queryset(self):
        return self.get_model_class().objects.all()

    def get_success_url(self):
        return reverse('scolarite-detail', kwargs={'type': self.model_type, 'pk': self.object.pk})


class ScolariteDeleteView(ScolariteBaseView, DeleteView):
    def get_template_names(self):
        return [self.template_delete]

    def get_queryset(self):
        return self.get_model_class().objects.all()

    def get_success_url(self):
        return reverse('scolarite-list', kwargs={'type': self.model_type})
