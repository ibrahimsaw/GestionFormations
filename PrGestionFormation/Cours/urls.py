# This code snippet is defining URL patterns for a Django web application. Here's a breakdown of what
# it does:
from django.urls import path
from .views.Salle import *
from .views.Matiere import *

app_name = 'cours'

# urls.py

urlpatterns = [
    ################### Salle ###################
    path('salle/', SalleListView.as_view(), name="salle"),
    path('salle/liste/', SalleListView.as_view(), name="salle_list"),
    path('salle/ajout/', SalleCreateView.as_view(), name="salle_create"),
    path('salle/<int:pk>/', SalleDetailView.as_view(), name="salle_detail"),
    path('salle/<int:pk>/modifier/', SalleUpdateView.as_view(), name="salle_update"),
    path('salle/<int:pk>/supprimer/', SalleDeleteView.as_view(), name="salle_delete"),
    
    ################### Matiere ###################
    path('matiere/', MatiereListView.as_view(), name='matiere_list'),
    path('matiere/liste/', MatiereListView.as_view(), name='matiere_list'),
    path('matiere/ajout/', MatiereCreateView.as_view(), name='matiere_create'),
    path('matiere/<int:pk>/', MatiereDetailView.as_view(), name='matiere_detail'),
    path('matiere/<int:pk>/modifier/', MatiereUpdateView.as_view(), name='matiere_update'),
    path('matiere/<int:pk>/supprimer/', MatiereDeleteView.as_view(), name='matiere_delete'),

]
