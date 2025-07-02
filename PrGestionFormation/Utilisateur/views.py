from django.contrib.auth import authenticate ,login
from django.views.decorators.csrf import csrf_protect
from config.globals import *
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse, reverse_lazy,NoReverseMatch
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string
from django.db import transaction
from django.utils import timezone
from itertools import chain
from operator import attrgetter
from decimal import Decimal
from .models import *
from .forms import *
from Formation.models import AnneeAcademique, Classe
from .forms import SpecialiteForm
import logging
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView


# Create your views here.


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        matricule = request.POST.get('matricule')
        password = request.POST.get('password')
        remember = request.POST.get('remember-me')  # 'on' si coché

        user = authenticate(request, matricule=matricule, password=password)

        if user is not None:
            login(request, user)

            if not remember:
                # Expire à la fermeture du navigateur
                request.session.set_expiry(0)
            else:
                # Expire dans 2 semaines
                request.session.set_expiry(1209600)

            return redirect('bienvenu')
        else:
            messages.error(request, "Matricule ou mot de passe incorrect.")
            return render(request, 'login/login.html', {"data": data,'titre_page': 'Connection',})
    else:
        return render(request, 'login/login.html', {"data": data,'titre_page': 'Connection',})


class Bienvenu(BaseContextView, TemplateView):
    template_name = 'Accuiel/bienvenu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donne'] = 'autre donnée'
        context['titre_page'] = 'Bienvenue'
        return context



def custom_403(request, exception):
    return render(request, 'errors/403.html', {'exception': exception, 'path': request.path, 'user': request.user}, status=403)

def custom_404(request, exception):
    return render(request, 'errors/404.html', {'exception': exception, 'path': request.path,'data':data}, status=404)

def custom_500(request):
    return render(request, 'errors/500.html', {'path': ''}, status=500)


class ChangerMotDePasseView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'Utilisateur/Modification_Motdepasse/changer_mot_de_passe.html'
    success_url = reverse_lazy('accueil')

    def form_valid(self, form):
        self.request.user.doit_changer_mot_de_passe = False
        self.request.user.save()
        return super().form_valid(form)



