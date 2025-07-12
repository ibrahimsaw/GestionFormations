from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render ,redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
from Utilisateur.models import Etudiant
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
    message = ""
    page = ""
    bouton = ""
    titre_page = ""
    path = ""
    view_name = ""
    breadcrumb = []
    model_mapping = {
        'frais': (Frais, FraisForm, "Frais"),
        'paiement': (Paiement, PaiementForm, "Paiement"),
        'inscription': (Inscription, EtudiantInscriptionForm, "Statut de l'inscription"),
    }

    def get_model_class(self):
        return self.model_mapping[self.model_type][0]

    def get_form_class(self):
        return self.model_mapping[self.model_type][1]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_name = self.get_type_name()

        context.update({
            'bouton' : self.bouton,
            'buttonName': self.bouton,
            'path' : self.path,
            'titre_page' : self.titre_page,
            'role_utilisateur': type_name,
            'model_type': self.model_type,
            'navbar': navbar,  # Assure-toi que 'navbar' est bien défini globalement
            'page': self.page,
            'message_debug': self.message,  # Optionnel : pour affichage dans le template
            'breadcrumb': self.breadcrumb,
        })
        return context

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     _, _, titre = self.model_mapping[self.model_type]
    #     context.update({
    #         'role' : self.model_type,
    #         'titre_formulaire': f"{titre} - Formulaire",
    #         'titre_liste': f"Liste des {titre}s",
    #         'titre_detail': f"Détails {titre}",
    #         'titre_suppression': f"Supprimer {titre}",
    #         'fonction': f"Créer un {titre}",
    #         'bouttonvalide': "Valider",
    #         'model_type': self.model_type
    #
    #     })
    #     return context

    def get_type_name(self):
        type_info = self.model_mapping.get(self.model_type)
        if type_info:
            type_name = type_info[-1]
        else:
            type_name = "Nom inconnu"
            self.message += f"[get_type_name] Type non reconnu : {self.model_type}\n"

        self.message += f"[get_type_name] Nom du type : {type_name}\n"
        return type_name

    def dispatch(self, request, *args, **kwargs):
        self.message = getattr(self, 'message', '')
        self.view_name = request.resolver_match.view_name.split(':')[-1]
        self.model_type = kwargs.get('type')

        self.message += f"[dispatch] View name: {self.view_name}\n"
        self.message += f"[dispatch] Type reçu : {self.model_type}\n"

        type_name = self.get_type_name()
        suffix = 'es' if type_name.endswith('t') else 's'

        # Configuration combinée : label + template
        view_config = {
            'scolarite-create': {
                'label': 'Création',
                'template': self.template_form,
                'bouton':'Enregistrer la Création',
                'titre_page': f"Création un {type_name}" if type_name != "Nom inconnu" else "Création"
            },
            'scolarite-list': {
                'label': 'Liste',
                'template': self.template_list,
                'bouton': '',
                'titre_page': f"Liste des {type_name}{suffix}" if type_name != "Nom inconnu" else "Liste",
            },
            'scolarite-detail': {
                'label': 'Détails',
                'template': self.template_detail,
                'bouton': '',
                'titre_page': f"Détails d'un {type_name}" if type_name != "Nom inconnu" else "Détails",
            },
            'scolarite-update': {
                'label': 'Modification',
                'template': self.template_form,
                'bouton': 'Enregistrer la modification',
                'titre_page': f"Modification d'un {type_name}" if type_name != "Nom inconnu" else "Modification",
            },
            'scolarite-delete': {
                'label': 'Suppression',
                'template': self.template_delete,
                'bouton': '',
                'titre_page': f"Suppression d'un {type_name}" if type_name != "Nom inconnu" else "Suppression",
            },
        }

        config = view_config.get(self.view_name, {
            'label': 'Action inconnue',
            'template': self.template_form,
            'bouton': 'Valider',
            'titre_page' : 'Page inconnu'
        })

        configtitre_page = view_config.get(self.view_name, {
            'titre_page': config['label']
        })

        self.page = config['label']
        selected_template = config['template']
        self.bouton = config['bouton']
        self.titre_page = configtitre_page['titre_page']
        role = self.model_type
        self.path = request.path
        path = request.path.strip('/').split('/')
        cumulative_path = ''
        self.breadcrumb = []
        for i,part in enumerate(path):
            cumulative_path += '/' + part
            # print('name :', part.capitalize())
            # print('url :',cumulative_path)
            self.breadcrumb.append({
            'name': part.capitalize(),
            'url': cumulative_path,
            'is_first': i == 0,
            'is_last': i == len(path) - 1
            })
        # print("Chemin de la requête :", request.path)
        # print("Méthode HTTP :", request.method)
        # print("Nom de la vue :", request.resolver_match.view_name)
        # print("Paramètre GET 'name' :", request.GET.get('name'))


        self.message += f"[dispatch] Action détectée : {self.page}\n"
        self.message += f"[dispatch] Template sélectionné : {selected_template}\n"

        if self.model_type not in self.model_mapping:
            print('path :',self.path,)
            self.message += "[dispatch] Type inconnu, chargement erreur.\n"
            return render(request, selected_template, {
                'erreur': "Type inconnu.",
                'message': self.message,
                'page': self.page,
                'data': data,
                'titre_page': self.titre_page,
                'page_title': self.page,
                'path': self.path,
            })
        return super().dispatch(request, *args, **kwargs)






