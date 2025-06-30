from django.urls import path
from .views import *

app_name = 'formation'

urlpatterns = [
    # Vos URLs ici
    path('maintenance/', Bienvenu.as_view(), name='maintenance'),
    path('ajouter/', UniversalCreateView.as_view(), name='universal-create'),
    path('ajouter/<str:type>/', UniversalCreateView.as_view(), name='universal-create'),
    path('liste/', UniversalListView.as_view(), name='universal-list'),
    path('liste/<str:type>/', UniversalListView.as_view(), name='universal-list'),
    path('detail/<str:type>/<int:pk>/', UniversalDetailView.as_view(), name='universal-detail'),

]