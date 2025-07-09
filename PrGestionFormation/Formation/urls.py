from django.urls import path
from .views import *

app_name = 'formation'

urlpatterns = [
    # Vos URLs ici
    path('maintenance/', Bienvenu.as_view(), name='maintenance'),
    path('ajouter/', FormationCreateView.as_view(), name='universal-create'),
    path('ajouter/<str:type>/', FormationCreateView.as_view(), name='universal-create'),
    path('liste/', FormationListView.as_view(), name='universal-list'),
    path('liste/<str:type>/', FormationListView.as_view(), name='universal-list'),
    path('detail/<str:type>/<int:pk>/', FormationDetailView.as_view(), name='universal-detail'),
]