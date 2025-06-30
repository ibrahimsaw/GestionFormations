from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView,DetailView
from django.urls import reverse_lazy,reverse
from django.http import Http404
from collections import defaultdict
from .models import *
from .forms import *
import json
from django.contrib.auth import authenticate ,login
from django.views.decorators.csrf import csrf_protect
from config.globals import *
from Utilisateur.models import Etudiant,Utilisateur


# Create your views here
class Bienvenu(BaseContextView, TemplateView):
    template_name = 'Accuiel/bienvenu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donne'] = 'autre donnée'
        return context






class UniversalCreateView(BaseContextView, CreateView):
    template_name = 'Formation/formulaire.html'
    model_type = None

    model_mapping = {
        'formation': (Formation, FormationForm, "Formation"),
        'parcours': (Parcours, ParcoursForm, "Parcours"),
        'annee': (AnneeAcademique, AnneeAcademiqueForm, "Année Académique"),
        'classe': (Classe, ClasseForm, "Classe"),
    }

    def dispatch(self, request, *args, **kwargs):
        self.model_type = kwargs.get('type')
        if self.model_type not in self.model_mapping:
            return render(request, 'Formation/formulaire.html', {'data': data})
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        return self.model_mapping[self.model_type][1]

    def get_queryset(self):
        return self.model_mapping[self.model_type][0].objects.all()

    def form_valid(self, form):
        print("✅ Formulaire valide pour :", self.model_type)

        # ✅ Afficher les champs soumis dans la console
        print("📩 Données POST reçues :")
        for key, value in self.request.POST.items():
            print(f"   → {key}: {value}")

        print("📋 Champs nettoyés (cleaned_data) :")
        for field, value in form.cleaned_data.items():
            print(f"   ✔ {field}: {value}")

        # Traitement par défaut
        response = super().form_valid(form)
        instance = form.instance

        # Logique post-validation spécifique
        if self.model_type == 'formation' and instance.avec_classes:
            annee_active = AnneeAcademique.objects.filter(classes_standards_creees=True).first()
            if annee_active:
                print("🛠 Création automatique des classes pour la formation")
                instance.creer_classes(annee_active)

        elif self.model_type == 'annee' and self.request.POST.get('creer_classes') == 'on':
            print("🛠 Création des classes standards pour l'année")
            instance.creer_classes_standards()

        return response

    def get_success_url(self):
        return reverse('formation:universal-detail', kwargs={
            'type': self.model_type,
            'pk': self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _, _, titre = self.model_mapping[self.model_type]
        context['titre_formulaire'] = titre
        context['role'] = self.model_type
        context['model_type'] = self.model_type
        context['fonction'] = "Création de " + titre
        context['bouttonvalide'] = "Créer"
        context['annee_durees'] = range(1, 11)
        type_formations = list(TypeFormation.objects.values('id', 'code', 'nom', 'liste_classe'))
        specification = list(Specification.objects.values('id', 'code', 'nom'))
        context['specifications_json'] = json.dumps(specification)
        context['type_formations_json'] = json.dumps(type_formations)

        return context


class UniversalListView(BaseContextView, ListView):
    template_name = 'Formation/liste.html'
    context_object_name = 'items'
    paginate_by = 10
    model_type = None

    model_mapping = {
        'formation': (Formation, "Liste des Formations", lambda: Formation.objects.all().order_by('parcours__type_formation', 'nom')),
        'parcours': (Parcours, "Liste des Parcours", lambda: Parcours.objects.all().order_by('type_formation', 'nom')),
        'annee': (AnneeAcademique, "Liste des Années Académiques", lambda: AnneeAcademique.objects.all().order_by('-date_debut')),
        'classe': (Classe, "Liste des Classes", lambda: Classe.objects.all().order_by('formation__parcours__type_formation', 'ordre')),
    }

    def dispatch(self, request, *args, **kwargs):
        self.model_type = kwargs.get('type')
        if self.model_type not in self.model_mapping:
            return render(request, 'Formation/liste.html', {'data': data})
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model_mapping[self.model_type][2]()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        _, titre, _ = self.model_mapping[self.model_type]
        context['model_type'] = self.model_type
        context['titre'] = titre
        context['role'] = self.model_type
        return context




class UniversalDetailView(DetailView):
    template_name = 'Formation/detail.html'
    model_type = None

    model_mapping = {
        'formation': (Formation, "Détail de la Formation"),
        'parcours': (Parcours, "Détail du Parcours"),
        'annee': (AnneeAcademique, "Détail de l'Année Académique"),
        'classe': (Classe, "Détail de la Classe"),
    }

    def dispatch(self, request, *args, **kwargs):
        self.model_type = kwargs.get('type')
        if self.model_type not in self.model_mapping:
            return render(request, self.template_name, {'error': "Type invalide"})
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        model_class, _ = self.model_mapping[self.model_type]
        return get_object_or_404(model_class, pk=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_class, titre = self.model_mapping[self.model_type]
        context['model_type'] = self.model_type
        context['titre'] = titre
        context['role'] = self.model_type

        obj = self.get_object()
        context['obj'] = obj

        if self.model_type == 'parcours':
            parcours = self.object
            context['structure_classes_affiche'] = parcours.structure_classes or []
            context['titre_page'] = f"Détail du parcours : {parcours.nom}"
            formations = obj.formations.all()
            data = []

            for formation in formations:
                classes_grouped = defaultdict(list)

                for classe in formation.classes.all():
                    annee = classe.annee_academique.nom if classe.annee_academique else "Non définie"
                    classes_grouped[annee].append(classe)

                classes_data = []
                for annee in sorted(classes_grouped):
                    classes_de_l_annee = classes_grouped[annee]

                    classes_avec_nb = []
                    for classe in classes_de_l_annee:
                        nb_etudiants_classe = Etudiant.objects.filter(
                            inscriptions__classe=classe,
                            inscriptions__annee_academique=classe.annee_academique
                        ).distinct().count()
                        classes_avec_nb.append({
                            'classe': classe,
                            'nb_etudiants': nb_etudiants_classe
                        })

                    nb_etudiants_annee = Etudiant.objects.filter(
                        inscriptions__classe__in=classes_de_l_annee,
                        inscriptions__annee_academique__nom=annee
                    ).distinct().count()

                    classes_data.append({
                        'annee': annee,
                        'nb_etudiants_annee': nb_etudiants_annee,
                        'classes': classes_avec_nb
                    })

                data.append({
                    'formation': formation,
                    'classes_par_annee': classes_data
                })

            context['formations_et_classes'] = data

        elif self.model_type == 'formation':
            classes = obj.classes.all()
            classes_par_annee = defaultdict(list)

            for classe in classes:
                annee = classe.annee_academique.nom if classe.annee_academique else "Non définie"
                nb_etudiants = Etudiant.objects.filter(inscriptions__classe=classe).distinct().count()

                classes_par_annee[annee].append({
                    'classe': classe,
                    'nb_etudiants': nb_etudiants
                })

            classes_data = [{'annee': annee, 'classes': cls_list} for annee, cls_list in classes_par_annee.items()]
            context['classes'] = classes_data
            context['classess'] = classes

        elif self.model_type == 'annee':
            classes = Classe.objects.filter(annee_academique=obj).select_related('formation').order_by('formation__nom', 'nom')
            nb_etudiants_total = Etudiant.objects.filter(inscriptions__annee_academique=obj).distinct().count()
            formations_dict = defaultdict(list)

            for classe in classes:
                nb_etudiants = Etudiant.objects.filter(inscriptions__classe=classe, inscriptions__annee_academique=obj).distinct().count()
                formations_dict[classe.formation].append({
                    'classe': classe,
                    'nb_etudiants': nb_etudiants
                })

            data = []
            for formation, classes_info in formations_dict.items():
                data.append({
                    'formation': formation,
                    'classes': classes_info
                })

            context['nb_etudiants_total'] = nb_etudiants_total
            context['annee'] = obj.nom if hasattr(obj, 'nom') else "Nom non défini"
            context['formations_et_classes'] = data

        elif self.model_type == 'classe':
            nb_etudiants = Etudiant.objects.filter(inscriptions__classe=obj).distinct().count()
            etudiants = Etudiant.objects.filter(inscriptions__classe=obj).distinct()

            context['etudiants'] = etudiants
            context['nb_etudiants'] = nb_etudiants or 0
            context['formation'] = obj.formation if obj.formation else "Non définie"
            context['annee'] = obj.annee_academique.nom if obj.annee_academique else "Non définie"
            context['parcours'] = obj.formation.parcours if obj.formation and obj.formation.parcours else "Non défini"

        return context



