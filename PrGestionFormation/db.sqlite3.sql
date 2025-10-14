BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "Finance_devoir" ("document_ptr_id" bigint NOT NULL PRIMARY KEY REFERENCES "Finance_document" ("id") DEFERRABLE INITIALLY DEFERRED, "date_rendu" datetime NOT NULL, "est_rendu" bool NOT NULL);
CREATE TABLE IF NOT EXISTS "Finance_document" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "titre" varchar(200) NOT NULL, "fichier" varchar(100) NOT NULL, "type" varchar(2) NOT NULL, "date_upload" datetime NOT NULL, "auteur_id" bigint NOT NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Finance_documentinscription" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "type_document" varchar(50) NOT NULL, "fichier" varchar(100) NOT NULL, "date_depot" datetime NOT NULL, "inscription_id" bigint NOT NULL REFERENCES "Finance_inscription" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Finance_frais" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "libelle" varchar(20) NOT NULL, "montant" decimal NOT NULL, "description" text NULL, "recurrent" bool NOT NULL, "classe_id" bigint NOT NULL REFERENCES "Formation_classe" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Finance_historicalfrais" ("id" bigint NOT NULL, "libelle" varchar(20) NOT NULL, "montant" decimal NOT NULL, "description" text NULL, "recurrent" bool NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "classe_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Finance_historicalinscription" ("id" bigint NOT NULL, "motif" text NULL, "Etablissement_accuiel" varchar(100) NULL, "date_inscription" date NOT NULL, "date_evenement" datetime NULL, "duree" integer unsigned NULL CHECK ("duree" >= 0), "statut" varchar(20) NOT NULL, "resultat_annee_precedente" varchar(100) NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "annee_academique_id" bigint NULL, "classe_id" bigint NULL, "etudiant_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "parcours_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Finance_historicalpaiement" ("id" bigint NOT NULL, "montant" decimal NOT NULL, "methode" varchar(2) NOT NULL, "reference" varchar(50) NOT NULL, "date_paiement" datetime NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "etudiant_id" bigint NULL, "frais_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Finance_inscription" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "date_inscription" date NOT NULL, "statut" varchar(20) NOT NULL, "annee_academique_id" bigint NULL REFERENCES "Formation_anneeacademique" ("id") DEFERRABLE INITIALLY DEFERRED, "classe_id" bigint NULL REFERENCES "Formation_classe" ("id") DEFERRABLE INITIALLY DEFERRED, "parcours_id" bigint NULL REFERENCES "Formation_parcours" ("id") DEFERRABLE INITIALLY DEFERRED, "date_evenement" datetime NULL, "duree" integer unsigned NULL CHECK ("duree" >= 0), "motif" text NULL, "resultat_annee_precedente" varchar(100) NULL, "Etablissement_accuiel" varchar(100) NULL, "etudiant_id" bigint NULL REFERENCES "Utilisateur_etudiant" ("utilisateur_id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Finance_notification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "contenu" text NOT NULL, "type" varchar(2) NOT NULL, "date_envoi" datetime NOT NULL, "est_lu" bool NOT NULL, "utilisateur_id" bigint NOT NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Finance_paiement" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "montant" decimal NOT NULL, "methode" varchar(2) NOT NULL, "reference" varchar(50) NOT NULL UNIQUE, "date_paiement" datetime NOT NULL, "etudiant_id" bigint NOT NULL REFERENCES "Utilisateur_etudiant" ("utilisateur_id") DEFERRABLE INITIALLY DEFERRED, "frais_id" bigint NOT NULL REFERENCES "Finance_frais" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Formation_anneeacademique" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(20) NOT NULL UNIQUE, "date_debut" date NOT NULL, "date_fin" date NOT NULL, "classes_standards_creees" bool NOT NULL);
CREATE TABLE IF NOT EXISTS "Formation_classe" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "ordre" integer NOT NULL, "annee_academique_id" bigint NOT NULL REFERENCES "Formation_anneeacademique" ("id") DEFERRABLE INITIALLY DEFERRED, "formation_id" bigint NOT NULL REFERENCES "Formation_formation" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Formation_formation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "est_professionnelle" bool NOT NULL, "avec_classes" bool NOT NULL, "parcours_id" bigint NOT NULL REFERENCES "Formation_parcours" ("id") DEFERRABLE INITIALLY DEFERRED, "duree" integer NULL);
CREATE TABLE IF NOT EXISTS "Formation_historicalanneeacademique" ("id" bigint NOT NULL, "nom" varchar(20) NOT NULL, "date_debut" date NOT NULL, "date_fin" date NOT NULL, "classes_standards_creees" bool NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Formation_historicalclasse" ("id" bigint NOT NULL, "nom" varchar(100) NOT NULL, "ordre" integer NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "annee_academique_id" bigint NULL, "formation_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Formation_historicalformation" ("id" bigint NOT NULL, "nom" varchar(100) NOT NULL, "duree" integer NULL, "est_professionnelle" bool NOT NULL, "avec_classes" bool NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "parcours_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Formation_historicalparcours" ("id" bigint NOT NULL, "nom" varchar(100) NOT NULL, "code_serie" varchar(3) NULL, "structure_classes" text NOT NULL CHECK ((JSON_VALID("structure_classes") OR "structure_classes" IS NULL)), "diplome_final" varchar(100) NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "specification_id" bigint NULL, "type_formation_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Formation_parcours" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL, "code_serie" varchar(3) NULL, "structure_classes" text NOT NULL CHECK ((JSON_VALID("structure_classes") OR "structure_classes" IS NULL)), "diplome_final" varchar(100) NULL, "specification_id" bigint NULL REFERENCES "Formation_specification" ("id") DEFERRABLE INITIALLY DEFERRED, "type_formation_id" bigint NOT NULL REFERENCES "Formation_typeformation" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Formation_specification" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "code" varchar(10) NOT NULL UNIQUE, "nom" varchar(50) NOT NULL);
CREATE TABLE IF NOT EXISTS "Formation_typeformation" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "code" varchar(10) NOT NULL UNIQUE, "nom" varchar(100) NOT NULL, "liste_classe" text NOT NULL CHECK ((JSON_VALID("liste_classe") OR "liste_classe" IS NULL)));
CREATE TABLE IF NOT EXISTS "Permissions_Manager_metapermission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "description" text NOT NULL, "roles_autorises" varchar(200) NOT NULL, "est_active" bool NOT NULL, "date_creation" datetime NOT NULL, "date_modification" datetime NOT NULL, "permission_id" integer NOT NULL UNIQUE REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_adminsysteme" ("utilisateur_id" bigint NOT NULL PRIMARY KEY REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_agentadministration" ("utilisateur_id" bigint NOT NULL PRIMARY KEY REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_agentadministration_fonctions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "agentadministration_id" bigint NOT NULL REFERENCES "Utilisateur_agentadministration" ("utilisateur_id") DEFERRABLE INITIALLY DEFERRED, "fonctionagent_id" bigint NOT NULL REFERENCES "Utilisateur_fonctionagent" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_enseignant" ("utilisateur_id" bigint NOT NULL PRIMARY KEY REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "autres_specialites" varchar(255) NOT NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_enseignant_specialites" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "enseignant_id" bigint NOT NULL REFERENCES "Utilisateur_enseignant" ("utilisateur_id") DEFERRABLE INITIALLY DEFERRED, "specialite_id" bigint NOT NULL REFERENCES "Utilisateur_specialite" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_etudiant" ("utilisateur_id" bigint NOT NULL PRIMARY KEY REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_fonctionagent" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "code" varchar(50) NOT NULL UNIQUE, "nom" varchar(100) NOT NULL, "description" text NOT NULL, "responsabilites" text NOT NULL CHECK ((JSON_VALID("responsabilites") OR "responsabilites" IS NULL)), "controles" text NOT NULL CHECK ((JSON_VALID("controles") OR "controles" IS NULL)), "protocoles" text NOT NULL CHECK ((JSON_VALID("protocoles") OR "protocoles" IS NULL)), "role" varchar(20) NOT NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_fonctionagent_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fonctionagent_id" bigint NOT NULL REFERENCES "Utilisateur_fonctionagent" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_genre" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "code" varchar(10) NOT NULL UNIQUE, "libelle" varchar(50) NOT NULL, "description" text NULL, "est_par_defaut" bool NOT NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_historicaladminsysteme" ("history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "utilisateur_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_historicalagentadministration" ("history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "utilisateur_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_historicalenseignant" ("autres_specialites" varchar(255) NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "utilisateur_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_historicaletudiant" ("history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "utilisateur_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_historicalparent" ("history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "utilisateur_id" bigint NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_historicalutilisateur" ("id" bigint NOT NULL, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "matricule" varchar(20) NOT NULL, "email" varchar(254) NULL, "telephone" varchar(20) NULL, "first_name" varchar(30) NOT NULL, "last_name" varchar(150) NOT NULL, "role" varchar(20) NOT NULL, "date_inscription" datetime NOT NULL, "date_nais" date NOT NULL, "doit_changer_mot_de_passe" bool NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "history_id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "history_date" datetime NOT NULL, "history_change_reason" varchar(100) NULL, "history_type" varchar(1) NOT NULL, "genre_id" bigint NULL, "history_user_id" bigint NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_parent" ("utilisateur_id" bigint NOT NULL PRIMARY KEY REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_parent_enfants" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "parent_id" bigint NOT NULL REFERENCES "Utilisateur_parent" ("utilisateur_id") DEFERRABLE INITIALLY DEFERRED, "etudiant_id" bigint NOT NULL REFERENCES "Utilisateur_etudiant" ("utilisateur_id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_rolepermission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "role" varchar(20) NOT NULL UNIQUE, "date_creation" datetime NOT NULL, "date_maj" datetime NOT NULL, "groupe_id" integer NULL UNIQUE REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_rolepermission_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "rolepermission_id" bigint NOT NULL REFERENCES "Utilisateur_rolepermission" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_specialite" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "nom" varchar(100) NOT NULL UNIQUE, "description" text NOT NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_utilisateur" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "password" varchar(128) NOT NULL, "last_login" datetime NULL, "is_superuser" bool NOT NULL, "matricule" varchar(20) NOT NULL UNIQUE, "email" varchar(254) NULL, "telephone" varchar(20) NULL, "first_name" varchar(30) NOT NULL, "last_name" varchar(150) NOT NULL, "role" varchar(20) NOT NULL, "date_inscription" datetime NOT NULL, "date_nais" date NOT NULL, "is_staff" bool NOT NULL, "is_active" bool NOT NULL, "genre_id" bigint NULL REFERENCES "Utilisateur_genre" ("id") DEFERRABLE INITIALLY DEFERRED, "doit_changer_mot_de_passe" bool NOT NULL);
CREATE TABLE IF NOT EXISTS "Utilisateur_utilisateur_groups" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "utilisateur_id" bigint NOT NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "Utilisateur_utilisateur_user_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "utilisateur_id" bigint NOT NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_group" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(150) NOT NULL UNIQUE);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "group_id" integer NOT NULL REFERENCES "auth_group" ("id") DEFERRABLE INITIALLY DEFERRED, "permission_id" integer NOT NULL REFERENCES "auth_permission" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE TABLE IF NOT EXISTS "auth_permission" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content_type_id" integer NOT NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "codename" varchar(100) NOT NULL, "name" varchar(255) NOT NULL);
CREATE TABLE IF NOT EXISTS "django_admin_log" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "object_id" text NULL, "object_repr" varchar(200) NOT NULL, "action_flag" smallint unsigned NOT NULL CHECK ("action_flag" >= 0), "change_message" text NOT NULL, "content_type_id" integer NULL REFERENCES "django_content_type" ("id") DEFERRABLE INITIALLY DEFERRED, "user_id" bigint NOT NULL REFERENCES "Utilisateur_utilisateur" ("id") DEFERRABLE INITIALLY DEFERRED, "action_time" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "django_content_type" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app_label" varchar(100) NOT NULL, "model" varchar(100) NOT NULL);
CREATE TABLE IF NOT EXISTS "django_migrations" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "app" varchar(255) NOT NULL, "name" varchar(255) NOT NULL, "applied" datetime NOT NULL);
CREATE TABLE IF NOT EXISTS "django_session" ("session_key" varchar(40) NOT NULL PRIMARY KEY, "session_data" text NOT NULL, "expire_date" datetime NOT NULL);
INSERT INTO "Finance_historicalinscription" ("id","motif","Etablissement_accuiel","date_inscription","date_evenement","duree","statut","resultat_annee_precedente","history_id","history_date","history_change_reason","history_type","annee_academique_id","classe_id","etudiant_id","history_user_id","parcours_id") VALUES (1,NULL,NULL,'2025-10-06',NULL,NULL,'inscrit',NULL,1,'2025-10-06 21:13:14.102444',NULL,'+',1,1,6,5,1),
 (2,NULL,NULL,'2025-10-06',NULL,NULL,'inscrit',NULL,2,'2025-10-06 21:14:30.251399',NULL,'+',1,1,7,5,1),
 (3,NULL,NULL,'2025-10-06',NULL,NULL,'inscrit',NULL,3,'2025-10-06 21:14:56.464782',NULL,'+',1,1,8,5,1),
 (1,NULL,NULL,'2025-10-06',NULL,NULL,'inscrit',NULL,4,'2025-10-07 09:52:17.674766',NULL,'~',1,1,6,7,1);
INSERT INTO "Finance_inscription" ("id","date_inscription","statut","annee_academique_id","classe_id","parcours_id","date_evenement","duree","motif","resultat_annee_precedente","Etablissement_accuiel","etudiant_id") VALUES (1,'2025-10-06','inscrit',1,1,1,NULL,NULL,NULL,NULL,NULL,6),
 (2,'2025-10-06','inscrit',1,1,1,NULL,NULL,NULL,NULL,NULL,7),
 (3,'2025-10-06','inscrit',1,1,1,NULL,NULL,NULL,NULL,NULL,8);
INSERT INTO "Formation_anneeacademique" ("id","nom","date_debut","date_fin","classes_standards_creees") VALUES (1,'2025-2026','2025-10-01','2026-10-01',1),
 (2,'2025-2027','2025-10-01','2027-10-01',1);
INSERT INTO "Formation_classe" ("id","nom","ordre","annee_academique_id","formation_id") VALUES (1,'Infographie',1,1,1);
INSERT INTO "Formation_formation" ("id","nom","est_professionnelle","avec_classes","parcours_id","duree") VALUES (1,'Infographie',1,1,1,3);
INSERT INTO "Formation_historicalanneeacademique" ("id","nom","date_debut","date_fin","classes_standards_creees","history_id","history_date","history_change_reason","history_type","history_user_id") VALUES (1,'2025-2026','2025-10-01','2026-10-01',0,1,'2025-10-06 19:50:13.949008',NULL,'+',5),
 (1,'2025-2026','2025-10-01','2026-10-01',1,2,'2025-10-06 19:50:13.994521',NULL,'~',5),
 (2,'2025-2027','2025-10-01','2027-10-01',1,3,'2025-10-06 19:51:39.280309',NULL,'+',5);
INSERT INTO "Formation_historicalclasse" ("id","nom","ordre","history_id","history_date","history_change_reason","history_type","annee_academique_id","formation_id","history_user_id") VALUES (1,'Infographie',1,1,'2025-10-06 19:52:28.633568',NULL,'+',1,1,5);
INSERT INTO "Formation_historicalformation" ("id","nom","duree","est_professionnelle","avec_classes","history_id","history_date","history_change_reason","history_type","history_user_id","parcours_id") VALUES (1,'Infographie',3,1,1,1,'2025-10-06 19:49:20.181208',NULL,'+',5,1);
INSERT INTO "Formation_historicalparcours" ("id","nom","code_serie","structure_classes","diplome_final","history_id","history_date","history_change_reason","history_type","history_user_id","specification_id","type_formation_id") VALUES (1,'Infographie',NULL,'["Infographie 1, Infographie 2"]','Attestation de Infographie',1,'2025-10-02 20:49:09.432077',NULL,'+',5,3,5);
INSERT INTO "Formation_parcours" ("id","nom","code_serie","structure_classes","diplome_final","specification_id","type_formation_id") VALUES (1,'Infographie',NULL,'["Infographie 1, Infographie 2"]','Attestation de Infographie',3,5);
INSERT INTO "Formation_specification" ("id","code","nom") VALUES (1,'GN','Générale'),
 (2,'TH','Technique'),
 (3,'FO','Formation'),
 (4,'UN','Université');
INSERT INTO "Formation_typeformation" ("id","code","nom","liste_classe") VALUES (1,'PR','Préscolaire','["PS", "MS", "GS"]'),
 (2,'PRIM','Primaire','["CP1", "CP2", "CE1", "CE2", "CM1", "CM2"]'),
 (3,'SEC1','Secondaire 1er cycle','["6e", "5e", "4e", "3e"]'),
 (4,'SEC2','Secondaire 2nd cycle','["2nde", "1\u00e8re", "Tle"]'),
 (5,'PRO','Professionnel','[]'),
 (6,'LIC','Licence','["L1", "L2", "L3"]'),
 (7,'MAS','Master','["M1", "M2"]');
INSERT INTO "Utilisateur_etudiant" ("utilisateur_id") VALUES (6),
 (7),
 (8);
INSERT INTO "Utilisateur_fonctionagent" ("id","code","nom","description","responsabilites","controles","protocoles","role") VALUES (1,'SECRETAIRE_ADMINISTRATIF','Secrétaire administratif','Gestion centralisée du courrier et documents administratifs','["Gestion du courrier entrant/sortant", "Classement et archivage des documents", "Accueil physique et t\u00e9l\u00e9phonique", "Pr\u00e9paration des dossiers pour r\u00e9unions", "Saisie des donn\u00e9es administratives"]','["V\u00e9rification quotidienne du bon acheminement du courrier", "Audit mensuel des dossiers archiv\u00e9s"]','["Proc\u00e9dure de traitement du courrier confidentiel", "Protocole de destruction des documents obsol\u00e8tes"]','AGENT'),
 (2,'CHARGE_INSCRIPTIONS','Chargé des inscriptions','Gestion du processus complet d''inscription des étudiants','["V\u00e9rification des dossiers d''inscription", "Enregistrement des nouveaux \u00e9tudiants", "Gestion des d\u00e9rogations", "Coordination avec le service financier", "Mise \u00e0 jour des fichiers \u00e9tudiants"]','["Contr\u00f4le al\u00e9atoire de 10% des dossiers", "V\u00e9rification des pi\u00e8ces justificatives"]','["Proc\u00e9dure de validation des d\u00e9rogations", "Protocole RGPD pour les donn\u00e9es personnelles"]','AGENT'),
 (3,'GESTIONNAIRE_DOSSIERS','Gestionnaire des dossiers étudiants','Maintenance et mise à jour des dossiers étudiants','["Maintenance des dossiers \u00e9tudiants", "V\u00e9rification des pi\u00e8ces manquantes", "Archivage num\u00e9rique et physique", "R\u00e9ponse aux demandes d''acc\u00e8s", "Application des r\u00e8gles RGPD"]','["V\u00e9rification trimestrielle de l''exhaustivit\u00e9 des dossiers", "Contr\u00f4le d''acc\u00e8s aux documents sensibles"]','["Protocole de mise \u00e0 jour des dossiers", "Proc\u00e9dure de r\u00e9ponse aux demandes l\u00e9gales"]','AGENT'),
 (4,'AGENT_SCOLARITE','Agent de scolarité','Gestion administrative des parcours étudiants','["Suivi des inscriptions p\u00e9dagogiques", "Gestion des changements de fili\u00e8re", "\u00c9dition des attestations", "Coordination avec les d\u00e9partements", "Traitement des demandes sp\u00e9ciales"]','["V\u00e9rification des pr\u00e9requis acad\u00e9miques", "Contr\u00f4le des droits d''inscription"]','["Proc\u00e9dure de changement de parcours", "Protocole d''\u00e9dition des documents officiels"]','AGENT'),
 (5,'RESPONSABLE_EMPLOI_TEMPS','Responsable des emplois du temps','Création et gestion des plannings académiques','["\u00c9laboration des plannings", "Gestion des salles et ressources", "R\u00e9solution des conflits d''horaire", "Publication des calendriers", "Coordination avec les enseignants"]','["V\u00e9rification de l''ad\u00e9quation salles/effectifs", "Contr\u00f4le du respect des volumes horaires"]','["Protocole de modification des plannings", "Proc\u00e9dure d''urgence pour salles indisponibles"]','AGENT'),
 (6,'AGENT_DISCIPLINE','Agent chargé de la discipline','Application du règlement intérieur et suivi disciplinaire','["Enregistrement des incidents", "Application du r\u00e8glement int\u00e9rieur", "Suivi des mesures disciplinaires", "Communication avec les familles", "Rapports mensuels"]','["V\u00e9rification de la proportionnalit\u00e9 des sanctions", "Contr\u00f4le du suivi des mesures"]','["Proc\u00e9dure de traitement des incidents graves", "Protocole de signalement aux autorit\u00e9s comp\u00e9tentes"]','AGENT'),
 (7,'CHARGE_EXAMENS','Chargé des examens et concours','Organisation logistique des évaluations académiques','["Organisation des sessions d''examen", "Gestion des sujets et copies", "Coordination des surveillances", "S\u00e9curisation des \u00e9preuves", "Traitement des fraudes"]','["Double v\u00e9rification des sujets", "Contr\u00f4le d''identit\u00e9 strict en salle"]','["Protocole de s\u00e9curisation des sujets", "Proc\u00e9dure de traitement des fraudes"]','AGENT'),
 (8,'RESPONSABLE_BULLETINS','Responsable des bulletins et relevés de notes','Gestion et diffusion des résultats académiques','["Saisie et v\u00e9rification des notes", "\u00c9dition des relev\u00e9s de notes", "Gestion des r\u00e9clamations", "Archivage des r\u00e9sultats", "Calcul des moyennes"]','["Double contr\u00f4le des calculs de moyennes", "V\u00e9rification des validations p\u00e9dagogiques"]','["Protocole de correction des erreurs", "Proc\u00e9dure de traitement des r\u00e9clamations"]','AGENT'),
 (9,'AGENT_ATTESTATIONS','Agent chargé des attestations et diplômes','Émission et gestion des documents officiels','["\u00c9mission des documents officiels", "Gestion des demandes de duplicata", "V\u00e9rification des droits", "Archivage s\u00e9curis\u00e9", "Lutte contre la fraude"]','["V\u00e9rification syst\u00e9matique des droits", "Contr\u00f4le qualit\u00e9 avant \u00e9mission"]','["Proc\u00e9dure d''\u00e9mission des duplicata", "Protocole anti-fraude des documents"]','AGENT'),
 (10,'GESTIONNAIRE_COURRIER','Gestionnaire du courrier administratif','Gestion du flux de courrier institutionnel','["Tri et distribution du courrier", "Gestion des envois institutionnels", "Tra\u00e7abilit\u00e9 des exp\u00e9ditions", "Num\u00e9risation des documents", "Classement chronologique"]','["Tra\u00e7abilit\u00e9 compl\u00e8te des envois", "V\u00e9rification des accus\u00e9s de r\u00e9ception"]','["Protocole pour courrier confidentiel", "Proc\u00e9dure d''urgence pour courrier recommand\u00e9"]','AGENT'),
 (11,'SUIVI_ENSEIGNANTS','Responsable du suivi des enseignants','Gestion administrative des intervenants pédagogiques','["Suivi des contrats enseignants", "Gestion des services horaires", "Interface avec les services RH"]','["V\u00e9rification des qualifications", "Contr\u00f4le du respect des volumes horaires"]','["Protocole de recrutement des vacataires", "Proc\u00e9dure de signalement des absences"]','AGENT'),
 (12,'LIAISON_PEDAGOGIQUE','Agent de liaison pédagogique','Interface entre administration et corps enseignant','["Transmission des informations p\u00e9dagogiques", "Remont\u00e9e des besoins mat\u00e9riels", "Organisation des r\u00e9unions p\u00e9dagogiques"]','["Suivi des comptes-rendus de r\u00e9union", "V\u00e9rification de la diffusion des informations"]','["Protocole de circulation de l''information", "Proc\u00e9dure d''urgence pour probl\u00e8mes p\u00e9dagogiques"]','AGENT'),
 (13,'RESSOURCES_MATERIELLES','Agent de gestion des ressources matérielles','Gestion du patrimoine matériel pédagogique','["Inventaire du mat\u00e9riel", "Gestion des pr\u00eats", "Organisation de la maintenance"]','["V\u00e9rification trimestrielle des stocks", "Contr\u00f4le des conditions de s\u00e9curit\u00e9"]','["Protocole de pr\u00eat de mat\u00e9riel", "Proc\u00e9dure de signalement des dysfonctionnements"]','AGENT'),
 (14,'CHARGE_CONVOCATIONS','Chargé des convocations','Gestion des convocations officielles','["\u00c9dition des convocations", "Gestion des envois", "Suivi des confirmations"]','["V\u00e9rification des listes de destinataires", "Contr\u00f4le des accus\u00e9s de r\u00e9ception"]','["Protocole pour convocations urgentes", "Proc\u00e9dure de relance des absents"]','AGENT'),
 (15,'BASE_DONNEES_ETUDIANTS','Responsable de la base de données étudiants','Gestion et sécurisation des données étudiantes','["Mise \u00e0 jour des donn\u00e9es", "Sauvegarde des informations", "Gestion des acc\u00e8s"]','["V\u00e9rification quotidienne des sauvegardes", "Audit semestriel des acc\u00e8s"]','["Protocole RGPD pour donn\u00e9es sensibles", "Proc\u00e9dure de r\u00e9cup\u00e9ration apr\u00e8s incident"]','AGENT'),
 (16,'AGENT_ACCUEIL','Agent d''accueil et d''information','Premier contact avec l''institution','["Accueil physique et t\u00e9l\u00e9phonique", "Orientation des visiteurs", "Gestion des demandes courantes"]','["Mesure de la satisfaction usagers", "Suivi du temps d''attente"]','["Protocole d''accueil des personnes \u00e0 mobilit\u00e9 r\u00e9duite", "Proc\u00e9dure pour situations d''urgence"]','AGENT'),
 (17,'AGENT_COMPTABLE','Agent comptable','Gestion des aspects financiers étudiants','["Encaissement des frais de scolarit\u00e9", "Gestion des \u00e9ch\u00e9anciers", "Rapprochement bancaire"]','["V\u00e9rification quotidienne des encaissements", "Contr\u00f4le mensuel des impay\u00e9s"]','["Protocole de traitement des paiements en retard", "Proc\u00e9dure de remboursement"]','AGENT');
INSERT INTO "Utilisateur_fonctionagent_permissions" ("id","fonctionagent_id","permission_id") VALUES (1,6,24);
INSERT INTO "Utilisateur_genre" ("id","code","libelle","description","est_par_defaut") VALUES (1,'F','Femme','Genre féminin',0),
 (2,'H','Homme','Genre masculin',0),
 (3,'ND','Non précisé','Genre non déclaré',1);
INSERT INTO "Utilisateur_historicaletudiant" ("history_id","history_date","history_change_reason","history_type","history_user_id","utilisateur_id") VALUES (1,'2025-10-06 21:13:14.082724',NULL,'+',5,6),
 (2,'2025-10-06 21:13:14.114330',NULL,'~',5,6),
 (3,'2025-10-06 21:14:30.233490',NULL,'+',5,7),
 (4,'2025-10-06 21:14:30.258782',NULL,'~',5,7),
 (5,'2025-10-06 21:14:56.448277',NULL,'+',5,8),
 (6,'2025-10-06 21:14:56.480685',NULL,'~',5,8),
 (7,'2025-10-07 09:52:17.381504',NULL,'~',7,6);
INSERT INTO "Utilisateur_historicalutilisateur" ("id","password","last_login","is_superuser","matricule","email","telephone","first_name","last_name","role","date_inscription","date_nais","doit_changer_mot_de_passe","is_staff","is_active","history_id","history_date","history_change_reason","history_type","genre_id","history_user_id") VALUES (3,'pbkdf2_sha256$1000000$B3WjUnOGyAOA9bBL4yZhlb$VssJYgwmvgpinuD5uxXQsVSYbuNbk5CLXuQXSL4wo9M=',NULL,1,'ADM003',NULL,NULL,'','','ADMIN','2025-10-02 17:56:28.892362','1990-01-01',1,1,1,1,'2025-10-02 17:56:28.931309',NULL,'+',NULL,NULL),
 (1,'pbkdf2_sha256$1000000$F8VLAZbMjNHyENNtBmKJQ3$7qm14ZK2Q1+/9PFZWHJCR0eas9TKPH0OK6LI3nUpcOU=','2025-10-02 17:57:15.897966',1,'ADM002',NULL,NULL,'','','ADMIN','2025-10-02 17:50:45.683212','1990-01-01',1,1,1,2,'2025-10-02 17:57:15.927665',NULL,'~',NULL,1),
 (1,'pbkdf2_sha256$1000000$F8VLAZbMjNHyENNtBmKJQ3$7qm14ZK2Q1+/9PFZWHJCR0eas9TKPH0OK6LI3nUpcOU=','2025-10-02 17:57:54.273105',1,'ADM002',NULL,NULL,'','','ADMIN','2025-10-02 17:50:45.683212','1990-01-01',1,1,1,3,'2025-10-02 17:57:54.284590',NULL,'~',NULL,1),
 (4,'pbkdf2_sha256$1000000$FquO7UhJUEAGeyRC6K1X2o$eBksBn5Tdg4n2pxqvxiC5g4/hSS7I76wyQGYDjVfG9E=',NULL,1,'ADM004',NULL,NULL,'','','ADMIN','2025-10-02 18:13:08.322601','1990-01-01',1,1,1,4,'2025-10-02 18:13:08.338202',NULL,'+',NULL,NULL),
 (5,'pbkdf2_sha256$1000000$AFvWFSEntaXFxNPlqhnWye$Zewc/GZRUCQ0LPJwGc9Q9jZ+V1TNBDroMBSpElSk0y4=',NULL,1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',1,1,1,5,'2025-10-02 18:21:33.243447',NULL,'+',NULL,NULL),
 (5,'pbkdf2_sha256$1000000$AFvWFSEntaXFxNPlqhnWye$Zewc/GZRUCQ0LPJwGc9Q9jZ+V1TNBDroMBSpElSk0y4=','2025-10-02 18:22:37.286797',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',1,1,1,6,'2025-10-02 18:22:37.292697',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$AFvWFSEntaXFxNPlqhnWye$Zewc/GZRUCQ0LPJwGc9Q9jZ+V1TNBDroMBSpElSk0y4=','2025-10-02 18:22:37.286797',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,7,'2025-10-02 18:23:02.398013',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-02 18:22:37.286797',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,8,'2025-10-02 18:23:08.574765',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-02 18:24:15.578705',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,9,'2025-10-02 18:24:15.587779',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-03 16:47:13.894773',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,10,'2025-10-03 16:47:13.921139',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-03 21:53:57.102980',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,11,'2025-10-03 21:53:57.110589',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-06 09:44:05.994823',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,12,'2025-10-06 09:44:06.191335',NULL,'~',NULL,5),
 (2,'pbkdf2_sha256$1000000$Kads0MyKStSGdvvNePKG7m$H3CSKXcjKfI4yy6bBCHMdmUoJgi3jt8Ymgz5e02ODiQ=','2025-10-06 16:18:16.933385',1,'ADM001',NULL,NULL,'','','ADMIN','2025-10-02 17:55:26.551181','1990-01-01',1,1,1,13,'2025-10-06 16:18:16.939250',NULL,'~',NULL,2),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-06 16:18:40.609495',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,14,'2025-10-06 16:18:40.614680',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-06 16:51:38.903767',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,15,'2025-10-06 16:51:38.914618',NULL,'~',NULL,5),
 (6,'pbkdf2_sha256$1000000$I6PVrq3bDZ4Eb7ZYWb2w5X$PC+d3aDVrcar7W88yKY52/KTmuBeub9NOuSQesudaSc=',NULL,0,'ETU-846983','ibrahimsaw@gmail.com','+22678687673','Ibra','Saw','ETUDIANT','2025-10-06 21:13:02.669332','1990-01-01',1,0,1,16,'2025-10-06 21:13:02.692406',NULL,'+',2,5),
 (6,'pbkdf2_sha256$1000000$SOdmj38oHk4iDqSwQzKJAV$gd9mTJEb3fAf9MN5C+zqvjkLooPLxXPCgh4aLRZ04R0=',NULL,0,'ETU-846983','ibrahimsaw@gmail.com','+22678687673','Ibra','Saw','ETUDIANT','2025-10-06 21:13:02.669332','1990-01-01',1,0,1,17,'2025-10-06 21:13:14.052305',NULL,'~',2,5),
 (7,'pbkdf2_sha256$1000000$NMNgjsCe9lxukpiBzrsHhJ$N2TQwyIU0O/f1vEMYKAq3XG4YdMZPraHc09PSEBvFr4=',NULL,0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',1,0,1,18,'2025-10-06 21:14:27.293069',NULL,'+',2,5),
 (7,'pbkdf2_sha256$1000000$B0Mxd3c5ZTef1k1tLwBRxX$UsasH/59M+jkAs0X0+MnmPuspxespu9uv1YOaAJpJag=',NULL,0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',1,0,1,19,'2025-10-06 21:14:30.206274',NULL,'~',2,5),
 (8,'pbkdf2_sha256$1000000$tg4XkzxMjJz43UbViJZNyw$oxTWWZ7NhhkfexBGjumA62j1+BSR/Xe9RoHvzlGl7F4=',NULL,0,'ETU-27C402','ibrahimsaw@gmail.com','+226687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:51.311986','1990-01-01',1,0,1,20,'2025-10-06 21:14:51.330623',NULL,'+',2,5),
 (8,'pbkdf2_sha256$1000000$zWApWmMWrSkUzCjwbWVrec$GnNu9CRpAfOJjzXzruc1Wmcw1FYjtLZ8Eeq/fePkHl0=',NULL,0,'ETU-27C402','ibrahimsaw@gmail.com','+226687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:51.311986','1990-01-01',1,0,1,21,'2025-10-06 21:14:56.412301',NULL,'~',2,5),
 (7,'pbkdf2_sha256$1000000$ooiEu23Rmr6rCbL34H5MnV$199F2fMiIwzo+gXtyY+Sq4IdVcQTgAd6ozvrgyLNwKg=',NULL,0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',1,0,1,22,'2025-10-07 09:25:50.314301',NULL,'~',2,5),
 (7,'pbkdf2_sha256$1000000$ooiEu23Rmr6rCbL34H5MnV$199F2fMiIwzo+gXtyY+Sq4IdVcQTgAd6ozvrgyLNwKg=','2025-10-07 09:26:14.511454',0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',1,0,1,23,'2025-10-07 09:26:14.520356',NULL,'~',2,7),
 (7,'pbkdf2_sha256$1000000$ooiEu23Rmr6rCbL34H5MnV$199F2fMiIwzo+gXtyY+Sq4IdVcQTgAd6ozvrgyLNwKg=','2025-10-07 09:26:14.511454',0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',0,0,1,24,'2025-10-07 09:27:22.978580',NULL,'~',2,7),
 (7,'pbkdf2_sha256$1000000$v35x8CyMcIXrBztQ3aAanY$iwvRntx4V6XbY+VhSfbD8SHrZA4Gt00nsVVXBYauj0s=','2025-10-07 09:26:14.511454',0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',0,0,1,25,'2025-10-07 09:27:24.557459',NULL,'~',2,7),
 (7,'pbkdf2_sha256$1000000$v35x8CyMcIXrBztQ3aAanY$iwvRntx4V6XbY+VhSfbD8SHrZA4Gt00nsVVXBYauj0s=','2025-10-07 09:49:49.119108',0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',0,0,1,26,'2025-10-07 09:49:49.132328',NULL,'~',2,7),
 (6,'pbkdf2_sha256$1000000$SOdmj38oHk4iDqSwQzKJAV$gd9mTJEb3fAf9MN5C+zqvjkLooPLxXPCgh4aLRZ04R0=',NULL,0,'ETU-846983','ibrahimsaw@gmail.com','+2268687673','Ibra','Saw','ETUDIANT','2025-10-06 21:13:02.669332','1990-01-02',1,0,1,27,'2025-10-07 09:52:17.115617',NULL,'~',2,7),
 (6,'pbkdf2_sha256$1000000$SOdmj38oHk4iDqSwQzKJAV$gd9mTJEb3fAf9MN5C+zqvjkLooPLxXPCgh4aLRZ04R0=',NULL,0,'ETU-846983','ibrahimsaw@gmail.com','+2268687673','Ibra','Saw','ETUDIANT','2025-10-06 21:13:02.669332','1990-01-02',1,0,1,28,'2025-10-07 09:52:17.158459',NULL,'~',2,7),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-08 09:15:29.820107',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,29,'2025-10-08 09:15:29.955498',NULL,'~',NULL,5),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-08 09:15:43.289306',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',0,1,1,30,'2025-10-08 09:15:43.324507',NULL,'~',NULL,5);
INSERT INTO "Utilisateur_rolepermission" ("id","role","date_creation","date_maj","groupe_id") VALUES (1,'ADMIN','2025-10-02 18:20:49.192250','2025-10-02 18:20:49.192303',1),
 (2,'AGENT','2025-10-02 18:20:50.142092','2025-10-02 18:20:50.142139',2),
 (3,'ENSEIGNANT','2025-10-02 18:20:50.547850','2025-10-02 18:20:50.547895',3),
 (4,'ETUDIANT','2025-10-02 18:20:50.575124','2025-10-02 18:20:50.575163',4),
 (5,'PARENT','2025-10-02 18:20:50.603676','2025-10-02 18:20:50.603716',5);
INSERT INTO "Utilisateur_rolepermission_permissions" ("id","rolepermission_id","permission_id") VALUES (1,1,1),
 (2,1,2),
 (3,1,3),
 (4,1,4),
 (5,1,5),
 (6,1,6),
 (7,1,7),
 (8,1,8),
 (9,1,9),
 (10,1,10),
 (11,1,11),
 (12,1,12),
 (13,1,13),
 (14,1,14),
 (15,1,15),
 (16,1,16),
 (17,1,17),
 (18,1,18),
 (19,1,19),
 (20,1,20),
 (21,1,21),
 (22,1,22),
 (23,1,23),
 (24,1,24),
 (25,1,25),
 (26,1,26),
 (27,1,27),
 (28,1,28),
 (29,1,29),
 (30,1,30),
 (31,1,31),
 (32,1,32),
 (33,1,33),
 (34,1,34),
 (35,1,35),
 (36,1,36),
 (37,1,37),
 (38,1,38),
 (39,1,39),
 (40,1,40),
 (41,1,41),
 (42,1,42),
 (43,1,43),
 (44,1,44),
 (45,1,45),
 (46,1,46),
 (47,1,47),
 (48,1,48),
 (49,1,49),
 (50,1,50),
 (51,1,51),
 (52,1,52),
 (53,1,53),
 (54,1,54),
 (55,1,55),
 (56,1,56),
 (57,1,57),
 (58,1,58),
 (59,1,59),
 (60,1,60),
 (61,1,61),
 (62,1,62),
 (63,1,63),
 (64,1,64),
 (65,1,65),
 (66,1,66),
 (67,1,67),
 (68,1,68),
 (69,1,69),
 (70,1,70),
 (71,1,71),
 (72,1,72),
 (73,1,73),
 (74,1,74),
 (75,1,75),
 (76,1,76),
 (77,1,77),
 (78,1,78),
 (79,1,79),
 (80,1,80),
 (81,1,81),
 (82,1,82),
 (83,1,83),
 (84,1,84),
 (85,1,85),
 (86,1,86),
 (87,1,87),
 (88,1,88),
 (89,1,89),
 (90,1,90),
 (91,1,91),
 (92,1,92),
 (93,1,93),
 (94,1,94),
 (95,1,95),
 (96,1,96),
 (97,1,97),
 (98,1,98),
 (99,1,99),
 (100,1,100),
 (101,1,101),
 (102,1,102),
 (103,1,103),
 (104,1,104),
 (105,1,105),
 (106,1,106),
 (107,1,107),
 (108,1,108),
 (109,1,109),
 (110,1,110),
 (111,1,111),
 (112,1,112),
 (113,1,113),
 (114,1,114),
 (115,1,115),
 (116,1,116),
 (117,1,117),
 (118,1,118),
 (119,1,119),
 (120,1,120),
 (121,1,121),
 (122,1,122),
 (123,1,123),
 (124,1,124),
 (125,1,125),
 (126,1,126),
 (127,1,127),
 (128,1,128),
 (129,1,129),
 (130,1,130),
 (131,1,131),
 (132,1,132),
 (133,1,133),
 (134,1,134),
 (135,1,135),
 (136,1,136),
 (137,1,137),
 (138,1,138),
 (139,1,139),
 (140,1,140),
 (141,1,141),
 (142,1,142),
 (143,1,143),
 (144,1,144),
 (145,1,145),
 (146,1,146),
 (147,1,147),
 (148,1,148),
 (149,1,149),
 (150,1,150),
 (151,1,151),
 (152,1,152),
 (153,1,153),
 (154,1,154),
 (155,1,155),
 (156,1,156),
 (157,1,157),
 (158,1,158),
 (159,1,159),
 (160,1,160),
 (161,1,161),
 (162,1,162),
 (163,1,163),
 (164,1,164),
 (165,1,165),
 (166,1,166),
 (167,1,167),
 (168,1,168),
 (169,2,96),
 (170,2,109),
 (171,2,110),
 (172,2,112),
 (173,2,24),
 (174,2,93),
 (175,2,94);
INSERT INTO "Utilisateur_utilisateur" ("id","password","last_login","is_superuser","matricule","email","telephone","first_name","last_name","role","date_inscription","date_nais","is_staff","is_active","genre_id","doit_changer_mot_de_passe") VALUES (1,'pbkdf2_sha256$1000000$F8VLAZbMjNHyENNtBmKJQ3$7qm14ZK2Q1+/9PFZWHJCR0eas9TKPH0OK6LI3nUpcOU=','2025-10-02 17:57:54.273105',1,'ADM002',NULL,NULL,'','','ADMIN','2025-10-02 17:50:45.683212','1990-01-01',1,1,NULL,1),
 (2,'pbkdf2_sha256$1000000$Kads0MyKStSGdvvNePKG7m$H3CSKXcjKfI4yy6bBCHMdmUoJgi3jt8Ymgz5e02ODiQ=','2025-10-06 16:18:16.933385',1,'ADM001',NULL,NULL,'','','ADMIN','2025-10-02 17:55:26.551181','1990-01-01',1,1,NULL,1),
 (3,'pbkdf2_sha256$1000000$B3WjUnOGyAOA9bBL4yZhlb$VssJYgwmvgpinuD5uxXQsVSYbuNbk5CLXuQXSL4wo9M=',NULL,1,'ADM003',NULL,NULL,'','','ADMIN','2025-10-02 17:56:28.892362','1990-01-01',1,1,NULL,1),
 (4,'pbkdf2_sha256$1000000$FquO7UhJUEAGeyRC6K1X2o$eBksBn5Tdg4n2pxqvxiC5g4/hSS7I76wyQGYDjVfG9E=',NULL,1,'ADM004',NULL,NULL,'','','ADMIN','2025-10-02 18:13:08.322601','1990-01-01',1,1,NULL,1),
 (5,'pbkdf2_sha256$1000000$wv2eGVe5SZEXkLsK49GJzR$o53wZeQE2pqC3O1KqIoRHpQLrwZ4hlOupaX0YoaCaQI=','2025-10-08 09:15:43.289306',1,'ADM005',NULL,NULL,'','','ADMIN','2025-10-02 18:21:33.225045','1990-01-01',1,1,NULL,0),
 (6,'pbkdf2_sha256$1000000$SOdmj38oHk4iDqSwQzKJAV$gd9mTJEb3fAf9MN5C+zqvjkLooPLxXPCgh4aLRZ04R0=',NULL,0,'ETU-846983','ibrahimsaw@gmail.com','+2268687673','Ibra','Saw','ETUDIANT','2025-10-06 21:13:02.669332','1990-01-02',0,1,2,1),
 (7,'pbkdf2_sha256$1000000$v35x8CyMcIXrBztQ3aAanY$iwvRntx4V6XbY+VhSfbD8SHrZA4Gt00nsVVXBYauj0s=','2025-10-07 09:49:49.119108',0,'ETU-D78BCE','ibrahimsaw@gmail.com','+2268687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:27.276668','1990-01-01',0,1,2,0),
 (8,'pbkdf2_sha256$1000000$zWApWmMWrSkUzCjwbWVrec$GnNu9CRpAfOJjzXzruc1Wmcw1FYjtLZ8Eeq/fePkHl0=',NULL,0,'ETU-27C402','ibrahimsaw@gmail.com','+226687673','Ibra','SawK','ETUDIANT','2025-10-06 21:14:51.311986','1990-01-01',0,1,2,1);
INSERT INTO "Utilisateur_utilisateur_groups" ("id","utilisateur_id","group_id") VALUES (9,2,1),
 (17,8,4),
 (22,7,4),
 (24,6,4),
 (26,5,1);
INSERT INTO "auth_group" ("id","name") VALUES (1,'Groupe des administrateurs'),
 (2,'Groupe des agents administratifs'),
 (3,'Groupe des enseignants'),
 (4,'Groupe des étudiants'),
 (5,'Groupe des parents');
INSERT INTO "auth_group_permissions" ("id","group_id","permission_id") VALUES (1,1,1),
 (2,1,2),
 (3,1,3),
 (4,1,4),
 (5,1,5),
 (6,1,6),
 (7,1,7),
 (8,1,8),
 (9,1,9),
 (10,1,10),
 (11,1,11),
 (12,1,12),
 (13,1,13),
 (14,1,14),
 (15,1,15),
 (16,1,16),
 (17,1,17),
 (18,1,18),
 (19,1,19),
 (20,1,20),
 (21,1,21),
 (22,1,22),
 (23,1,23),
 (24,1,24),
 (25,1,25),
 (26,1,26),
 (27,1,27),
 (28,1,28),
 (29,1,29),
 (30,1,30),
 (31,1,31),
 (32,1,32),
 (33,1,33),
 (34,1,34),
 (35,1,35),
 (36,1,36),
 (37,1,37),
 (38,1,38),
 (39,1,39),
 (40,1,40),
 (41,1,41),
 (42,1,42),
 (43,1,43),
 (44,1,44),
 (45,1,45),
 (46,1,46),
 (47,1,47),
 (48,1,48),
 (49,1,49),
 (50,1,50),
 (51,1,51),
 (52,1,52),
 (53,1,53),
 (54,1,54),
 (55,1,55),
 (56,1,56),
 (57,1,57),
 (58,1,58),
 (59,1,59),
 (60,1,60),
 (61,1,61),
 (62,1,62),
 (63,1,63),
 (64,1,64),
 (65,1,65),
 (66,1,66),
 (67,1,67),
 (68,1,68),
 (69,1,69),
 (70,1,70),
 (71,1,71),
 (72,1,72),
 (73,1,73),
 (74,1,74),
 (75,1,75),
 (76,1,76),
 (77,1,77),
 (78,1,78),
 (79,1,79),
 (80,1,80),
 (81,1,81),
 (82,1,82),
 (83,1,83),
 (84,1,84),
 (85,1,85),
 (86,1,86),
 (87,1,87),
 (88,1,88),
 (89,1,89),
 (90,1,90),
 (91,1,91),
 (92,1,92),
 (93,1,93),
 (94,1,94),
 (95,1,95),
 (96,1,96),
 (97,1,97),
 (98,1,98),
 (99,1,99),
 (100,1,100),
 (101,1,101),
 (102,1,102),
 (103,1,103),
 (104,1,104),
 (105,1,105),
 (106,1,106),
 (107,1,107),
 (108,1,108),
 (109,1,109),
 (110,1,110),
 (111,1,111),
 (112,1,112),
 (113,1,113),
 (114,1,114),
 (115,1,115),
 (116,1,116),
 (117,1,117),
 (118,1,118),
 (119,1,119),
 (120,1,120),
 (121,1,121),
 (122,1,122),
 (123,1,123),
 (124,1,124),
 (125,1,125),
 (126,1,126),
 (127,1,127),
 (128,1,128),
 (129,1,129),
 (130,1,130),
 (131,1,131),
 (132,1,132),
 (133,1,133),
 (134,1,134),
 (135,1,135),
 (136,1,136),
 (137,1,137),
 (138,1,138),
 (139,1,139),
 (140,1,140),
 (141,1,141),
 (142,1,142),
 (143,1,143),
 (144,1,144),
 (145,1,145),
 (146,1,146),
 (147,1,147),
 (148,1,148),
 (149,1,149),
 (150,1,150),
 (151,1,151),
 (152,1,152),
 (153,1,153),
 (154,1,154),
 (155,1,155),
 (156,1,156),
 (157,1,157),
 (158,1,158),
 (159,1,159),
 (160,1,160),
 (161,1,161),
 (162,1,162),
 (163,1,163),
 (164,1,164),
 (165,1,165),
 (166,1,166),
 (167,1,167),
 (168,1,168),
 (169,2,96),
 (170,2,109),
 (171,2,110),
 (172,2,112),
 (173,2,24),
 (174,2,93),
 (175,2,94);
INSERT INTO "auth_permission" ("id","content_type_id","codename","name") VALUES (1,1,'add_logentry','Can add log entry'),
 (2,1,'change_logentry','Can change log entry'),
 (3,1,'delete_logentry','Can delete log entry'),
 (4,1,'view_logentry','Can view log entry'),
 (5,2,'add_permission','Can add permission'),
 (6,2,'change_permission','Can change permission'),
 (7,2,'delete_permission','Can delete permission'),
 (8,2,'view_permission','Can view permission'),
 (9,3,'add_group','Can add group'),
 (10,3,'change_group','Can change group'),
 (11,3,'delete_group','Can delete group'),
 (12,3,'view_group','Can view group'),
 (13,4,'add_contenttype','Can add content type'),
 (14,4,'change_contenttype','Can change content type'),
 (15,4,'delete_contenttype','Can delete content type'),
 (16,4,'view_contenttype','Can view content type'),
 (17,5,'add_session','Can add session'),
 (18,5,'change_session','Can change session'),
 (19,5,'delete_session','Can delete session'),
 (20,5,'view_session','Can view session'),
 (21,6,'add_utilisateur','Can add utilisateur'),
 (22,6,'change_utilisateur','Can change utilisateur'),
 (23,6,'delete_utilisateur','Can delete utilisateur'),
 (24,6,'view_utilisateur','Can view utilisateur'),
 (25,7,'add_genre','Can add Genre'),
 (26,7,'change_genre','Can change Genre'),
 (27,7,'delete_genre','Can delete Genre'),
 (28,7,'view_genre','Can view Genre'),
 (29,8,'add_specialite','Can add specialite'),
 (30,8,'change_specialite','Can change specialite'),
 (31,8,'delete_specialite','Can delete specialite'),
 (32,8,'view_specialite','Can view specialite'),
 (33,9,'add_adminsysteme','Can add admin systeme'),
 (34,9,'change_adminsysteme','Can change admin systeme'),
 (35,9,'delete_adminsysteme','Can delete admin systeme'),
 (36,9,'view_adminsysteme','Can view admin systeme'),
 (37,10,'add_etudiant','Can add etudiant'),
 (38,10,'change_etudiant','Can change etudiant'),
 (39,10,'delete_etudiant','Can delete etudiant'),
 (40,10,'view_etudiant','Can view etudiant'),
 (41,11,'add_fonctionagent','Can add Fonction d''agent'),
 (42,11,'change_fonctionagent','Can change Fonction d''agent'),
 (43,11,'delete_fonctionagent','Can delete Fonction d''agent'),
 (44,11,'view_fonctionagent','Can view Fonction d''agent'),
 (45,12,'add_rolepermission','Can add role permission'),
 (46,12,'change_rolepermission','Can change role permission'),
 (47,12,'delete_rolepermission','Can delete role permission'),
 (48,12,'view_rolepermission','Can view role permission'),
 (49,13,'add_agentadministration','Can add agent administration'),
 (50,13,'change_agentadministration','Can change agent administration'),
 (51,13,'delete_agentadministration','Can delete agent administration'),
 (52,13,'view_agentadministration','Can view agent administration'),
 (53,14,'add_enseignant','Can add enseignant'),
 (54,14,'change_enseignant','Can change enseignant'),
 (55,14,'delete_enseignant','Can delete enseignant'),
 (56,14,'view_enseignant','Can view enseignant'),
 (57,15,'add_parent','Can add parent'),
 (58,15,'change_parent','Can change parent'),
 (59,15,'delete_parent','Can delete parent'),
 (60,15,'view_parent','Can view parent'),
 (61,16,'add_document','Can add document'),
 (62,16,'change_document','Can change document'),
 (63,16,'delete_document','Can delete document'),
 (64,16,'view_document','Can view document'),
 (65,17,'add_frais','Can add frais'),
 (66,17,'change_frais','Can change frais'),
 (67,17,'delete_frais','Can delete frais'),
 (68,17,'view_frais','Can view frais'),
 (69,18,'add_inscription','Can add inscription'),
 (70,18,'change_inscription','Can change inscription'),
 (71,18,'delete_inscription','Can delete inscription'),
 (72,18,'view_inscription','Can view inscription'),
 (73,19,'add_notification','Can add notification'),
 (74,19,'change_notification','Can change notification'),
 (75,19,'delete_notification','Can delete notification'),
 (76,19,'view_notification','Can view notification'),
 (77,20,'add_paiement','Can add paiement'),
 (78,20,'change_paiement','Can change paiement'),
 (79,20,'delete_paiement','Can delete paiement'),
 (80,20,'view_paiement','Can view paiement'),
 (81,21,'add_devoir','Can add devoir'),
 (82,21,'change_devoir','Can change devoir'),
 (83,21,'delete_devoir','Can delete devoir'),
 (84,21,'view_devoir','Can view devoir'),
 (85,22,'add_documentinscription','Can add document inscription'),
 (86,22,'change_documentinscription','Can change document inscription'),
 (87,22,'delete_documentinscription','Can delete document inscription'),
 (88,22,'view_documentinscription','Can view document inscription'),
 (89,23,'add_anneeacademique','Can add Année Académique'),
 (90,23,'change_anneeacademique','Can change Année Académique'),
 (91,23,'delete_anneeacademique','Can delete Année Académique'),
 (92,23,'view_anneeacademique','Can view Année Académique'),
 (93,24,'add_formation','Can add formation'),
 (94,24,'change_formation','Can change formation'),
 (95,24,'delete_formation','Can delete formation'),
 (96,24,'view_formation','Can view formation'),
 (97,25,'add_parcours','Can add parcours'),
 (98,25,'change_parcours','Can change parcours'),
 (99,25,'delete_parcours','Can delete parcours'),
 (100,25,'view_parcours','Can view parcours'),
 (101,26,'add_specification','Can add Spécification'),
 (102,26,'change_specification','Can change Spécification'),
 (103,26,'delete_specification','Can delete Spécification'),
 (104,26,'view_specification','Can view Spécification'),
 (105,27,'add_typeformation','Can add Type de formation'),
 (106,27,'change_typeformation','Can change Type de formation'),
 (107,27,'delete_typeformation','Can delete Type de formation'),
 (108,27,'view_typeformation','Can view Type de formation'),
 (109,28,'add_classe','Can add classe'),
 (110,28,'change_classe','Can change classe'),
 (111,28,'delete_classe','Can delete classe'),
 (112,28,'view_classe','Can view classe'),
 (113,29,'add_metapermission','Can add Métadonnée de permission'),
 (114,29,'change_metapermission','Can change Métadonnée de permission'),
 (115,29,'delete_metapermission','Can delete Métadonnée de permission'),
 (116,29,'view_metapermission','Can view Métadonnée de permission'),
 (117,30,'add_historicaladminsysteme','Can add historical admin systeme'),
 (118,30,'change_historicaladminsysteme','Can change historical admin systeme'),
 (119,30,'delete_historicaladminsysteme','Can delete historical admin systeme'),
 (120,30,'view_historicaladminsysteme','Can view historical admin systeme'),
 (121,31,'add_historicalagentadministration','Can add historical agent administration'),
 (122,31,'change_historicalagentadministration','Can change historical agent administration'),
 (123,31,'delete_historicalagentadministration','Can delete historical agent administration'),
 (124,31,'view_historicalagentadministration','Can view historical agent administration'),
 (125,32,'add_historicalenseignant','Can add historical enseignant'),
 (126,32,'change_historicalenseignant','Can change historical enseignant'),
 (127,32,'delete_historicalenseignant','Can delete historical enseignant'),
 (128,32,'view_historicalenseignant','Can view historical enseignant'),
 (129,33,'add_historicaletudiant','Can add historical etudiant'),
 (130,33,'change_historicaletudiant','Can change historical etudiant'),
 (131,33,'delete_historicaletudiant','Can delete historical etudiant'),
 (132,33,'view_historicaletudiant','Can view historical etudiant'),
 (133,34,'add_historicalparent','Can add historical parent'),
 (134,34,'change_historicalparent','Can change historical parent'),
 (135,34,'delete_historicalparent','Can delete historical parent'),
 (136,34,'view_historicalparent','Can view historical parent'),
 (137,35,'add_historicalutilisateur','Can add historical utilisateur'),
 (138,35,'change_historicalutilisateur','Can change historical utilisateur'),
 (139,35,'delete_historicalutilisateur','Can delete historical utilisateur'),
 (140,35,'view_historicalutilisateur','Can view historical utilisateur'),
 (141,36,'add_historicalfrais','Can add historical frais'),
 (142,36,'change_historicalfrais','Can change historical frais'),
 (143,36,'delete_historicalfrais','Can delete historical frais'),
 (144,36,'view_historicalfrais','Can view historical frais'),
 (145,37,'add_historicalinscription','Can add historical inscription'),
 (146,37,'change_historicalinscription','Can change historical inscription'),
 (147,37,'delete_historicalinscription','Can delete historical inscription'),
 (148,37,'view_historicalinscription','Can view historical inscription'),
 (149,38,'add_historicalpaiement','Can add historical paiement'),
 (150,38,'change_historicalpaiement','Can change historical paiement'),
 (151,38,'delete_historicalpaiement','Can delete historical paiement'),
 (152,38,'view_historicalpaiement','Can view historical paiement'),
 (153,39,'add_historicalanneeacademique','Can add historical Année Académique'),
 (154,39,'change_historicalanneeacademique','Can change historical Année Académique'),
 (155,39,'delete_historicalanneeacademique','Can delete historical Année Académique'),
 (156,39,'view_historicalanneeacademique','Can view historical Année Académique'),
 (157,40,'add_historicalclasse','Can add historical classe'),
 (158,40,'change_historicalclasse','Can change historical classe'),
 (159,40,'delete_historicalclasse','Can delete historical classe'),
 (160,40,'view_historicalclasse','Can view historical classe'),
 (161,41,'add_historicalformation','Can add historical formation'),
 (162,41,'change_historicalformation','Can change historical formation'),
 (163,41,'delete_historicalformation','Can delete historical formation'),
 (164,41,'view_historicalformation','Can view historical formation'),
 (165,42,'add_historicalparcours','Can add historical parcours'),
 (166,42,'change_historicalparcours','Can change historical parcours'),
 (167,42,'delete_historicalparcours','Can delete historical parcours'),
 (168,42,'view_historicalparcours','Can view historical parcours');
INSERT INTO "django_content_type" ("id","app_label","model") VALUES (1,'admin','logentry'),
 (2,'auth','permission'),
 (3,'auth','group'),
 (4,'contenttypes','contenttype'),
 (5,'sessions','session'),
 (6,'Utilisateur','utilisateur'),
 (7,'Utilisateur','genre'),
 (8,'Utilisateur','specialite'),
 (9,'Utilisateur','adminsysteme'),
 (10,'Utilisateur','etudiant'),
 (11,'Utilisateur','fonctionagent'),
 (12,'Utilisateur','rolepermission'),
 (13,'Utilisateur','agentadministration'),
 (14,'Utilisateur','enseignant'),
 (15,'Utilisateur','parent'),
 (16,'Finance','document'),
 (17,'Finance','frais'),
 (18,'Finance','inscription'),
 (19,'Finance','notification'),
 (20,'Finance','paiement'),
 (21,'Finance','devoir'),
 (22,'Finance','documentinscription'),
 (23,'Formation','anneeacademique'),
 (24,'Formation','formation'),
 (25,'Formation','parcours'),
 (26,'Formation','specification'),
 (27,'Formation','typeformation'),
 (28,'Formation','classe'),
 (29,'Permissions_Manager','metapermission'),
 (30,'Utilisateur','historicaladminsysteme'),
 (31,'Utilisateur','historicalagentadministration'),
 (32,'Utilisateur','historicalenseignant'),
 (33,'Utilisateur','historicaletudiant'),
 (34,'Utilisateur','historicalparent'),
 (35,'Utilisateur','historicalutilisateur'),
 (36,'Finance','historicalfrais'),
 (37,'Finance','historicalinscription'),
 (38,'Finance','historicalpaiement'),
 (39,'Formation','historicalanneeacademique'),
 (40,'Formation','historicalclasse'),
 (41,'Formation','historicalformation'),
 (42,'Formation','historicalparcours');
INSERT INTO "django_migrations" ("id","app","name","applied") VALUES (1,'Formation','0001_initial','2025-10-02 17:49:52.098214'),
 (2,'Formation','0002_alter_formation_duree','2025-10-02 17:49:52.143020'),
 (3,'contenttypes','0001_initial','2025-10-02 17:49:52.174309'),
 (4,'contenttypes','0002_remove_content_type_name','2025-10-02 17:49:52.224027'),
 (5,'auth','0001_initial','2025-10-02 17:49:52.311853'),
 (6,'auth','0002_alter_permission_name_max_length','2025-10-02 17:49:52.376155'),
 (7,'auth','0003_alter_user_email_max_length','2025-10-02 17:49:52.421366'),
 (8,'auth','0004_alter_user_username_opts','2025-10-02 17:49:52.468970'),
 (9,'auth','0005_alter_user_last_login_null','2025-10-02 17:49:52.508499'),
 (10,'auth','0006_require_contenttypes_0002','2025-10-02 17:49:52.554476'),
 (11,'auth','0007_alter_validators_add_error_messages','2025-10-02 17:49:52.599689'),
 (12,'auth','0008_alter_user_username_max_length','2025-10-02 17:49:52.627247'),
 (13,'auth','0009_alter_user_last_name_max_length','2025-10-02 17:49:52.675485'),
 (14,'auth','0010_alter_group_name_max_length','2025-10-02 17:49:52.720326'),
 (15,'auth','0011_update_proxy_permissions','2025-10-02 17:49:52.777969'),
 (16,'auth','0012_alter_user_first_name_max_length','2025-10-02 17:49:52.811444'),
 (17,'Utilisateur','0001_initial','2025-10-02 17:49:52.996309'),
 (18,'Finance','0001_initial','2025-10-02 17:49:53.041941'),
 (19,'Finance','0002_initial','2025-10-02 17:49:53.316526'),
 (20,'Finance','0003_alter_paiement_methode_alter_paiement_reference','2025-10-02 17:49:53.381279'),
 (21,'Finance','0004_inscription_date_evenement_inscription_doucument_and_more','2025-10-02 17:49:53.571708'),
 (22,'Finance','0005_remove_inscription_doucument_and_more','2025-10-02 17:49:53.787695'),
 (23,'Finance','0006_alter_inscription_etablissement_accuiel','2025-10-02 17:49:53.861968'),
 (24,'Finance','0007_remove_inscription_unique_inscription_par_annee','2025-10-02 17:49:53.912004'),
 (25,'Finance','0008_alter_inscription_date_evenement','2025-10-02 17:49:53.968956'),
 (26,'Finance','0009_alter_inscription_date_evenement','2025-10-02 17:49:54.017212'),
 (27,'Finance','0010_alter_inscription_annee_academique_and_more','2025-10-02 17:49:54.151100'),
 (28,'Finance','0011_alter_inscription_classe_alter_inscription_parcours','2025-10-02 17:49:54.255882'),
 (29,'Permissions_Manager','0001_initial','2025-10-02 17:49:54.327459'),
 (30,'Utilisateur','0002_utilisateur_doit_changer_mot_de_passe','2025-10-02 17:49:54.388822'),
 (31,'admin','0001_initial','2025-10-02 17:49:54.486467'),
 (32,'admin','0002_logentry_remove_auto_add','2025-10-02 17:49:54.541023'),
 (33,'admin','0003_logentry_add_action_flag_choices','2025-10-02 17:49:54.582727'),
 (34,'sessions','0001_initial','2025-10-02 17:49:54.660194'),
 (35,'Utilisateur','0003_alter_utilisateur_doit_changer_mot_de_passe_and_more','2025-10-02 17:55:47.657790'),
 (36,'Formation','0003_historicalanneeacademique_historicalclasse_and_more','2025-10-02 17:55:47.868488'),
 (37,'Finance','0012_alter_inscription_etudiant_alter_inscription_statut_and_more','2025-10-02 17:55:48.157668');
INSERT INTO "django_session" ("session_key","session_data","expire_date") VALUES ('6ec41q6ezdn0a0y1jgups0aqj1nalit3','e30:1v4NYJ:uiN5oXKDxk7HFuA4vYYX0bbT6EHM01XPPt50xr1VUuU','2025-10-16 17:57:15.878605'),
 ('oj6l0czbfxf52xsvpqlphptjooeehrfk','e30:1v4NYw:4CIyMWNSzHgWulCbIigLi9DQY835jjQJ_sBbqyLaryA','2025-10-16 17:57:54.255203'),
 ('1u3daom51doaldk3cfqg5rxxq5e0fryq','.eJxVjEEOwiAQRe_C2hAKo4hL956BDDODRQ01pU00xrtrky50-9_776UizlMf5yZjLKwOaqs2v1tCukpdAF-wngdNQ53GkvSi6JU2fRpYbsfV_Qv02PrvmzKgNeR3hsRbSMw5kdiAAF1AZghos03kc8cUQHxwLuw7Z5wHSOCWaJPWylCjPO5lfKqDeX8Au84_bg:1v4NxM:LspRKoTM_vOf7wV7JztdXbeS11ZOEOvXT5Tog4x_x2I','2025-10-16 18:23:08.644671'),
 ('11hcuk1bxzoa33753e3yuxxpgf3sjlev','.eJxVjEsOwjAMBe-SNYpSp-lvyZ4zRHbs0gBKUNNKIMTdoVIXsH0zb17K47pMfi0y-8hqUE4dfjfCcJW0Ab5gOmcdclrmSHpT9E6LPmWW23F3_wITlun7BltXxvY8QuVq5rEmE6Dt-sYCMrMlAMJOBLgzBGxH12BPoa2MOOCWtmiRUmJOXh73OD_VYN4fiVw_Ww:1v4NyR:PJqgV8nY2J3VJlWXJgOH8ZjBfsw0nrOy18ZTxK4qkKw','2025-10-16 18:24:15.619216'),
 ('3tr9dsun15gs9f85m6pw16zoi0osp3ee','.eJxVjEsOwjAMBe-SNYpSp-lvyZ4zRHbs0gBKUNNKIMTdoVIXsH0zb17K47pMfi0y-8hqUE4dfjfCcJW0Ab5gOmcdclrmSHpT9E6LPmWW23F3_wITlun7BltXxvY8QuVq5rEmE6Dt-sYCMrMlAMJOBLgzBGxH12BPoa2MOOCWtmiRUmJOXh73OD_VYN4fiVw_Ww:1v4iw5:fqsApMr-SRVxM120YV_kC5k9g98rGTqEl9uJM11o-5w','2025-10-17 16:47:13.971761'),
 ('6d4gzmpq23qw7a0781s87dk6q7vca81e','.eJxVjEsOwjAMBe-SNYpSp-lvyZ4zRHbs0gBKUNNKIMTdoVIXsH0zb17K47pMfi0y-8hqUE4dfjfCcJW0Ab5gOmcdclrmSHpT9E6LPmWW23F3_wITlun7BltXxvY8QuVq5rEmE6Dt-sYCMrMlAMJOBLgzBGxH12BPoa2MOOCWtmiRUmJOXh73OD_VYN4fiVw_Ww:1v4niv:XWU6PxeqUoCCz2tw1flpY3SpT-bTVJbfL_9OrnL5O6I','2025-10-17 21:53:57.146105'),
 ('pbyzvtse5cz42rik10gur3bgboxd2fk3','.eJxVjEsOwjAMBe-SNYpSp-lvyZ4zRHbs0gBKUNNKIMTdoVIXsH0zb17K47pMfi0y-8hqUE4dfjfCcJW0Ab5gOmcdclrmSHpT9E6LPmWW23F3_wITlun7BltXxvY8QuVq5rEmE6Dt-sYCMrMlAMJOBLgzBGxH12BPoa2MOOCWtmiRUmJOXh73OD_VYN4fiVw_Ww:1v5hlG:5pIqaH2GdrQPFKsSp23MwNfNExdqnz7DDZ5xQqCXy64','2025-10-20 09:44:06.577516'),
 ('nlafm58kzylo2z9nlqiu2g8h2ht4ko96','.eJxVjEEOgjAQRe_StWkKTAPD0r1naKYzRaqmNRQSjfHugmGh2__efy_laJlHt5QwuSiqV606_G6e-BrSBuRC6Zw15zRP0etN0Tst-pQl3I67-xcYqYzrm6AJOHAAAiMVGpaBfcPQedsOtcUOpEbCxq-aIbTeotiKCMECC3yjJZQSc3LhcY_TU_Xm_QG2HT-u:1v63ye:rRnVa4BRIwTcoP8ixxTTeREOvPwHXQaYKE4xySkyED4','2025-10-21 09:27:24.587757'),
 ('uirxokmar8290i9q2nir6cs9mqyzniys','.eJxVjE0OwiAYRO_C2hAKtYUu3XsGwveDRQ2Y0iYa491tky40s5t5897Ch2Ue_VJ58onEIHpx-O0g4I3zNtA15EuRWPI8JZAbIve1ynMhvp929k8whjqubwttBDJrYtQOFQarXXMk61i7LhhlNcRWY8RomCyqviNAFxqjemUINmnlWlPJnp-PNL3EoD5fxp1AAw:1v64KL:_QgA1xnIb1aupiL9UFuCwuMk2SdYV28dYWZ-HLGooJ0','2025-10-21 09:49:49.168034'),
 ('yg86ol7tx4hokp4zh8vbtcqyxi0fx3gy','.eJxVjEsOwjAMBe-SNYpSp-lvyZ4zRHbs0gBKUNNKIMTdoVIXsH0zb17K47pMfi0y-8hqUE4dfjfCcJW0Ab5gOmcdclrmSHpT9E6LPmWW23F3_wITlun7BltXxvY8QuVq5rEmE6Dt-sYCMrMlAMJOBLgzBGxH12BPoa2MOOCWtmiRUmJOXh73OD_VYN4fiVw_Ww:1v6QGh:csNDfbdyFzEUUZPc3ucFXIsnl2tLKPgxAF1R7LQYu_0','2025-10-22 09:15:31.316183'),
 ('7g6758xkc1zcg9d5143va36jsky2kful','.eJxVjEsOwjAMBe-SNYpSp-lvyZ4zRHbs0gBKUNNKIMTdoVIXsH0zb17K47pMfi0y-8hqUE4dfjfCcJW0Ab5gOmcdclrmSHpT9E6LPmWW23F3_wITlun7BltXxvY8QuVq5rEmE6Dt-sYCMrMlAMJOBLgzBGxH12BPoa2MOOCWtmiRUmJOXh73OD_VYN4fiVw_Ww:1v6QGt:LZETl5NIxeLwLfh0kUyu-aXxpJlh0n-JKXzqodzsLYM','2025-10-22 09:15:43.381808');
CREATE INDEX "Finance_document_auteur_id_78a519d4" ON "Finance_document" ("auteur_id");
CREATE INDEX "Finance_documentinscription_inscription_id_36afd89f" ON "Finance_documentinscription" ("inscription_id");
CREATE INDEX "Finance_frais_classe_id_ea4a0d79" ON "Finance_frais" ("classe_id");
CREATE INDEX "Finance_historicalfrais_classe_id_9b8f33b6" ON "Finance_historicalfrais" ("classe_id");
CREATE INDEX "Finance_historicalfrais_history_date_3f280802" ON "Finance_historicalfrais" ("history_date");
CREATE INDEX "Finance_historicalfrais_history_user_id_1e31a747" ON "Finance_historicalfrais" ("history_user_id");
CREATE INDEX "Finance_historicalfrais_id_078be976" ON "Finance_historicalfrais" ("id");
CREATE INDEX "Finance_historicalinscription_annee_academique_id_d4020c59" ON "Finance_historicalinscription" ("annee_academique_id");
CREATE INDEX "Finance_historicalinscription_classe_id_fd4bf306" ON "Finance_historicalinscription" ("classe_id");
CREATE INDEX "Finance_historicalinscription_etudiant_id_ee932f26" ON "Finance_historicalinscription" ("etudiant_id");
CREATE INDEX "Finance_historicalinscription_history_date_bf8d8c9b" ON "Finance_historicalinscription" ("history_date");
CREATE INDEX "Finance_historicalinscription_history_user_id_3cf809ac" ON "Finance_historicalinscription" ("history_user_id");
CREATE INDEX "Finance_historicalinscription_id_7877b3ca" ON "Finance_historicalinscription" ("id");
CREATE INDEX "Finance_historicalinscription_parcours_id_279aece3" ON "Finance_historicalinscription" ("parcours_id");
CREATE INDEX "Finance_historicalpaiement_etudiant_id_f3a2be2a" ON "Finance_historicalpaiement" ("etudiant_id");
CREATE INDEX "Finance_historicalpaiement_frais_id_8be72f66" ON "Finance_historicalpaiement" ("frais_id");
CREATE INDEX "Finance_historicalpaiement_history_date_16336fb1" ON "Finance_historicalpaiement" ("history_date");
CREATE INDEX "Finance_historicalpaiement_history_user_id_6e2a4e87" ON "Finance_historicalpaiement" ("history_user_id");
CREATE INDEX "Finance_historicalpaiement_id_0080a60c" ON "Finance_historicalpaiement" ("id");
CREATE INDEX "Finance_historicalpaiement_reference_85f22f5f" ON "Finance_historicalpaiement" ("reference");
CREATE INDEX "Finance_inscription_annee_academique_id_f5e9542f" ON "Finance_inscription" ("annee_academique_id");
CREATE INDEX "Finance_inscription_classe_id_249f99ba" ON "Finance_inscription" ("classe_id");
CREATE INDEX "Finance_inscription_etudiant_id_6daa2cc4" ON "Finance_inscription" ("etudiant_id");
CREATE INDEX "Finance_inscription_parcours_id_1b2ac4da" ON "Finance_inscription" ("parcours_id");
CREATE INDEX "Finance_notification_utilisateur_id_92bdf54b" ON "Finance_notification" ("utilisateur_id");
CREATE INDEX "Finance_paiement_etudiant_id_e5498b26" ON "Finance_paiement" ("etudiant_id");
CREATE INDEX "Finance_paiement_frais_id_4d62b048" ON "Finance_paiement" ("frais_id");
CREATE INDEX "Formation_classe_annee_academique_id_97581707" ON "Formation_classe" ("annee_academique_id");
CREATE INDEX "Formation_classe_formation_id_61c79929" ON "Formation_classe" ("formation_id");
CREATE INDEX "Formation_formation_parcours_id_d9da748a" ON "Formation_formation" ("parcours_id");
CREATE INDEX "Formation_historicalanneeacademique_history_date_f4d3987a" ON "Formation_historicalanneeacademique" ("history_date");
CREATE INDEX "Formation_historicalanneeacademique_history_user_id_c11775de" ON "Formation_historicalanneeacademique" ("history_user_id");
CREATE INDEX "Formation_historicalanneeacademique_id_fd9312db" ON "Formation_historicalanneeacademique" ("id");
CREATE INDEX "Formation_historicalanneeacademique_nom_0a6a6d3d" ON "Formation_historicalanneeacademique" ("nom");
CREATE INDEX "Formation_historicalclasse_annee_academique_id_93b8f3cc" ON "Formation_historicalclasse" ("annee_academique_id");
CREATE INDEX "Formation_historicalclasse_formation_id_0db3f168" ON "Formation_historicalclasse" ("formation_id");
CREATE INDEX "Formation_historicalclasse_history_date_9e30c015" ON "Formation_historicalclasse" ("history_date");
CREATE INDEX "Formation_historicalclasse_history_user_id_69efde8a" ON "Formation_historicalclasse" ("history_user_id");
CREATE INDEX "Formation_historicalclasse_id_50794392" ON "Formation_historicalclasse" ("id");
CREATE INDEX "Formation_historicalformation_history_date_b68c0f19" ON "Formation_historicalformation" ("history_date");
CREATE INDEX "Formation_historicalformation_history_user_id_ff115f1f" ON "Formation_historicalformation" ("history_user_id");
CREATE INDEX "Formation_historicalformation_id_360135d6" ON "Formation_historicalformation" ("id");
CREATE INDEX "Formation_historicalformation_parcours_id_dae370d6" ON "Formation_historicalformation" ("parcours_id");
CREATE INDEX "Formation_historicalparcours_history_date_c4cf6c88" ON "Formation_historicalparcours" ("history_date");
CREATE INDEX "Formation_historicalparcours_history_user_id_4d8afd18" ON "Formation_historicalparcours" ("history_user_id");
CREATE INDEX "Formation_historicalparcours_id_101296aa" ON "Formation_historicalparcours" ("id");
CREATE INDEX "Formation_historicalparcours_specification_id_eb8643f5" ON "Formation_historicalparcours" ("specification_id");
CREATE INDEX "Formation_historicalparcours_type_formation_id_d5913457" ON "Formation_historicalparcours" ("type_formation_id");
CREATE INDEX "Formation_parcours_specification_id_eaf1b15a" ON "Formation_parcours" ("specification_id");
CREATE INDEX "Formation_parcours_type_formation_id_73993bbd" ON "Formation_parcours" ("type_formation_id");
CREATE INDEX "Utilisateur_agentadministration_fonctions_agentadministration_id_ee7eaf3b" ON "Utilisateur_agentadministration_fonctions" ("agentadministration_id");
CREATE UNIQUE INDEX "Utilisateur_agentadministration_fonctions_agentadministration_id_fonctionagent_id_9cf335fa_uniq" ON "Utilisateur_agentadministration_fonctions" ("agentadministration_id", "fonctionagent_id");
CREATE INDEX "Utilisateur_agentadministration_fonctions_fonctionagent_id_fff45faf" ON "Utilisateur_agentadministration_fonctions" ("fonctionagent_id");
CREATE INDEX "Utilisateur_enseignant_specialites_enseignant_id_8beed188" ON "Utilisateur_enseignant_specialites" ("enseignant_id");
CREATE UNIQUE INDEX "Utilisateur_enseignant_specialites_enseignant_id_specialite_id_8001a09f_uniq" ON "Utilisateur_enseignant_specialites" ("enseignant_id", "specialite_id");
CREATE INDEX "Utilisateur_enseignant_specialites_specialite_id_b418ec25" ON "Utilisateur_enseignant_specialites" ("specialite_id");
CREATE INDEX "Utilisateur_fonctionagent_permissions_fonctionagent_id_27e34c91" ON "Utilisateur_fonctionagent_permissions" ("fonctionagent_id");
CREATE UNIQUE INDEX "Utilisateur_fonctionagent_permissions_fonctionagent_id_permission_id_24fc4ad9_uniq" ON "Utilisateur_fonctionagent_permissions" ("fonctionagent_id", "permission_id");
CREATE INDEX "Utilisateur_fonctionagent_permissions_permission_id_e3ef9117" ON "Utilisateur_fonctionagent_permissions" ("permission_id");
CREATE INDEX "Utilisateur_historicaladminsysteme_history_date_dffba0ef" ON "Utilisateur_historicaladminsysteme" ("history_date");
CREATE INDEX "Utilisateur_historicaladminsysteme_history_user_id_371dc615" ON "Utilisateur_historicaladminsysteme" ("history_user_id");
CREATE INDEX "Utilisateur_historicaladminsysteme_utilisateur_id_4a3fd278" ON "Utilisateur_historicaladminsysteme" ("utilisateur_id");
CREATE INDEX "Utilisateur_historicalagentadministration_history_date_62c92646" ON "Utilisateur_historicalagentadministration" ("history_date");
CREATE INDEX "Utilisateur_historicalagentadministration_history_user_id_18644699" ON "Utilisateur_historicalagentadministration" ("history_user_id");
CREATE INDEX "Utilisateur_historicalagentadministration_utilisateur_id_5ce51c34" ON "Utilisateur_historicalagentadministration" ("utilisateur_id");
CREATE INDEX "Utilisateur_historicalenseignant_history_date_93f8e923" ON "Utilisateur_historicalenseignant" ("history_date");
CREATE INDEX "Utilisateur_historicalenseignant_history_user_id_bcf7421b" ON "Utilisateur_historicalenseignant" ("history_user_id");
CREATE INDEX "Utilisateur_historicalenseignant_utilisateur_id_e5e7b937" ON "Utilisateur_historicalenseignant" ("utilisateur_id");
CREATE INDEX "Utilisateur_historicaletudiant_history_date_974bf1f3" ON "Utilisateur_historicaletudiant" ("history_date");
CREATE INDEX "Utilisateur_historicaletudiant_history_user_id_ae37b8b8" ON "Utilisateur_historicaletudiant" ("history_user_id");
CREATE INDEX "Utilisateur_historicaletudiant_utilisateur_id_2a0e94b6" ON "Utilisateur_historicaletudiant" ("utilisateur_id");
CREATE INDEX "Utilisateur_historicalparent_history_date_aa28f432" ON "Utilisateur_historicalparent" ("history_date");
CREATE INDEX "Utilisateur_historicalparent_history_user_id_4b644a0d" ON "Utilisateur_historicalparent" ("history_user_id");
CREATE INDEX "Utilisateur_historicalparent_utilisateur_id_707ed492" ON "Utilisateur_historicalparent" ("utilisateur_id");
CREATE INDEX "Utilisateur_historicalutilisateur_genre_id_0114515b" ON "Utilisateur_historicalutilisateur" ("genre_id");
CREATE INDEX "Utilisateur_historicalutilisateur_history_date_8bc29a96" ON "Utilisateur_historicalutilisateur" ("history_date");
CREATE INDEX "Utilisateur_historicalutilisateur_history_user_id_ded493c6" ON "Utilisateur_historicalutilisateur" ("history_user_id");
CREATE INDEX "Utilisateur_historicalutilisateur_id_6ca6d67b" ON "Utilisateur_historicalutilisateur" ("id");
CREATE INDEX "Utilisateur_historicalutilisateur_matricule_978938b1" ON "Utilisateur_historicalutilisateur" ("matricule");
CREATE INDEX "Utilisateur_parent_enfants_etudiant_id_3c764d44" ON "Utilisateur_parent_enfants" ("etudiant_id");
CREATE INDEX "Utilisateur_parent_enfants_parent_id_09cae3aa" ON "Utilisateur_parent_enfants" ("parent_id");
CREATE UNIQUE INDEX "Utilisateur_parent_enfants_parent_id_etudiant_id_a3f00d72_uniq" ON "Utilisateur_parent_enfants" ("parent_id", "etudiant_id");
CREATE INDEX "Utilisateur_rolepermission_permissions_permission_id_fc590b15" ON "Utilisateur_rolepermission_permissions" ("permission_id");
CREATE INDEX "Utilisateur_rolepermission_permissions_rolepermission_id_a3092979" ON "Utilisateur_rolepermission_permissions" ("rolepermission_id");
CREATE UNIQUE INDEX "Utilisateur_rolepermission_permissions_rolepermission_id_permission_id_0025996f_uniq" ON "Utilisateur_rolepermission_permissions" ("rolepermission_id", "permission_id");
CREATE INDEX "Utilisateur_utilisateur_genre_id_f5a957da" ON "Utilisateur_utilisateur" ("genre_id");
CREATE INDEX "Utilisateur_utilisateur_groups_group_id_47f1d85a" ON "Utilisateur_utilisateur_groups" ("group_id");
CREATE INDEX "Utilisateur_utilisateur_groups_utilisateur_id_a4666844" ON "Utilisateur_utilisateur_groups" ("utilisateur_id");
CREATE UNIQUE INDEX "Utilisateur_utilisateur_groups_utilisateur_id_group_id_cff792c6_uniq" ON "Utilisateur_utilisateur_groups" ("utilisateur_id", "group_id");
CREATE INDEX "Utilisateur_utilisateur_user_permissions_permission_id_e9f382e5" ON "Utilisateur_utilisateur_user_permissions" ("permission_id");
CREATE INDEX "Utilisateur_utilisateur_user_permissions_utilisateur_id_de39a63d" ON "Utilisateur_utilisateur_user_permissions" ("utilisateur_id");
CREATE UNIQUE INDEX "Utilisateur_utilisateur_user_permissions_utilisateur_id_permission_id_ff925b9e_uniq" ON "Utilisateur_utilisateur_user_permissions" ("utilisateur_id", "permission_id");
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" ("group_id");
CREATE UNIQUE INDEX "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" ("group_id", "permission_id");
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" ("permission_id");
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "auth_permission" ("content_type_id");
CREATE UNIQUE INDEX "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" ("content_type_id", "codename");
CREATE INDEX "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" ("content_type_id");
CREATE INDEX "django_admin_log_user_id_c564eba6" ON "django_admin_log" ("user_id");
CREATE UNIQUE INDEX "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" ("app_label", "model");
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");
COMMIT;
