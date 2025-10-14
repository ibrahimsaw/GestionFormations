from django.urls import path
from Permissions_Manager.views import *

app_name = 'Permissions_Manager'

urlpatterns = [
    path('', GestionPermissionsView.as_view(), name='permission'),
    path('<str:type>/', GestionPermissionsView.as_view(), name='permission'),
    path('users/<uuid:user_id>/', GererPermissionsUtilisateurView.as_view(), name='gerer_permissions_utilisateur'),
    path('fonction/creer/', GererFonctionView.as_view(), name='creer_fonction'),
    path('fonction/<int:fonction_id>/', GererFonctionView.as_view(), name='modifier_fonction'),
    path('fonction/supprimer/<int:fonction_id>/', SupprimerFonctionView.as_view(), name='supprimer_fonction'),
    # path('permission/creer/', CreerPermissionView.as_view(), name='creer_permission'),
    # path('permission/modifier/<int:permission_id>/', ModifierPermissionView.as_view(), name='modifier_permission'),
    path('permissions/<int:permission_id>/detail/',DetailPermissionView.as_view(),name='permission_detail'),
    path('utilisateur/<int:pk>/', historique_utilisateur, name='historique_utilisateur'),
    path('utilisateur/<uuid:utilisateur_pk>/historique-actions/', historique_actions_par_utilisateur, name='historique_actions_utilisateur'),
    path('utilisateur/<str:type>/<uuid:pk>/historique/', HistoriqueUtilisateurView.as_view(), name='historique_utilisateur'),
]