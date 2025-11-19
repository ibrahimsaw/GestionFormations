from .views import *
# ------------------------------------------------------
# Base view générique pour Enseignement
# ------------------------------------------------------
class EnseignementBaseView(BaseContextView):
    model_type = None
    template_form = 'Cours/ajouter/enseignement_form.html'
    template_list = 'Cours/liste/enseignement_list.html'
    template_detail = 'Cours/detail/enseignement_detail.html'
    template_delete = 'Cours/supprimer/enseignement_confirm_delete.html'

    bouton = ""
    titre_page = "Enseignement"
    page = ""
    path = ""
    view_name = ""
    breadcrumb = []

    model_mapping = {
        'enseignement': (Enseignement, EnseignementForm, "Enseignement"),
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
        self.model_type = "enseignement"
        type_name = self.get_type_name()
        suffix = "s"

        config = {
            'enseignement_create': {
                'template': self.template_form,
                'bouton': 'Créer Enseignement',
                'titre_page': f"Créer une {type_name}",
                'label': 'Création',
            },
            'enseignement_list': {
                'template': self.template_list,
                'bouton': '',
                'titre_page': f"Liste des {type_name}{suffix}",
                'label': 'Liste',
            },
            'enseignement_detail': {
                'template': self.template_detail,
                'bouton': '',
                'titre_page': f"Détails de la {type_name}",
                'label': 'Détails',
            },
            'enseignement_update': {
                'template': self.template_form,
                'bouton': 'Modifier Enseignement',
                'titre_page': f"Modifier une {type_name}",
                'label': 'Modification',
            },
            'enseignement_delete': {
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
        self.model_type = "enseignement"
        if self.model_type:
            self.model = Enseignement
            self.form_class = EnseignementForm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_name = self.get_type_name()
        context.update({
            'classe': "Enseignement",
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
# Classes d’action pour Enseignement
# ------------------------------------------------------
class EnseignementListView(ListView, EnseignementBaseView):
    context_object_name = "enseignements"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.template_name = self.template_list
        return super().get(request, *args, **kwargs)


class EnseignementCreateView(CreateView, EnseignementBaseView):
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ajouter toutes les classes pour le dropdown
        context['classes'] = Classe.objects.all()
        return context
    
    def get_success_url(self):
        return reverse('cours:enseignement_detail', kwargs={'pk': self.object.pk})




# =========================
# AJAX pour charger matières
# =========================
def Enseignement_by_classe(request, classe_id):
    matieres = MatiereClasse.objects.filter(classe_id=classe_id).values("id", "matiere__nom")
    data = {
        "matieres": [{"id": m["id"], "nom": m["matiere__nom"]} for m in matieres]
    }
    return JsonResponse(data)

# =========================
# AJAX pour charger enseignants
# =========================
def Enseignement_by_classe_matiere(request, classe_id, matiereclasse_id):
    matiere_classe = get_object_or_404(MatiereClasse, pk=matiereclasse_id)
    matiere_nom = matiere_classe.matiere.nom

    enseignants = Enseignant.objects.filter(
        matieres__nom=matiere_nom
    ).values(
        "utilisateur_id",
        "utilisateur__first_name",
        "utilisateur__last_name"
    ).distinct()

    data = {
        "enseignants": [
            {
                "utilisateur_id": e["utilisateur_id"],
                "utilisateur__first_name": e["utilisateur__first_name"],
                "utilisateur__last_name": e["utilisateur__last_name"]
            }
            for e in enseignants
        ]
    }
    return JsonResponse(data)


class EnseignementDetailView(DetailView, EnseignementBaseView):
    context_object_name = "Enseignement"
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        return super().get(request, *args, **kwargs)


class EnseignementUpdateView(UpdateView, EnseignementBaseView):
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

    def get_success_url(self):
        return reverse('cours:enseignement_detail', kwargs={'pk': self.object.pk})


class EnseignementDeleteView(DeleteView, EnseignementBaseView):
    model = Enseignement
    pk_url_kwarg = "pk"
    context_object_name = "Enseignement"
    template_name = 'Cours/supprimer/enseignement_confirm_delete.html'
    success_url = reverse_lazy('cours:enseignement_list')
