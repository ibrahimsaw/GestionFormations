from django.urls import path

from .views.parent import *
from .views.views import *
from .views.etudiant import *

app_name = 'utilisateur'

urlpatterns = [
    # Vos URLs ici
    path('', CustomLoginView.as_view(), name='login'),
    path('parent/', ParentextView.as_view(), name='parent'),
    path('etudiant/', EtudiantextView.as_view(), name='etudiant'),
    path('etudiantS/', EtudiantextViewS.as_view(), name='etudiantS'),
    path('changer-mot-de-passe/', ChangerMotDePasseView.as_view(), name='changer-mot-de-passe'),
    path('utilisateur/<uuid:utilisateur_id>/changer-mot-de-passe/', ModifierMotDePasseUtilisateurView.as_view(), name='modifier_mot_de_passe_utilisateur'),

    path('bienvenu', Bienvenu.as_view(), name='bienvenu'),
    path('cv', Cv.as_view(), name='cv'),
    path('cvv', Cvv.as_view(), name='cvv'),

    # -----------------Creation-------------------
    path('ajouter/', UtilisateurCreateView.as_view(), name='utilisateur_create'),
    path('ajouter/<str:role>/', UtilisateurCreateView.as_view(), name='utilisateur_create'),
    path('ajouter-specialite/', ajouter_specialite, name='ajouter_specialite'),

    # -----------------Liste-------------------
    # path('utilisateur/', views.ChoixListes_des_Utilisateurs.as_view(), name='liste_utilisateurs'),
    path('liste/', UtilisateurListView.as_view(), name='utilisateur_list'),
    path('liste/<str:role>/', UtilisateurListView.as_view(), name='utilisateur_list'),
    # -----------------Detail-------------------
    path('detail/<str:role>/<uuid:pk>/', UtilisateurDetailView.as_view(), name='utilisateur_detail'),
    # -----------------Modifier-------------------
    # path('<str:role>/<int:pk>/modifier/', UtilisateurUpdateView.as_view(), name='utilisateur_update'),
    path('modifier/<str:role>/<uuid:pk>/modifier/', UtilisateurUpdateView.as_view(), name='utilisateur_modifier'),
    # -----------------Supprimer-------------------
    path('supprimer/<str:role>/<uuid:pk>/supprimer/', UtilisateurDeleteView.as_view(), name='utilisateur_supprimer'),

    path('get_parcours_options/', get_parcours_options, name='get_parcours_options'),
    path('get_classes_options/', get_classes_options, name='get_classes_options'),
    path('ajax/get-infos-etudiant/', get_infos_etudiant, name='get_student_info'),
    path('search_students/',search_students, name='search_students'),


    # # Administrateur
    path('tableau_de_bord_admin/', Bienvenu.as_view(), name='tableau_de_bord_admin'),
    # # path('creation_de_comptes/', views. Creation_de_comptes, name='creation_de_comptes'),
    # # path('liste_utilisateurs/', views. Listes_des_Utilisateurs, name='liste_utilisateurs'),
    path('droits_acces/', Bienvenu.as_view(), name='droits_acces'),
    
    ## Etudiant
    path('tableau_de_bord_etudiant/', TableauBordEtudiantView.as_view(), name='tableau_de_bord_etudiant'),
    path('profil_etudiant/', ProfilEtudiantView.as_view(), name='profil_etudiant'),
    path('calendrier_etudiant/', CalendrierEtudiantView.as_view(), name='calendrier_etudiant'),
    path('notes_etudiant/', NotesEtudiantView.as_view(), name='notes_etudiant'),
    path('cours_etudiant/', CoursEtudiantView.as_view(), name='cours_etudiant'),
    path('documents_etudiant/', DocumentsEtudiantView.as_view(), name='documents_etudiant'),
    path('assiduite_etudiant/', AssiduiteEtudiantView.as_view(), name='assiduite_etudiant'),
    
## Parent
    path('tableau_de_bord_parent/', TableauBordParentView.as_view(), name='tableau_de_bord_parent'),
    path('profil_parent/', ProfilParentView.as_view(), name='profil_parent'),
    
    # path('configuration_generale/', Bienvenu.as_view(), name='configuration_generale'),
    # path('gestion_roles/', Bienvenu.as_view(), name='gestion_roles'),
    # path('activite_systeme/', Bienvenu.as_view(), name='activite_systeme'),
    # path('connexions_utilisateurs/', Bienvenu.as_view(), name='connexions_utilisateurs'),
    # path('sauvegardes/', Bienvenu.as_view(), name='sauvegardes'),
    # path('audit_securite/', Bienvenu.as_view(), name='audit_securite'),
    # path('support_technique/', Bienvenu.as_view(), name='support_technique'),
    #
    # # Agent Administratif
    # path('accueil_agent/', Bienvenu.as_view(), name='accueil_agent'),
    # path('gestion_inscriptions/', Bienvenu.as_view(), name='gestion_inscriptions'),
    # path('emplois_du_temps/', Bienvenu.as_view(), name='emplois_du_temps'),
    # path('ressources_pedagogiques/', Bienvenu.as_view(), name='ressources_pedagogiques'),
    # path('envoi_annonces/', Bienvenu.as_view(), name='envoi_annonces'),
    # path('messagerie_interne/', Bienvenu.as_view(), name='messagerie_interne'),
    # path('documents_administratifs/', Bienvenu.as_view(), name='documents_administratifs'),
    # path('archivage/', Bienvenu.as_view(), name='archivage'),
    # path('statistiques/', Bienvenu.as_view(), name='statistiques'),
    #
    # # Enseignant
    # path('planning_enseignant/', Bienvenu.as_view(), name='planning_enseignant'),
    # path('matieres_enseignees/', Bienvenu.as_view(), name='matieres_enseignees'),
    # path('documents_pedagogiques/', Bienvenu.as_view(), name='documents_pedagogiques'),
    # path('saisie_notes/', Bienvenu.as_view(), name='saisie_notes'),
    # path('bulletins_enseignant/', Bienvenu.as_view(), name='bulletins_enseignant'),
    # path('liste_classes/', Bienvenu.as_view(), name='liste_classes'),
    # path('suivi_individuel/', Bienvenu.as_view(), name='suivi_individuel'),
    # path('ressources_partagees/', Bienvenu.as_view(), name='ressources_partagees'),
    # path('forum_pedagogique/', Bienvenu.as_view(), name='forum_pedagogique'),
    # path('parametres_notification/', Bienvenu.as_view(), name='parametres_notification'),
    #
    # # Étudiant
    # path('emploi_du_temps_etudiant/', Bienvenu.as_view(), name='emploi_du_temps_etudiant'),
    # path('documents_cours/', Bienvenu.as_view(), name='documents_cours'),
    # path('resultats_matiere/', Bienvenu.as_view(), name='resultats_matiere'),
    # path('historique_notes/', Bienvenu.as_view(), name='historique_notes'),
    # path('bibliotheque_numerique/', Bienvenu.as_view(), name='bibliotheque_numerique'),
    # path('travaux_a_rendre/', Bienvenu.as_view(), name='travaux_a_rendre'),
    # path('messagerie_etudiant/', Bienvenu.as_view(), name='messagerie_etudiant'),
    # path('evenements_etudiant/', Bienvenu.as_view(), name='evenements_etudiant'),
    # path('parametres_compte_etudiant/', Bienvenu.as_view(), name='parametres_compte_etudiant'),
    #
    # # Parent
    # path('resultats_enfant/', Bienvenu.as_view(), name='resultats_enfant'),
    # path('absences_retards/', Bienvenu.as_view(), name='absences_retards'),
    # path('communication_enseignants/', Bienvenu.as_view(), name='communication_enseignants'),
    # path('annonces_etablissement/', Bienvenu.as_view(), name='annonces_etablissement'),
    # path('certificats_scolaires/', Bienvenu.as_view(), name='certificats_scolaires'),
    # path('factures_parent/', Bienvenu.as_view(), name='factures_parent'),
    # path('calendrier_scolaire/', Bienvenu.as_view(), name='calendrier_scolaire'),
    # path('alertes_parent/', Bienvenu.as_view(), name='alertes_parent'),
    # path('parametres_parent/', Bienvenu.as_view(), name='parametres_parent'),
    #
    # # Commun
    # path('profil_utilisateur/', Bienvenu.as_view(), name='profil_utilisateur'),
    # path('aide/', Bienvenu.as_view(), name='aide'),
    # path('deconnexion/', Bienvenu.as_view(), name='deconnexion'),
]