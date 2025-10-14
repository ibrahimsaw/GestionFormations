from django.urls import path
from .views import *

app_name = 'finance'

urlpatterns = [
    # Vos URLs ici
    path('ajouter/', ScolariteCreateView.as_view(), name='scolarite-create'),
    path('ajax/frais_par_etudiant/', frais_par_etudiant, name='frais_par_etudiant'),
    path("ajax/montant_restant/", montant_restant_pour_frais, name="montant_restant"),
    path("etudiants/search/", search_etudiant_by_matricule, name="etudiant-search-matricule"),

    path('ajouter/<str:type>', ScolariteCreateView.as_view(), name='scolarite-create'),
    path('liste/', ScolariteListView.as_view(), name='scolarite-list'),
    path('liste/<str:type>/', ScolariteListView.as_view(), name='scolarite-list'),
    path('liste/<str:type>/<int:pk>/', ScolariteDetailView.as_view(), name='scolarite-detail'),
    path('scolarite/<str:type>/<int:pk>/modifier/', ScolariteUpdateView.as_view(), name='scolarite-update'),
    path('scolarite/<str:type>/<int:pk>/supprimer/', ScolariteDeleteView.as_view(), name='scolarite-delete'),
]