class ScolariteCreateView(ScolariteBaseView, CreateView):

    def dispatch(self, request, *args, **kwargs):
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

from django.http import JsonResponse


def frais_par_etudiant(request):
    etudiant_id = request.GET.get('etudiant_id')
    if etudiant_id:
        try:
            etudiant = Etudiant.objects.get(utilisateur_id=etudiant_id)  # ✅ ici
            classe = etudiant.classe_actuelle
            print("classe :",classe)
            frais_list = Frais.objects.filter(classe=classe).values('id', 'libelle', 'montant')
            print("frais_list :", frais_list)
            return JsonResponse(list(frais_list), safe=False)
        except Etudiant.DoesNotExist:
            return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)
    return JsonResponse({'error': 'ID manquant'}, status=400)


# views.py
from django.http import JsonResponse
from .models import Paiement, Etudiant, Frais
from django.db.models import Sum
from decimal import Decimal

def montant_restant_pour_frais(request):
    etudiant_id = request.GET.get("etudiant_id")
    frais_id = request.GET.get("frais_id")

    try:
        etudiant = Etudiant.objects.get(utilisateur_id=etudiant_id)
        frais = Frais.objects.get(id=frais_id)

        total_paye = Paiement.objects.filter(etudiant=etudiant, frais=frais).aggregate(
            total=Sum("montant")
        )["total"] or Decimal("0.00")

        montant_restant = max(frais.montant - total_paye, Decimal("0.00"))

        return JsonResponse({
            "montant_restant": f"{montant_restant:.2f}"
        })
    except (Etudiant.DoesNotExist, Frais.DoesNotExist):
        return JsonResponse({"error": "Etudiant ou frais introuvable"}, status=404)

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required
def search_etudiant_by_matricule(request):
    q = request.GET.get('q', '')
    results = []

    if q:
        queryset = Etudiant.objects.filter(utilisateur__matricule__icontains=q)[:10]
        results = [{
            'id': e.id,
            'matricule': e.utilisateur.matricule,
            'nom': str(e.utilisateur)
        } for e in queryset]

    return JsonResponse(results, safe=False)







class ScolariteListView(ScolariteBaseView, ListView):
    def get_template_names(self):
        return [self.template_list]

    def get_queryset(self):
        return self.get_model_class().objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Génère le dictionnaire { "Inscrit": queryset, ... }
        context['inscriptions_by_statut'] = {
            label: Inscription.objects.filter(statut=code)
            .select_related('etudiant', 'classe', 'annee_academique', 'parcours')
            for code, label in Inscription.STATUT_CHOICES
        }
        context['frais_par_libelle'] = {
            label: Frais.objects.filter(libelle=code)
            .select_related('classe')
            for code, label in Frais.LIBELLE_CHOICES
        }
        context['paiements_par_methode'] = {
            label: Paiement.objects.filter(methode=code)
            .select_related('etudiant', 'frais', 'frais__classe')
            for code, label in Paiement.MethodePaiement.choices
        }

        return context

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
