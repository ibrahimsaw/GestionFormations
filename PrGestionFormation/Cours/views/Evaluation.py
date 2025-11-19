
from .views import *
# ------------------------------------------------------
# Base view générique pour Evaluation
# ------------------------------------------------------
class EvaluationBaseView(BaseContextView):
    model_type = None
    template_form = 'Cours/ajouter/evaluation_form.html'
    template_list = 'Cours/liste/evaluation_list.html'
    template_detail = 'Cours/detail/evaluation_detail.html'
    template_delete = 'Cours/supprimer/evaluation_confirm_delete.html'

    bouton = ""
    titre_page = "Evaluation"
    page = ""
    path = ""
    view_name = ""
    breadcrumb = []

    model_mapping = {
        'evaluation': (Evaluation, EvaluationForm, "Evaluation"),
    }

    def get_model_class(self):
        return self.model_mapping[self.model_type][0]

    def get_form_class(self):
        return self.model_mapping[self.model_type][1]

    def get_type_name(self):
        model_info = self.model_mapping.get(self.model_type)
        return model_info[-1] if model_info else "Type inconnu"

    def setup_configuration(self, request):
        self.view_name = request.resolver_match.view_name.split(':')[-1]
        self.model_type = "evaluation"
        type_name = self.get_type_name()
        suffix = "s"

        config = {
            'evaluation_create': {
                'template': self.template_form,
                'bouton': 'Créer Evaluation',
                'titre_page': f"Créer une {type_name}",
                'label': 'Création',
            },
            'evaluation_list': {
                'template': self.template_list,
                'bouton': '',
                'titre_page': f"Liste des {type_name}{suffix}",
                'label': 'Liste',
            },
            'evaluation_detail': {
                'template': self.template_detail,
                'bouton': '',
                'titre_page': f"Détails de la {type_name}",
                'label': 'Détails',
            },
            'evaluation_update': {
                'template': self.template_form,
                'bouton': 'Modifier Evaluation',
                'titre_page': f"Modifier une {type_name}",
                'label': 'Modification',
            },
            'evaluation_delete': {
                'template': self.template_delete,
                'bouton': '',
                'titre_page': f"Supprimer une {type_name}",
                'label': 'Suppression',
            },
        }

        selected = config.get(self.view_name)
        if not selected:
            return HttpResponse("Vue inconnue")

        self.template_name = selected['template']
        self.bouton = selected['bouton']
        self.titre_page = selected['titre_page']
        self.page = selected['label']
        self.path = request.path

        # Breadcrumb dynamique
        parts = request.path.strip("/").split("/")
        url_stack = ""
        self.breadcrumb = []
        for index, part in enumerate(parts):
            url_stack += f"/{part}"
            self.breadcrumb.append({
                "name": part.capitalize(),
                "url": url_stack,
                "is_first": index == 0,
                "is_last": index == len(parts) - 1
            })

    def dispatch(self, request, *args, **kwargs):
        self.model_type = "evaluation"
        if self.model_type:
            self.model = Evaluation
            self.form_class = EvaluationForm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_name = self.get_type_name()
        context.update({
            'classe': "Evaluation",
            'bouton': self.bouton,
            'buttonName': self.bouton,
            'path': self.path,
            'titre_page': self.titre_page,
            'role_utilisateur': type_name,
            'model_type': self.model_type,
            'navbar': navbar,
            'page': self.page,
            'breadcrumb': self.breadcrumb,
        })
        return context

# ------------------------------------------------------
# Classes d’action pour Evaluation
# ------------------------------------------------------
class EvaluationListView(ListView, EvaluationBaseView):
    context_object_name = "evaluation"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.template_name = self.template_list
        return super().get(request, *args, **kwargs)


class EvaluationCreateView(EvaluationBaseView, CreateView):
    template_name = "cours/evaluation_form.html"

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.form_class = self.get_form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.form_class = self.get_form_class()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """
        On récupère classe + matière → on les transforme en matiereclasse
        avant d’enregistrer l’évaluation.
        """
        classe = form.cleaned_data["classe"]
        matiere = form.cleaned_data["matiere"]

        try:
            mc = MatiereClasse.objects.get(classe=classe, matiere=matiere)
        except MatiereClasse.DoesNotExist:
            form.add_error(None, "Cette matière n'est pas associée à la classe sélectionnée.")
            return self.form_invalid(form)

        form.instance.matiereclasse = mc

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('cours:evaluation_detail', kwargs={'pk': self.object.pk})

