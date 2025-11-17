from .views import *

# views.py




class SalleBaseView(BaseContextView):
    """
    Contrôleur générique complet (comme ScolariteBaseView)
    """
    model_type = "salle"
    template_form = 'Cours/ajouter/salle_form.html'
    template_list = 'Cours/liste/salle_list.html'
    template_detail = 'Cours/detail/salle_detail.html'
    template_delete = 'Cours/supprimer/salle_confirm_delete.html'

    bouton = ""
    titre_page = "Salle"
    page = ""
    path = ""
    view_name = ""
    breadcrumb = []

    model_mapping = {
        'salle': (Salle, SalleForm, "Salle"),
    }

    # 🔹 Retourne le model associé
    def get_model_class(self):
        return Salle

    # 🔹 Retourne le form associé
    def get_form_class(self):
        return SalleForm

    # 🔹 Retourne le nom du type
    def get_type_name(self):
        model_info = self.model_mapping.get(self.model_type)
        print(model_info)
        return model_info[-1] if model_info else "Type inconnu"

    # 🔹 Configure la vue selon l’action : list, create, detail, update, delete
    def setup_configuration(self, request):
        self.view_name = request.resolver_match.view_name.split(':')[-1]
        self.model_type = "salle"
        print(self.model_type)
        type_name = self.get_type_name()
        suffix = "s"

        config = {
            'salle': {
                'template': self.template_form,
                'bouton': 'Créer Salle',
                'titre_page': f"Créer une {type_name}",
                'label': 'Création',
            },
            'salle_create': {
                'template': self.template_form,
                'bouton': 'Créer Salle',
                'titre_page': f"Créer une {type_name}",
                'label': 'Création',
            },
            'salle_list': {
                'template': self.template_list,
                'bouton': '',
                'titre_page': f"Liste des {type_name}{suffix}",
                'label': 'Liste',
            },
            'salle_detail': {
                'template': self.template_detail,
                'bouton': '',
                'titre_page': f"Détails de la {type_name}",
                'label': 'Détails',
            },
            'salle_update': {
                'template': self.template_form,
                'bouton': 'Modifier Salle',
                'titre_page': f"Modifier une {type_name}",
                'label': 'Modification',
            },
            'salle_delete': {
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
        self.model_type = "salle"
        if self.model_type:
            self.model = Salle
            self.form_class = SalleForm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        type_name = self.get_type_name()

        context.update({
            'classe' : "Salle",
            'bouton' : self.bouton,
            'buttonName': self.bouton,
            'path' : self.path,
            'titre_page' : self.titre_page,
            'role_utilisateur': type_name,
            'model_type': self.model_type,
            'navbar': navbar,  # Assure-toi que 'navbar' est bien défini globalement
            'page': self.page,
            'breadcrumb': self.breadcrumb,
        })
        return context


# ------------------------------------------------------
# 2️⃣ Classes d’actions basées sur SalleBaseView
# ------------------------------------------------------


class SalleListView(ListView,SalleBaseView):
    context_object_name = "salles"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = Salle
        self.template_name = self.template_list
        return super().get(request, *args, **kwargs)


class SalleCreateView(CreateView,SalleBaseView):
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

    success_url = reverse_lazy('cours:salle_list')


class SalleDetailView(DetailView,SalleBaseView):
    context_object_name = "salle"
    pk_url_kwarg = "pk"

    def get(self, request, *args, **kwargs):
        self.setup_configuration(request)
        self.model = self.get_model_class()
        return super().get(request, *args, **kwargs)


class SalleUpdateView(UpdateView,SalleBaseView):
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

    success_url = reverse_lazy('cours:salle_list')


class SalleDeleteView(DeleteView):
    model = Salle
    pk_url_kwarg = "pk"
    context_object_name = "salle"
    template_name = 'Cours/supprimer/salle_confirm_delete.html'
    success_url = reverse_lazy('cours:salle_list')