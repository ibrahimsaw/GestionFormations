from django.urls import path
from Permissions_Manager.views import (
    GestionPermissionsView,
    GererPermissionsUtilisateurView,
    GererFonctionView,
    # CreerPermissionView,
    DetailPermissionView,
    SupprimerFonctionView,
    # ModifierPermissionView
)

app_name = 'Permissions_Manager'

urlpatterns = [
    path('', GestionPermissionsView.as_view(), name='permission'),
    path('utilisateur/<int:user_id>/', GererPermissionsUtilisateurView.as_view(), name='gerer_permissions_utilisateur'),
    path('fonction/', GererFonctionView.as_view(), name='creer_fonction'),
    path('fonction/<int:fonction_id>/', GererFonctionView.as_view(), name='modifier_fonction'),
    path('fonction/supprimer/<int:fonction_id>/', SupprimerFonctionView.as_view(), name='supprimer_fonction'),
    # path('permission/creer/', CreerPermissionView.as_view(), name='creer_permission'),
    # path('permission/modifier/<int:permission_id>/', ModifierPermissionView.as_view(), name='modifier_permission'),
    path('permissions/<int:permission_id>/detail/',DetailPermissionView.as_view(),name='permission_detail'
    ),
]