# Filtrer matières et enseignants selon la classe
def filter_by_classe(request, classe_id):
    matieres = Matiere.objects.filter(
        id__in=MatiereClasse.objects.filter(classe_id=classe_id).values_list('matiere', flat=True)
    ).values('id', 'nom')

    print("############@#@ Classes @#@############")               
    print("Matieres :",matieres)
    enseignants = Enseignant.objects.filter(
        utilisateur_id__in=Enseignement.objects.filter(
            matiere_classe__classe_id=classe_id
        ).values_list('enseignant__utilisateur_id', flat=True)
    ).values('utilisateur_id', 'utilisateur__last_name', 'utilisateur__first_name')
    print("Enseignants :",enseignants)
    return JsonResponse({
        'matieres': list(matieres),
        'enseignants': [
            {
                'id': str(e['utilisateur_id']),  # UUID en string
                'nom': f"{e['utilisateur__last_name']} {e['utilisateur__first_name']}"
            } for e in enseignants
        ],
    })


# Filtrer classes et enseignants selon la matière
def filter_by_matiere(request, matiere_id):
    classes = Classe.objects.filter(
        id__in=MatiereClasse.objects.filter(matiere_id=matiere_id).values_list('classe', flat=True)
    ).values('id', 'nom')
    print("############@#@ Matieres @#@############") 
    print("Classes :",classes)
    enseignants = Enseignant.objects.filter(
        utilisateur_id__in=Enseignement.objects.filter(
            matiere_classe__matiere_id=matiere_id
        ).values_list('enseignant__utilisateur_id', flat=True)
    ).values('utilisateur_id', 'utilisateur__last_name', 'utilisateur__first_name')
    print("Enseignants :",enseignants)
    return JsonResponse({
        'classes': list(classes),
        'enseignants': [
            {
                'id': str(e['utilisateur_id']),
                'nom': f"{e['utilisateur__last_name']} {e['utilisateur__first_name']}"
            } for e in enseignants
        ],
    })


# Filtrer classes et matières selon l’enseignant
def filter_by_enseignant(request, enseignant_id):
    enseignements = Enseignement.objects.filter(enseignant__utilisateur_id=enseignant_id)
    print("############@#@ Enseignant @#@############") 
    print("Enseignements :",enseignements)
    
    classes = Classe.objects.filter(
        id__in=enseignements.values_list('matiere_classe__classe', flat=True)
    ).values('id', 'nom')

    print("Classes :",classes)
    matieres = Matiere.objects.filter(
        id__in=enseignements.values_list('matiere_classe__matiere', flat=True)
    ).values('id', 'nom')
    
    print("Matieres :",matieres)
    
    return JsonResponse({
        'classes': list(classes),
        'matieres': list(matieres),
    })

def filter_by_classe_matiere(request, classe_id, matiere_id):
    # Vérifie qu'il existe bien le MatiereClasse
    try:
        mc = MatiereClasse.objects.get(classe_id=classe_id, matiere_id=matiere_id)
    except MatiereClasse.DoesNotExist:
        return JsonResponse({'enseignants': []})

    # Récupère les enseignements correspondant à cette matière-classe
    enseignements = Enseignement.objects.filter(matiere_classe=mc)

    # Récupère les enseignants liés (utilisateur_id = UUID)
    enseignants_qs = Enseignant.objects.filter(utilisateur_id__in=enseignements.values_list('enseignant__utilisateur_id', flat=True))

    # Format JSON
    enseignants = [
        {
            'id': str(e.utilisateur_id),
            'nom': f"{e.utilisateur.utilisateur.last_name if hasattr(e, 'utilisateur') else e.utilisateur.last_name} {e.utilisateur.first_name if hasattr(e, 'utilisateur') else e.utilisateur.first_name}"
        }
        for e in enseignants_qs
    ]

    return JsonResponse({'enseignants': enseignants})




class EvaluationDetailView(DetailView, EvaluationBaseView):
    context_object_name = "evaluation"
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        return super().get(request, *args, **kwargs)


class EvaluationUpdateView(UpdateView, EvaluationBaseView):
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.form_class = self.get_form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.form_class = self.get_form_class()
        return super().post(request, *args, **kwargs)

    success_url = reverse_lazy('cours:evaluation_list')


class EvaluationDeleteView(DeleteView, EvaluationBaseView):
    model = Evaluation
    pk_url_kwarg = "pk"
    context_object_name = "evaluation"
    template_name = 'Cours/supprimer/evaluation_confirm_delete.html'
    success_url = reverse_lazy('cours:evaluation_list')

