# This code snippet is defining URL patterns for a Django web application. Here's a breakdown of what
# it does:
from django.urls import path
from .views.Salle import *
from .views.Matiere import *
from .views.MatiereClasse import *
from .views.Evaluation import *


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
    path('matiere/', MatiereListView.as_view(), name='matiere_list'),
    path('matiere/liste/', MatiereListView.as_view(), name='matiere_list'),
    path('matiere/ajout/', MatiereCreateView.as_view(), name='matiere_create'),
    path('matiere/<int:pk>/detail', MatiereDetailView.as_view(), name='matiere_detail'),
    path('matiere/<int:pk>/modifier/', MatiereUpdateView.as_view(), name='matiere_update'),
    path('matiere/<int:pk>/supprimer/', MatiereDeleteView.as_view(), name='matiere_delete'),

    ################### MatiereClasse ###################
    path('matiereclasse/', MatiereClasseListView.as_view(), name='matiereclasse_list'),
    path('matiereclasse/liste/', MatiereClasseListView.as_view(), name='matiereclasse_list'),
    path('matiereclasse/ajout/', MatiereClasseCreateView.as_view(), name='matiereclasse_create'),
    path('matiereclasse/<int:pk>/detail', MatiereClasseDetailView.as_view(), name='matiereclasse_detail'),
    path('matiereclasse/<int:pk>/modifier/', MatiereClasseUpdateView.as_view(), name='matiereclasse_update'),
    path('matiereclasse/<int:pk>/supprimer/', MatiereClasseDeleteView.as_view(), name='matiereclasse_delete'),
    
    ################### Evaluation ###################
    path('evaluation/', EvaluationListView.as_view(), name='evaluation_list'),
    path('evaluation/liste/', EvaluationListView.as_view(), name='evaluation_list'),
    path('evaluation/ajout/',EvaluationCreateView.as_view(), name='evaluation_create'),
    path('evaluation/<int:pk>/detail', EvaluationDetailView.as_view(), name='evaluation_detail'),
    path('evaluation/<int:pk>/modifier/', EvaluationUpdateView.as_view(), name='evaluation_update'),
    path('evaluation/<int:pk>/supprimer/', EvaluationDeleteView.as_view(), name='evaluation_delete'),
]
