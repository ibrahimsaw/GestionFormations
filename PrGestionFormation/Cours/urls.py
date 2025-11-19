# This code snippet is defining URL patterns for a Django web application. Here's a breakdown of what
# it does:
from django.urls import path
from .views.Salle import *
from .views.Matiere import *
from .views.MatiereClasse import *
from .views.Evaluation import * 
from .views.Note import * 
from .views.Enseignement import *

app_name = 'cours'

# urls.py

urlpatterns = [
    ################### Salle ###################
    path('salle/', SalleListView.as_view(), name="salle"),
    path('salle/liste/', SalleListView.as_view(), name="salle_list"),
    path('salle/ajout/', SalleCreateView.as_view(), name="salle_create"),
    path('salle/<int:pk>/detail', SalleDetailView.as_view(), name="salle_detail"),
    path('salle/<int:pk>/modifier/', SalleUpdateView.as_view(), name="salle_update"),
    path('salle/<int:pk>/supprimer/', SalleDeleteView.as_view(), name="salle_delete"),
    
    ################### Matiere ###################
    path('matiere/', MatiereListView.as_view(), name='matiere'),
    path('matiere/liste/', MatiereListView.as_view(), name='matiere_list'),
    path('matiere/ajout/', MatiereCreateView.as_view(), name='matiere_create'),
    path('matiere/<int:pk>/detail', MatiereDetailView.as_view(), name='matiere_detail'),
    path('matiere/<int:pk>/modifier/', MatiereUpdateView.as_view(), name='matiere_update'),
    path('matiere/<int:pk>/supprimer/', MatiereDeleteView.as_view(), name='matiere_delete'),

    ################### MatiereClasse ###################
    path('matiereclasse/', MatiereClasseListView.as_view(), name='matiereclasse'),
    path('matiereclasse/liste/', MatiereClasseListView.as_view(), name='matiereclasse_list'),
    path('matiereclasse/ajout/', MatiereClasseCreateView.as_view(), name='matiereclasse_create'),
    path('matiereclasse/<int:pk>/detail', MatiereClasseDetailView.as_view(), name='matiereclasse_detail'),
    path('matiereclasse/<int:pk>/modifier/', MatiereClasseUpdateView.as_view(), name='matiereclasse_update'),
    path('matiereclasse/<int:pk>/supprimer/', MatiereClasseDeleteView.as_view(), name='matiereclasse_delete'),
    
    ################### Evaluation ###################
    path('evaluation/', EvaluationListView.as_view(), name='evaluation'),
    path('evaluation/liste/', EvaluationListView.as_view(), name='evaluation_list'),
    path('evaluation/ajout/',EvaluationCreateView.as_view(), name='evaluation_create'),
    path('evaluation/<int:pk>/detail', EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('evaluation/<int:pk>/modifier/', EvaluationUpdateView.as_view(), name='evaluation_update'),
    path('evaluation/<int:pk>/supprimer/', EvaluationDeleteView.as_view(), name='evaluation_delete'),
    path('filter_by_classe/<int:classe_id>/', filter_by_classe, name='filter_by_classe'),
    path('filter_by_matiere/<int:matiere_id>/', filter_by_matiere, name='filter_by_matiere'),
    path('filter_by_enseignant/<uuid:enseignant_id>/', filter_by_enseignant, name='filter_by_enseignant'),

    
    ################### Note ###################
    path('note/', NoteListView.as_view(), name='note'),
    path('note/liste/', NoteListView.as_view(), name='note_list'),
    path('note/ajout/', NoteCreateView.as_view(), name='note_create'),
    path('note/<int:pk>/detail', NoteDetailView.as_view(), name='note_detail'),
    path('note/<int:pk>/modifier/', NoteUpdateView.as_view(), name='note_update'),
    path('note/<int:pk>/supprimer/', NoteDeleteView.as_view(), name='note_delete'),
    
    ################### Enseignement ###################
    path('enseignement/', EnseignementListView.as_view(), name='enseignement'),
    path('enseignement/liste/', EnseignementListView.as_view(), name='enseignement_list'),
    path('enseignement/ajout/', EnseignementCreateView.as_view(), name='enseignement_create'),
    path('enseignement/<int:pk>/detail', EnseignementDetailView.as_view(), name='enseignement_detail'),
    path('enseignement/<int:pk>/modifier/', EnseignementUpdateView.as_view(), name='enseignement_update'),
    path('enseignement/<int:pk>/supprimer/', EnseignementDeleteView.as_view(), name='enseignement_delete'),
    path("enseignement_by_classe/<int:classe_id>/", Enseignement_by_classe, name="enseignement_by_classe"),
    path("enseignement_by_classe_matiere/<int:classe_id>/<int:matiereclasse_id>/", Enseignement_by_classe_matiere, name="enseignement_by_classe_matiere"),
    
]
