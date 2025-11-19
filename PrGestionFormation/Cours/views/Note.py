from .views import *
# ------------------------------------------------------
# Base view générique pour Matiere
# ------------------------------------------------------
class NoteBaseView(BaseContextView):
    model_type = None
    template_form = 'Cours/ajouter/note_form.html'
    template_list = 'Cours/liste/note_list.html'
    template_detail = 'Cours/detail/note_detail.html'
    template_delete = 'Cours/supprimer/note_confirm_delete.html'

    bouton = ""
    titre_page = "Note"
    page = ""
    path = ""
    view_name = ""
    breadcrumb = []

    model_mapping = {
        'note': (Note, NoteForm, "Note"),
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
        self.model_type = "note"
        type_name = self.get_type_name()
        suffix = "s"

        config = {
            'note_create': {
                'template': self.template_form,
                'bouton': 'Créer Note',
                'titre_page': f"Créer une {type_name}",
                'label': 'Création',
            },
            'note_list': {
                'template': self.template_list,
                'bouton': '',
                'titre_page': f"Liste des {type_name}{suffix}",
                'label': 'Liste',
            },
            'note_detail': {
                'template': self.template_detail,
                'bouton': '',
                'titre_page': f"Détails de la {type_name}",
                'label': 'Détails',
            },
            'note_update': {
                'template': self.template_form,
                'bouton': 'Modifier Note',
                'titre_page': f"Modifier une {type_name}",
                'label': 'Modification',
            },
            'note_delete': {
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
        self.model_type = "note"
        if self.model_type:
            self.model = Note
            self.form_class = NoteForm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_name = self.get_type_name()
        context.update({
            'classe': "Note",
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
# Classes d’action pour Matiere
# ------------------------------------------------------
class NoteListView(ListView, NoteBaseView):
    context_object_name = "note"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        self.template_name = self.template_list
        return super().get(request, *args, **kwargs)


class NoteCreateView(CreateView, NoteBaseView):
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

    success_url = reverse_lazy('cours:note_list')


class NoteDetailView(DetailView, NoteBaseView):
    context_object_name = "note"
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        return super().get(request, *args, **kwargs)


class NoteUpdateView(UpdateView, NoteBaseView):
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

    success_url = reverse_lazy('cours:note_list')


class NoteDeleteView(DeleteView, NoteBaseView):
    model = Note
    pk_url_kwarg = "pk"
    context_object_name = "note"
    template_name = 'Cours/supprimer/note_confirm_delete.html'
    success_url = reverse_lazy('cours:note_list')