class UtilisateurBaseView(BaseContextView):
    """Classe de base pour toutes les vues utilisateur avec gestion des templates dynamiques."""

    model_type = None
    view_name = ""
    template_form = 'Utilisateur/formulaire.html'
    template_list = 'Utilisateur/listes.html'
    template_detail = 'Utilisateur/details.html'
    template_delete = 'Utilisateur/confirm_delete.html'
    message = ""
    page = ""
    bouton = ""
    titre_page = ""
    path = ""
    breadcrumb = []

    model_mapping = {
        'utilisateur': (Utilisateur, CustomUserCreationForm,CustomUserChangeForm, "Utilisateur"),
        'admin': (AdminSysteme, AdminSystemeForm,AdminSystemeUpdateForm, "Administrateur Système"),
        'agent': (AgentAdministration, AgentAdministrationForm, AgentAdministrationUpdateForm, "Agent d'Administration"),
        'enseignant': (Enseignant, EnseignantForm, EnseignantUpdateForm, "Enseignant"),
        'etudiant': (Etudiant, EtudiantInscriptionForm, EtudiantUpdateForm, "Étudiant"),
        'parent': (Parent, ParentForm, ParentUpdateForm, "Parent d'étudiant"),
    }

    def dispatch(self, request, *args, **kwargs):
        self.message = getattr(self, 'message', '')
        self.view_name = request.resolver_match.view_name.split(':')[-1]
        self.model_type = kwargs.get('role')

        self.message += f"[dispatch] View name: {self.view_name}\n"
        self.message += f"[dispatch] Type reçu : {self.model_type}\n"

        type_name = self.get_type_name()
        suffix = 'es' if type_name.endswith('t') else 's'

        # Configuration combinée : label + template
        view_config = {
            'utilisateur_create': {
                'label': 'Création',
                'template': self.template_form,
                'bouton':'Créer le compte',
                'titre_page': f"Création un {type_name}" if type_name != "Nom inconnu" else "Création"
            },
            'utilisateur_list': {
                'label': 'Liste',
                'template': self.template_list,
                'bouton': '',
                'titre_page': f"Liste des {type_name}{suffix}" if type_name != "Nom inconnu" else "Liste",
            },
            'utilisateur_detail': {
                'label': 'Détails',
                'template': self.template_detail,
                'bouton': '',
                'titre_page': f"Détails d'un {type_name}" if type_name != "Nom inconnu" else "Détails",
            },
            'utilisateur_modifier': {
                'label': 'Modification',
                'template': self.template_form,
                'bouton': 'Enregistrer la modification',
                'titre_page': f"Modification d'un {type_name}" if type_name != "Nom inconnu" else "Modification",
            },
            'utilisateur_delete': {
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
            print('name :', part.capitalize())
            print('url :',cumulative_path)
            self.breadcrumb.append({
            'name': part.capitalize(),
            'url': cumulative_path,
            'is_first': i == 0,
            'is_last': i == len(path) - 1
            })
        print("Chemin de la requête :", request.path)
        print("Méthode HTTP :", request.method)
        print("Nom de la vue :", request.resolver_match.view_name)
        print("Paramètre GET 'name' :", request.GET.get('name'))


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
        print(self.message)
        return super().dispatch(request, *args, **kwargs)



    def get_model_class(self):
        model_class = self.model_mapping[self.model_type][0]
        self.message += f"[get_model_class] Classe du modèle : {model_class}\n"
        return model_class

    def get_form_class(self):
        form_class = self.model_mapping[self.model_type][1]
        self.message += f"[get_form_class] Classe du formulaire : {form_class}\n"
        return form_class

    def get_form_class_by_type(self, update=False):
        form_class = self.model_mapping[self.model_type][2 if update else 1]
        self.message += f"[get_form_class_by_type] Formulaire {'update' if update else 'create'} : {form_class}\n"
        return form_class

    def get_type_name(self):
        type_info = self.model_mapping.get(self.model_type)
        if type_info:
            type_name = type_info[-1]
        else:
            type_name = "Nom inconnu"
            self.message += f"[get_type_name] Type non reconnu : {self.model_type}\n"

        self.message += f"[get_type_name] Nom du type : {type_name}\n"
        return type_name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_name = self.get_type_name()

        context.update({
            'bouton' : self.bouton,
            'path' : self.path,
            'titre_page' : self.titre_page,
            'role_utilisateur': type_name,
            'model_type': self.model_type,
            'navbar': navbar,  # Assure-toi que 'navbar' est bien défini globalement
            'page': self.page,
            'message_debug': self.message,  # Optionnel : pour affichage dans le template
            'breadcrumb': self.breadcrumb,
        })

        # Debug console log
        # print("[get_context_data] Contexte envoyé :")
        # for key, value in context.items():
        #     if key == "form" and value and value.errors:
        #         print("[get_context_data] Formulaire avec erreurs :")
        #         print("    form.errors :", value.errors)
        #     else:
        #         print(f"    {key}: {value}")
        return context





class UtilisateurCreateView(UtilisateurBaseView, CreateView):
    messagecreate = ""
    def get_template_names(self):
        self.messagecreate +=f"[UtilisateurCreateView] Template utilisé : {self.template_form}"  # DEBUG
        return [self.template_form]

    def get_queryset(self):
        self.messagecreate +="==> get_queryset appelé"
        return self.get_model_class().objects.all()

    def get_form_kwargs(self):
        self.messagecreate +="==> get_form_kwargs appelé"
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            self.messagecreate +="==> Données POST reçues"
            kwargs['utilisateur_data'] = self.request.POST
        return kwargs



    def form_valid(self, form):
        self.messagecreate +="==> form_valid appelé"

        if hasattr(form, 'utilisateur_form'):
            self.messagecreate +="==> utilisateur_form détecté"
            if form.utilisateur_form.is_valid():
                self.messagecreate +="==> utilisateur_form valide"
                utilisateur = form.utilisateur_form.save()

                form.instance.utilisateur = utilisateur
                self.object = form.save()
                self.messagecreate +="==> Form principal sauvegardé avec utilisateur"

                return redirect(self.get_success_url())
            else:
                self.messagecreate +="==> utilisateur_form invalide"
                print(form.utilisateur_form.errors)
                return self.form_invalid(form)
        else:
            print("==> Pas de utilisateur_form")
            return self.form_invalid(form)

    def form_invalid(self, form):
        print("==> erreurs du formulaire principal :", form.errors)
        if hasattr(form, 'utilisateur_form'):
            print("==> erreurs du sous-formulaire utilisateur :", form.utilisateur_form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        self.messagecreate +="==> Redirection vers le détail de l'utilisateur"
        return reverse('utilisateur:utilisateur_detail', kwargs={
            'role': self.model_type,
            'pk': self.object.pk
        })

    def get_context_data(self, **kwargs):
        self.messagecreate +="==> get_context_data appelé"
        context = super().get_context_data(**kwargs)

        form = kwargs.get('form') or self.get_form()
        context['utilisateur_form'] = getattr(form, 'utilisateur_form', None)

        if self.model_type == 'enseignant':
            context['specialites'] = Specialite.objects.all()
            context['specialite_form'] = SpecialiteForm(prefix='specialite')
        elif self.model_type == 'parent':
            context['etudiants'] = Etudiant.objects.all()

        return context

    print(messagecreate)




@require_POST
@csrf_exempt  # À n'utiliser qu'en développement, remplacer par un vrai token en production
def ajouter_specialite(request):
    try:
        data = json.loads(request.body)
        nom = data.get('nom')

        if not nom:
            return JsonResponse({
                "success": False,
                "error": "Le nom de la spécialité est requis"
            }, status=400)

        # Créer la nouvelle spécialité
        specialite = Specialite.objects.create(nom=nom)

        return JsonResponse({
            "success": True,
            "id": specialite.id,
            "nom": specialite.nom
        })

    except Exception as e:
        return JsonResponse({
            "success": False,
            "error": str(e)
        }, status=400)



class UtilisateurListView(UtilisateurBaseView, ListView):
    def get_template_names(self):
            return [self.template_list]
    context_object_name = 'agents'
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        self.model_type = kwargs.get('role')
        if 'pdf' in request.GET:
            self.paginate_by = None
        else:
            self.paginate_by = 10

        print(self.model_mapping)
        print(self.model_type)
        erreur = "Type inconnu."
        if self.model_type not in self.model_mapping:
            print(erreur)
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get('q')
        periode = self.request.GET.get('periode')

        def filter_queryset(qs, has_utilisateur=False):
            if q:
                qs = qs.filter(utilisateur__matricule__icontains=q) if has_utilisateur else qs.filter(matricule__icontains=q)

            if periode == 'semaine':
                date_limit = timezone.now() - timezone.timedelta(days=7)
            elif periode == 'mois':
                now = timezone.now()
                return qs.filter(
                    utilisateur__date_inscription__year=now.year,
                    utilisateur__date_inscription__month=now.month
                ) if has_utilisateur else qs.filter(
                    date_inscription__year=now.year,
                    date_inscription__month=now.month
                )
            elif periode == '3mois':
                date_limit = timezone.now() - timezone.timedelta(days=90)
            else:
                date_limit = None

            if date_limit:
                qs = qs.filter(utilisateur__date_inscription__gte=date_limit) if has_utilisateur else qs.filter(date_inscription__gte=date_limit)
            return qs

        # Si aucun type spécifique, retourner tous les types
        if not self.model_type or self.model_type not in self.model_mapping:
            queryset_list = []
            for model, _, _ in self.model_mapping.values():
                has_utilisateur = model.__name__ != 'Utilisateur'
                qs = model.objects.all()
                qs = filter_queryset(qs, has_utilisateur)
                queryset_list.append(qs)
            combined = sorted(
                chain(*queryset_list),
                key=lambda obj: obj.utilisateur.date_inscription if hasattr(obj, 'utilisateur') else obj.date_inscription,
                reverse=True
            )
            return combined

        model = self.get_model_class()
        has_utilisateur = model.__name__ != 'Utilisateur'
        qs = model.objects.all()
        return filter_queryset(qs, has_utilisateur)




class UtilisateurDetailView(UtilisateurBaseView, DetailView):
    def get_template_names(self):
        return [self.template_detail]
    context_object_name = 'agent'  # Change ce nom si nécessaire

    def get_queryset(self):
        model = self.get_model_class()
        return model.objects.all()



class UtilisateurUpdateView(UtilisateurBaseView, UpdateView):
    def get_template_names(self):
        return [self.template_form]

    def dispatch(self, request, *args, **kwargs):
        self.model_type = (kwargs.get('role') or kwargs.get('type', '')).lower()

        if not self.model_type:
            return render(request, 'error.html', {"error": "Type d'utilisateur non fourni"})

        if self.model_type not in self.model_mapping:
            return render(request, 'error.html', {"error": "Type d'utilisateur invalide"})

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.get_model_class().objects.all()

    def get_form_class(self):
        return self.get_form_class_by_type(update=True)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        utilisateur = self.get_object().utilisateur
        kwargs.update({
            'data': self.request.POST or None,
            'files': self.request.FILES or None,
            'utilisateur_instance': utilisateur,
        })
        return kwargs

    def get_success_url(self):
        return reverse('utilisateur:utilisateur_detail', kwargs={
            'role': self.model_type,
            'pk': self.object.pk
        })

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        titre = self.model_mapping[self.model_type][-1]  # récupère le dernier élément : le nom lisible
        instance = self.get_object()

        if self.request.method == 'POST':
            utilisateur_form = CustomUserChangeForm(
                self.request.POST,
                instance=instance.utilisateur,
                prefix='utilisateur'
            )
        else:
            utilisateur_form = CustomUserChangeForm(
                instance=instance.utilisateur,
                prefix='utilisateur'
            )

        context.update({
            'utilisateur_form': utilisateur_form,
        })

        # Données spécifiques selon le rôle
        if self.model_type == 'enseignant':
            context.update({
                'specialites': Specialite.objects.all(),
                'specialite_form': SpecialiteForm(prefix='specialite'),
            })
        elif self.model_type == 'parent':
            context['etudiants'] = Etudiant.objects.all()

        return context

    def post(self, request, *args, **kwargs):
        print("==== POST reçu ====")
        self.object = self.get_object()
        form = self.get_form()
        utilisateur_form = getattr(form, 'utilisateur_form', None)

        # Forcer l'évaluation des erreurs
        _ = form.errors
        _ = utilisateur_form.errors if utilisateur_form else None

        print("Formulaire principal valide ?", form.is_valid())
        print("Formulaire utilisateur valide ?", utilisateur_form.is_valid() if utilisateur_form else "Aucun")
        print("❌ Erreurs du formulaire principal :", form.errors)
        print("❌ Erreurs du formulaire utilisateur :", utilisateur_form.errors if utilisateur_form else "Aucun")

        if form.is_valid() and (utilisateur_form is None or utilisateur_form.is_valid()):
            return self.form_valid(form)
        else:
            return self.form_invalid(form, utilisateur_form)

    def form_valid(self, form):
        if hasattr(form, 'utilisateur_form'):
            utilisateur = form.utilisateur_form.save(commit=True)
            form.instance.utilisateur = utilisateur

        self.object = form.save()
        messages.success(self.request, "Modification enregistrée avec succès")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, utilisateur_form):
        self.add_form_errors_to_messages(self.request, form, 'Formulaire principal')
        self.add_form_errors_to_messages(self.request, utilisateur_form, 'Formulaire utilisateur')

        return self.render_to_response(
            self.get_context_data(
                form=form,
                utilisateur_form=utilisateur_form
            )
        )

    def add_form_errors_to_messages(self, request, form, form_name):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"Erreur ({form_name}) - {field}: {error}")



class UtilisateurDeleteView(UtilisateurBaseView, DeleteView):
    def get_template_names(self):
        print("[UtilisateurDeleteView] get_template_names called")
        return [self.template_delete]

    def get_object(self, queryset=None):
        print(f"[UtilisateurDeleteView] get_object called with kwargs: {self.kwargs}")
        self.model_type = self.kwargs.get('type')
        if not self.model_type:
            raise Http404("Type d'utilisateur non spécifié")

        model_class = self.get_model_class()
        pk = self.kwargs.get('pk')
        try:
            return model_class.objects.get(pk=pk)
        except model_class.DoesNotExist:
            raise Http404("Utilisateur non trouvé")

    def get_context_data(self, **kwargs):
        print("[UtilisateurDeleteView] get_context_data called")
        context = super().get_context_data(**kwargs)
        context.update({
            'type_name': self.get_type_name(),
            'object_name': str(self.object),
            'titre_suppression': f"Supprimer {self.get_type_name()}",
            'type': self.model_type,  # Ajout crucial pour les URLs
            'pk': self.object.pk  # Ajout crucial pour les URLs
        })
        print(f"[UtilisateurDeleteView] Final context: {context}")
        return context

    def delete(self, request, *args, **kwargs):
        print("[UtilisateurDeleteView] delete called")
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, f"{self.get_type_name()} supprimé avec succès")
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        url = reverse('utilisateur_list', kwargs={'type': self.model_type})  # Changé de 'role' à 'type'
        print(f"[UtilisateurDeleteView] Success URL: {url}")
        return url




