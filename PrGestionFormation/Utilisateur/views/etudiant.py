from .views import *

class EtudiantextViewTableauBord(BaseContextView, TemplateView):
    template_name ='Utilisateur/Etudiant/tableau_de_bord_etudiant.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donne'] = 'Tableau de Bord Etudiant'
        context['model_type'] = 'tableau_bord_etudiant'
        return context

class EtudiantextViewProfil(BaseContextView, TemplateView):
    template_name = 'Utilisateur/Etudiant/profil_etudiant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donne'] = 'Profil Etudiant'
        context['model_type'] = 'profil_etudiant'
        return context
    
class EtudiantextViewCalendrier(BaseContextView, TemplateView):
    template_name = 'Utilisateur/Etudiant/calendrier_etudiant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donne'] = 'Calendrier Etudiant'
        context['model_type'] = 'calendrier_etudiant'
        return context

class EtudiantextViewNotes(BaseContextView, TemplateView):
    template_name = 'Utilisateur/Etudiant/notes_etudiant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donne'] = 'Notes Etudiant'
        context['model_type'] = 'notes_etudiant'
        return context
    
class EtudiantextViewCours(BaseContextView, TemplateView):
    template_name = 'Utilisateur/Etudiant/cours_etudiant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['donne'] = 'Cours Etudiant'
        context['model_type'] = 'cours_etudiant'    
        return context
    
class EtudiantextViewDocuments(BaseContextView, TemplateView):
    template_name = 'Utilisateur/Etudiant/documents_etudiant.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)# The
        context['donne'] = 'Documents Etudiant'
        context['model_type'] = 'documents_etudiant'
        return context