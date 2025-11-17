from .views import *
# ------------------------------------------------------
# Base view générique pour MatiereClasse
# ------------------------------------------------------
class MatiereClasseBaseView(BaseContextView):
    model_type = None
    template_form = 'Cours/ajouter/matiereclasse_form.html'
    template_list = 'Cours/liste/matiereclasse_list.html'
    template_detail = 'Cours/detail/matiereclasse_detail.html'
    template_delete = 'Cours/supprimer/matiereclasse_confirm_delete.html'

    bouton = ""
    titre_page = "Matière Classe"
    page = ""
    path = ""
    view_name = ""
    breadcrumb = []

    model_mapping = {
        'matiereclasse': (MatiereClasse, MatiereClasseForm, "Matière Classe"),
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
        self.model_type = "matiereclasse"
        type_name = self.get_type_name()
        suffix = "s"

        config = {
            'matiereclasse_create': {
                'template': self.template_form,
                'bouton': 'Créer',
                'titre_page': f"Créer une {type_name}",
                'label': 'Création',
            },
            'matiereclasse_list': {
                'template': self.template_list,
                'bouton': '',
                'titre_page': f"Liste des lien {type_name}{suffix}",
                'label': 'Liste',
            },
            'matiereclasse_detail': {
                'template': self.template_detail,
                'bouton': '',
                'titre_page': f"Détails du lien {type_name}",
                'label': 'Détails',
            },
            'matiere_update': {
                'template': self.template_form,
                'bouton': 'Modifier',
                'titre_page': f"Modifier le lien {type_name}",
                'label': 'Modification',
            },
            'matiere_delete': {
                'template': self.template_delete,
                'bouton': '',
                'titre_page': f"Supprimer le lien {type_name}",
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
        self.model_type = "matiere"
        if self.model_type:
            self.model = MatiereClasse
            self.form_class = MatiereClasseForm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_name = self.get_type_name()
        context.update({
            'classe': "Matière Classe",
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
# Classes d’action pour MatiereClasse
# ------------------------------------------------------
class MatiereClasseListView(ListView, MatiereClasseBaseView):
    context_object_name = "matieres"
    paginate_by = 20

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.template_name = self.template_list
        return super().get(request, *args, **kwargs)


class MatiereClasseCreateView(CreateView, MatiereClasseBaseView):
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

    success_url = reverse_lazy('cours:matiereclasse_list')


class MatiereClasseDetailView(DetailView, MatiereClasseBaseView):
    context_object_name = "matiereclasse"
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        return super().get(request, *args, **kwargs)


class MatiereClasseUpdateView(UpdateView, MatiereClasseBaseView):
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

    success_url = reverse_lazy('cours:matiereclasse_list')


class MatiereClasseDeleteView(DeleteView,MatiereClasseBaseView):
    model = MatiereClasse
    pk_url_kwarg = "pk"
    context_object_name = "matiereclasse"
    template_name = 'Cours/supprimer/matiereclasse_confirm_delete.html'
    success_url = reverse_lazy('cours:matiereclasse_list')