logger = logging.getLogger(__name__)


@require_GET
def get_parcours_options(request):
    annee_id = request.GET.get('annee_academique')
    logger.info(f"Paramètre année académique reçu: {annee_id}")

    if not annee_id:
        logger.warning("Paramètre annee_academique manquant")
        return JsonResponse({'error': 'Paramètre annee_academique manquant'}, status=400)

    try:
        annee = get_object_or_404(AnneeAcademique, pk=annee_id)
        logger.info(f"Année académique trouvée: {annee}")

        classes = Classe.objects.filter(
            annee_academique=annee
        ).select_related('formation').order_by('formation__nom', 'nom')

        logger.info(f"{classes.count()} classes récupérées pour l'année {annee}")

        formations_dict = {}
        for classe in classes:
            logger.debug(f"Classe: {classe.nom}, Formation: {classe.formation}")
            if classe.formation.id not in formations_dict:
                formations_dict[classe.formation.id] = {
                    'id': classe.formation.id,
                    'nom': str(classe.formation),
                    'classes': []
                }
            formations_dict[classe.formation.id]['classes'].append({
                'id': classe.id,
                'nom': classe.nom
            })

        logger.info(f"{len(formations_dict)} formations préparées pour réponse JSON")
        return JsonResponse(list(formations_dict.values()), safe=False)

    except Exception as e:
        logger.exception("Erreur lors de la récupération des parcours:")
        return JsonResponse({'error': str(e)}, status=500)


@require_GET
def get_classes_options(request):
    """API pour récupérer les classes en fonction du parcours."""
    annee_id = request.GET.get('annee_academique')
    parcours_id = request.GET.get('parcours')

    classes = Classe.objects.filter(
        annee_academique_id=annee_id,
        formation__parcours_id=parcours_id
    ).select_related('formation')

    data = [{'id': c.id, 'nom': f"{c.formation.nom} - {c.nom}"} for c in classes]
    return JsonResponse(data, safe=False)