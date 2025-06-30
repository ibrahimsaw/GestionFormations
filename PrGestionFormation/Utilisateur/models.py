from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission,Group
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid
from datetime import date
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinLengthValidator


class CustomUserManager(BaseUserManager):
    def _create_user(self, matricule, password=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec le matricule et mot de passe
        """
        if not matricule:
            raise ValueError('Le matricule est obligatoire')

        user = self.model(matricule=matricule, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, matricule, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(matricule, password, **extra_fields)

    def create_superuser(self, matricule, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self._create_user(matricule, password, **extra_fields)




class Genre(models.Model):
    code = models.CharField(max_length=10, unique=True)
    libelle = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    est_par_defaut = models.BooleanField(default=False)

    def __str__(self):
        return self.libelle

    @classmethod
    def initialiser_genres(cls):
        # Liste des genres avec "Non précisé" comme défaut
        genres = [
            {'code': 'F', 'libelle': 'Femme', 'description': 'Genre féminin', 'est_par_defaut': False},
            {'code': 'H', 'libelle': 'Homme', 'description': 'Genre masculin', 'est_par_defaut': False},
            {'code': 'ND', 'libelle': 'Non précisé', 'description': 'Genre non déclaré', 'est_par_defaut': True},
        ]

        for data in genres:
            cls.objects.get_or_create(code=data['code'], defaults=data)

    @classmethod
    def get_default_genre(cls):
        try:
            return cls.objects.get(est_par_defaut=True).id
        except:
            return None  # Retourne None si la table n'existe pas ou aucun défaut

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"



class Utilisateur(AbstractBaseUser, PermissionsMixin):
    print("\nInitialisation de la classe Utilisateur...")
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrateur Système'
        AGENT = 'AGENT', 'Agent administratif'
        ENSEIGNANT = 'ENSEIGNANT', 'Enseignant'
        ETUDIANT = 'ETUDIANT', 'Étudiant'
        PARENT = 'PARENT', 'Parent'

    # Champs d'authentification
    matricule = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    # Champs personnels
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    date_inscription = models.DateTimeField(auto_now_add=True)
    date_nais = models.DateField(default=date(1990, 1, 1))
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,  # Temporairement à None
        verbose_name="Genre"
    )
    # Champs requis pour AbstractBaseUser
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'matricule'
    REQUIRED_FIELDS = ['role']



    def __str__(self):
        return f"{self.matricule} ({self.get_role_display()})"

    @classmethod
    def create_admin_user(cls, matricule, password, **extra_fields):
        """Méthode sécurisée pour créer un admin système"""
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('role', cls.Role.ADMIN)

        if extra_fields.get('role') != cls.Role.ADMIN:
            raise ValueError("Le rôle doit être ADMIN pour un administrateur système")

        user = cls.objects.create_user(
            matricule=matricule,
            password=password,
            **extra_fields
        )
        return user

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_role_display_name(self):
        """Retourne le nom d'affichage complet du rôle"""
        return self.get_role_display()

    # Ou sous forme de propriété pour un accès plus naturel
    @property
    def role_display(self):
        """Retourne le nom d'affichage complet du rôle (propriété)"""
        return self.get_role_display()
    # Utilisateur/models.py
    def assign_role_permissions(self):
        """Attribue les permissions selon le type de profil"""
        print(f"\nDébut assign_role_permissions() pour {self.matricule}")

        try:
            # Récupère la configuration des permissions pour ce rôle
            role = self.role
            print(f"Le role : {role}")
            role_perm = RolePermission.objects.get(role=role)
            print(f"Configuration trouvée: {role_perm}")

            # Nettoie les groupes existants
            self.groups.clear()
            print("Groupes existants nettoyés")

            # Ajoute au groupe correspondant
            self.groups.add(role_perm.groupe)
            print(f"Ajouté au groupe: {role_perm.groupe.name}")

            # Pour les admins, on active les flags
            if self.role == self.Role.ADMIN:
                self.is_staff = True
                self.is_superuser = True
                print("Défini comme superutilisateur (admin)")

        except Exception as e:
            print(f"ERREUR dans assign_role_permissions: {str(e)}")
            raise

    def save(self, *args, **kwargs):
        """Sauvegarde avec gestion du matricule et des permissions"""
        print(f"\nSauvegarde Utilisateur {self.matricule or 'nouveau'}")

        # Génération du matricule si vide
        if not self.matricule:
            prefix = {
                'ADMIN': 'ADM',
                'AGENT': 'AGT',
                'ENSEIGNANT': 'ENS',
                'ETUDIANT': 'ETU',
                'PARENT': 'PAR'
            }.get(self.role, 'USR')
            self.matricule = f"{prefix}-{uuid.uuid4().hex[:6].upper()}"
            print(f"Matricule généré: {self.matricule}")

        # Sauvegarde d'abord l'utilisateur
        super().save(*args, **kwargs)

        # Puis attribution des permissions
        self.assign_role_permissions()
        print("Utilisateur sauvegardé avec permissions")




class FonctionAgent(models.Model):
    code = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(3)],
        help_text="Code unique de la fonction (ex: SECRETAIRE_ADMIN)"
    )
    nom = models.CharField(
        max_length=100,
        help_text="Nom complet de la fonction (ex: Secrétaire administratif)"
    )
    description = models.TextField(
        help_text="Description détaillée du rôle et des missions"
    )
    responsabilites = models.JSONField(
        default=list,
        help_text="Liste des responsabilités principales"
    )
    controles = models.JSONField(
        default=list,
        help_text="Liste des mécanismes de contrôle associés"
    )
    protocoles = models.JSONField(
        default=list,
        help_text="Liste des protocoles et procédures spécifiques"
    )
    role = models.CharField(
        max_length=20,
        choices=Utilisateur.Role.choices,
        default=Utilisateur.Role.AGENT,
        editable=False
    )

    # Définition des permissions disponibles structurées
    PERMISSIONS_DISPONIBLES = {
        'formation': {
            'view': 'Voir les formations',
            'add': 'Ajouter une formation',
            'change': 'Modifier une formation',
            'delete': 'Supprimer une formation'
        },
        'classe': {
            'view': 'Voir les classes',
            'add': 'Ajouter une classe',
            'change': 'Modifier une classe'
        },
        'utilisateur': {
            'view': 'Voir les utilisateurs'
        },
        'courrier': {
            'view': 'Voir le courrier',
            'add': 'Ajouter du courrier'
        },
        'dossier': {
            'view': 'Voir les dossiers',
            'change': 'Modifier les dossiers'
        }
    }

    permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='fonctions_agent',
        limit_choices_to={'codename__in': []},  # Initialisé vide, rempli dans la méthode
        help_text="Permissions spécifiques à cette fonction"
    )

    @classmethod
    def get_allowed_permissions(cls):
        """Retourne la liste des noms de permissions autorisées"""
        return [
            f"{action}_{model}"
            for model, actions in cls.PERMISSIONS_DISPONIBLES.items()
            for action in actions.keys()
        ]

    class Meta:
        ordering = ['nom']
        verbose_name = "Fonction d'agent"
        verbose_name_plural = "Fonctions d'agents"

    def __str__(self):
        return self.nom

    @classmethod
    def get_permissions_choices(cls):
        """
        Génère dynamiquement les paires (codename, description)
        à partir de votre structure existante
        """
        permissions = []
        for model, actions in cls.PERMISSIONS_DISPONIBLES.items():
            model_perms = []
            for action, description in actions.items():
                codename = f"{action}_{model}"
                model_perms.append((codename, {
                    'name': codename,
                    'description': description
                }))
                print(codame)
                print(description)
            permissions.append((model, model_perms))
        return permissions

    @classmethod
    def creer_permissions(cls):
        """Crée les permissions en base si elles n'existent pas"""
        ContentType = apps.get_model('contenttypes', 'ContentType')
        Permission = apps.get_model('auth', 'Permission')
        created = []

        for model, actions in cls.PERMISSIONS_DISPONIBLES.items():
            try:
                content_type = ContentType.objects.get(
                    app_label='votre_app',  # À adapter!
                    model=model
                )

                for action, name in actions.items():
                    codename = f"{action}_{model}"
                    perm, is_new = Permission.objects.get_or_create(
                        codename=codename,
                        content_type=content_type,
                        defaults={'name': name}
                    )
                    if is_new:
                        created.append(perm)

            except ContentType.DoesNotExist:
                print(f"Attention: ContentType pour {model} non trouvé")
                continue

        return created

    def clean(self):
        Utilisateur = apps.get_model('Utilisateur', 'Utilisateur')
        if self.role != Utilisateur.Role.AGENT:
            raise ValidationError("Une fonction doit être associée au rôle AGENT.")

        # Validation supplémentaire pour s'assurer que les permissions sont valides
        if self.pk:  # Only check if instance already exists
            valid_permissions = [
                f"{action}_{model}"
                for model, actions in self.PERMISSIONS_DISPONIBLES.items()
                for action in actions.keys()
            ]
            invalid_perms = self.permissions.exclude(codename__in=valid_permissions)
            if invalid_perms.exists():
                raise ValidationError(
                    f"Certaines permissions ne sont pas autorisées: {', '.join(invalid_perms.values_list('codename', flat=True))}"
                )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @classmethod
    def initialiser_fonctions(cls):
        try:
            role_agent = Utilisateur.Role.AGENT
        except Role.DoesNotExist:
            raise Exception("Le rôle AGENT doit être créé avant les fonctions")

        fonctions = [
            {
                'code': 'SECRETAIRE_ADMINISTRATIF',
                'nom': 'Secrétaire administratif',
                'description': "Gestion centralisée du courrier et documents administratifs",
                'responsabilites': [
                    "Gestion du courrier entrant/sortant",
                    "Classement et archivage des documents",
                    "Accueil physique et téléphonique",
                    "Préparation des dossiers pour réunions",
                    "Saisie des données administratives"
                ],
                'controles': [
                    "Vérification quotidienne du bon acheminement du courrier",
                    "Audit mensuel des dossiers archivés"
                ],
                'protocoles': [
                    "Procédure de traitement du courrier confidentiel",
                    "Protocole de destruction des documents obsolètes"
                ]
            },
            {
                'code': 'CHARGE_INSCRIPTIONS',
                'nom': 'Chargé des inscriptions',
                'description': "Gestion du processus complet d'inscription des étudiants",
                'responsabilites': [
                    "Vérification des dossiers d'inscription",
                    "Enregistrement des nouveaux étudiants",
                    "Gestion des dérogations",
                    "Coordination avec le service financier",
                    "Mise à jour des fichiers étudiants"
                ],
                'controles': [
                    "Contrôle aléatoire de 10% des dossiers",
                    "Vérification des pièces justificatives"
                ],
                'protocoles': [
                    "Procédure de validation des dérogations",
                    "Protocole RGPD pour les données personnelles"
                ]
            },
            {
                'code': 'GESTIONNAIRE_DOSSIERS',
                'nom': 'Gestionnaire des dossiers étudiants',
                'description': "Maintenance et mise à jour des dossiers étudiants",
                'responsabilites': [
                    "Maintenance des dossiers étudiants",
                    "Vérification des pièces manquantes",
                    "Archivage numérique et physique",
                    "Réponse aux demandes d'accès",
                    "Application des règles RGPD"
                ],
                'controles': [
                    "Vérification trimestrielle de l'exhaustivité des dossiers",
                    "Contrôle d'accès aux documents sensibles"
                ],
                'protocoles': [
                    "Protocole de mise à jour des dossiers",
                    "Procédure de réponse aux demandes légales"
                ]
            },
            {
                'code': 'AGENT_SCOLARITE',
                'nom': 'Agent de scolarité',
                'description': "Gestion administrative des parcours étudiants",
                'responsabilites': [
                    "Suivi des inscriptions pédagogiques",
                    "Gestion des changements de filière",
                    "Édition des attestations",
                    "Coordination avec les départements",
                    "Traitement des demandes spéciales"
                ],
                'controles': [
                    "Vérification des prérequis académiques",
                    "Contrôle des droits d'inscription"
                ],
                'protocoles': [
                    "Procédure de changement de parcours",
                    "Protocole d'édition des documents officiels"
                ]
            },
            {
                'code': 'RESPONSABLE_EMPLOI_TEMPS',
                'nom': 'Responsable des emplois du temps',
                'description': "Création et gestion des plannings académiques",
                'responsabilites': [
                    "Élaboration des plannings",
                    "Gestion des salles et ressources",
                    "Résolution des conflits d'horaire",
                    "Publication des calendriers",
                    "Coordination avec les enseignants"
                ],
                'controles': [
                    "Vérification de l'adéquation salles/effectifs",
                    "Contrôle du respect des volumes horaires"
                ],
                'protocoles': [
                    "Protocole de modification des plannings",
                    "Procédure d'urgence pour salles indisponibles"
                ]
            },
            {
                'code': 'AGENT_DISCIPLINE',
                'nom': 'Agent chargé de la discipline',
                'description': "Application du règlement intérieur et suivi disciplinaire",
                'responsabilites': [
                    "Enregistrement des incidents",
                    "Application du règlement intérieur",
                    "Suivi des mesures disciplinaires",
                    "Communication avec les familles",
                    "Rapports mensuels"
                ],
                'controles': [
                    "Vérification de la proportionnalité des sanctions",
                    "Contrôle du suivi des mesures"
                ],
                'protocoles': [
                    "Procédure de traitement des incidents graves",
                    "Protocole de signalement aux autorités compétentes"
                ]
            },
            {
                'code': 'CHARGE_EXAMENS',
                'nom': 'Chargé des examens et concours',
                'description': "Organisation logistique des évaluations académiques",
                'responsabilites': [
                    "Organisation des sessions d'examen",
                    "Gestion des sujets et copies",
                    "Coordination des surveillances",
                    "Sécurisation des épreuves",
                    "Traitement des fraudes"
                ],
                'controles': [
                    "Double vérification des sujets",
                    "Contrôle d'identité strict en salle"
                ],
                'protocoles': [
                    "Protocole de sécurisation des sujets",
                    "Procédure de traitement des fraudes"
                ]
            },
            {
                'code': 'RESPONSABLE_BULLETINS',
                'nom': 'Responsable des bulletins et relevés de notes',
                'description': "Gestion et diffusion des résultats académiques",
                'responsabilites': [
                    "Saisie et vérification des notes",
                    "Édition des relevés de notes",
                    "Gestion des réclamations",
                    "Archivage des résultats",
                    "Calcul des moyennes"
                ],
                'controles': [
                    "Double contrôle des calculs de moyennes",
                    "Vérification des validations pédagogiques"
                ],
                'protocoles': [
                    "Protocole de correction des erreurs",
                    "Procédure de traitement des réclamations"
                ]
            },
            {
                'code': 'AGENT_ATTESTATIONS',
                'nom': 'Agent chargé des attestations et diplômes',
                'description': "Émission et gestion des documents officiels",
                'responsabilites': [
                    "Émission des documents officiels",
                    "Gestion des demandes de duplicata",
                    "Vérification des droits",
                    "Archivage sécurisé",
                    "Lutte contre la fraude"
                ],
                'controles': [
                    "Vérification systématique des droits",
                    "Contrôle qualité avant émission"
                ],
                'protocoles': [
                    "Procédure d'émission des duplicata",
                    "Protocole anti-fraude des documents"
                ]
            },
            {
                'code': 'GESTIONNAIRE_COURRIER',
                'nom': 'Gestionnaire du courrier administratif',
                'description': "Gestion du flux de courrier institutionnel",
                'responsabilites': [
                    "Tri et distribution du courrier",
                    "Gestion des envois institutionnels",
                    "Traçabilité des expéditions",
                    "Numérisation des documents",
                    "Classement chronologique"
                ],
                'controles': [
                    "Traçabilité complète des envois",
                    "Vérification des accusés de réception"
                ],
                'protocoles': [
                    "Protocole pour courrier confidentiel",
                    "Procédure d'urgence pour courrier recommandé"
                ]
            },
            {
                'code': 'SUIVI_ENSEIGNANTS',
                'nom': 'Responsable du suivi des enseignants',
                'description': "Gestion administrative des intervenants pédagogiques",
                'responsabilites': [
                    "Suivi des contrats enseignants",
                    "Gestion des services horaires",
                    "Interface avec les services RH"
                ],
                'controles': [
                    "Vérification des qualifications",
                    "Contrôle du respect des volumes horaires"
                ],
                'protocoles': [
                    "Protocole de recrutement des vacataires",
                    "Procédure de signalement des absences"
                ]
            },
            {
                'code': 'LIAISON_PEDAGOGIQUE',
                'nom': 'Agent de liaison pédagogique',
                'description': "Interface entre administration et corps enseignant",
                'responsabilites': [
                    "Transmission des informations pédagogiques",
                    "Remontée des besoins matériels",
                    "Organisation des réunions pédagogiques"
                ],
                'controles': [
                    "Suivi des comptes-rendus de réunion",
                    "Vérification de la diffusion des informations"
                ],
                'protocoles': [
                    "Protocole de circulation de l'information",
                    "Procédure d'urgence pour problèmes pédagogiques"
                ]
            },
            {
                'code': 'RESSOURCES_MATERIELLES',
                'nom': 'Agent de gestion des ressources matérielles',
                'description': "Gestion du patrimoine matériel pédagogique",
                'responsabilites': [
                    "Inventaire du matériel",
                    "Gestion des prêts",
                    "Organisation de la maintenance"
                ],
                'controles': [
                    "Vérification trimestrielle des stocks",
                    "Contrôle des conditions de sécurité"
                ],
                'protocoles': [
                    "Protocole de prêt de matériel",
                    "Procédure de signalement des dysfonctionnements"
                ]
            },
            {
                'code': 'CHARGE_CONVOCATIONS',
                'nom': 'Chargé des convocations',
                'description': "Gestion des convocations officielles",
                'responsabilites': [
                    "Édition des convocations",
                    "Gestion des envois",
                    "Suivi des confirmations"
                ],
                'controles': [
                    "Vérification des listes de destinataires",
                    "Contrôle des accusés de réception"
                ],
                'protocoles': [
                    "Protocole pour convocations urgentes",
                    "Procédure de relance des absents"
                ]
            },
            {
                'code': 'BASE_DONNEES_ETUDIANTS',
                'nom': 'Responsable de la base de données étudiants',
                'description': "Gestion et sécurisation des données étudiantes",
                'responsabilites': [
                    "Mise à jour des données",
                    "Sauvegarde des informations",
                    "Gestion des accès"
                ],
                'controles': [
                    "Vérification quotidienne des sauvegardes",
                    "Audit semestriel des accès"
                ],
                'protocoles': [
                    "Protocole RGPD pour données sensibles",
                    "Procédure de récupération après incident"
                ]
            },
            {
                'code': 'AGENT_ACCUEIL',
                'nom': "Agent d'accueil et d'information",
                'description': "Premier contact avec l'institution",
                'responsabilites': [
                    "Accueil physique et téléphonique",
                    "Orientation des visiteurs",
                    "Gestion des demandes courantes"
                ],
                'controles': [
                    "Mesure de la satisfaction usagers",
                    "Suivi du temps d'attente"
                ],
                'protocoles': [
                    "Protocole d'accueil des personnes à mobilité réduite",
                    "Procédure pour situations d'urgence"
                ]
            },
            {
                'code': 'AGENT_COMPTABLE',
                'nom': 'Agent comptable',
                'description': "Gestion des aspects financiers étudiants",
                'responsabilites': [
                    "Encaissement des frais de scolarité",
                    "Gestion des échéanciers",
                    "Rapprochement bancaire"
                ],
                'controles': [
                    "Vérification quotidienne des encaissements",
                    "Contrôle mensuel des impayés"
                ],
                'protocoles': [
                    "Protocole de traitement des paiements en retard",
                    "Procédure de remboursement"
                ]
            }
        ]

        for data in fonctions:
            fonction, created = cls.objects.get_or_create(
                code=data['code'],
                defaults={
                    'nom': data['nom'],
                    'description': data['description'],
                    'responsabilites': data.get('responsabilites', []),
                    'controles': data.get('controles', []),
                    'protocoles': data.get('protocoles', [])
                }
            )
            if not created:
                fonction.nom = data['nom']
                fonction.description = data['description']
                fonction.save()






class AdminSysteme(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key = True,
        limit_choices_to = {'role': Utilisateur.Role.ADMIN, 'is_superuser': True}
    )

    def save(self, *args, **kwargs):
        # Vérifie que l'utilisateur est bien ADMIN ET superuser
        print(self.utilisateur.role)
        print(Utilisateur.Role.ADMIN)
        print(self.utilisateur.is_superuser)
        # if self.utilisateur.role != Utilisateur.Role.ADMIN or not self.utilisateur.is_superuser:
        #     raise ValueError(
        #         "L'utilisateur doit avoir le rôle ADMIN ET être superutilisateur "
        #         "pour être AdminSysteme."
        #     )
        super().save(*args, **kwargs)

class AgentAdministration(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'role': 'AGENT'}
    )
    fonctions = models.ManyToManyField(FonctionAgent)  # Plus de unique_together ici

    def __str__(self):
        return f"{self.utilisateur} - {', '.join(f.nom for f in self.fonctions.all())}"

    def save(self, *args, **kwargs):
        if self.utilisateur.role != Utilisateur.Role.AGENT:
            self.utilisateur.role = Utilisateur.Role.AGENT
            self.utilisateur.save()
        super().save(*args, **kwargs)




class Specialite(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.nom

class Enseignant(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'role': 'ENSEIGNANT'}
    )
    specialites = models.ManyToManyField(Specialite, blank=True)
    autres_specialites = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.utilisateur}"

class Etudiant(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'role': 'ETUDIANT'}
    )

    def __str__(self):
        return str(self.utilisateur)

    @property
    def classe_actuelle(self):
        inscription = self.inscriptions.order_by('-annee_academique').first()
        return inscription.classe if inscription else None

class Parent(models.Model):
    utilisateur = models.OneToOneField(
        Utilisateur,
        on_delete=models.CASCADE,
        primary_key=True,
        limit_choices_to={'role': 'PARENT'}
    )
    enfants = models.ManyToManyField(Etudiant, related_name='parent')


# Permissions_Manager/models.py


class RolePermission(models.Model):
    print("\nInitialisation de RolePermission...")

    # Configuration temporaire des rôles
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('AGENT', 'Agent administratif'),
        ('ENSEIGNANT', 'Enseignant'),
        ('ETUDIANT', 'Étudiant'),
        ('PARENT', 'Parent')
    ]

    ROLE_PERMISSIONS_CONFIG = {
        'ADMIN': {
            '*': ['add', 'change', 'delete', 'view']
        },
        'AGENT': {
            'formation': ['add', 'change', 'view'],
            'classe': ['add', 'change', 'view'],
            'utilisateur': ['view']
        },
        'ENSEIGNANT': {
            'cours': ['add', 'change', 'delete', 'view'],
            'evaluation': ['view', 'change'],
            'emploidutemps': ['view']
        },
        'ETUDIANT': {
            'notes': ['view'],
            'emploidutemps': ['view']
        },
        'PARENT': {
            'notes': ['view']
        }
    }

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        unique=True,
        verbose_name="Rôle système"
    )
    permissions = models.ManyToManyField(Permission, blank=True)
    groupe = models.OneToOneField(Group, on_delete=models.CASCADE, null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_maj = models.DateTimeField(auto_now=True)

    GROUP_NAMES = {
        'ADMIN': 'Groupe des administrateurs',
        'AGENT': 'Groupe des agents administratifs',
        'ENSEIGNANT': 'Groupe des enseignants',
        'ETUDIANT': 'Groupe des étudiants',
        'PARENT': 'Groupe des parents',
    }

    def __str__(self):
        return f"Permissions pour {self.get_role_display()}"

    def save(self, *args, **kwargs):
        print(f"\nDébut save() RolePermission - rôle: {self.role}")

        if not self.groupe:
            print("Création du groupe...")
            group_name = self.GROUP_NAMES.get(self.role, f"Groupe_{self.role}")
            groupe, created = Group.objects.get_or_create(name=group_name)
            self.groupe = groupe
            print(f"Groupe {'créé' if created else 'existant'}: {groupe.name}")

        super().save(*args, **kwargs)
        print("Mise à jour des permissions...")
        self.update_permissions()
        print("RolePermission sauvegardé avec succès\n")

    def update_permissions(self):
        print(f"\nupdate_permissions() pour {self.role}")
        permissions = self._get_configured_permissions()
        print(f"Permissions à appliquer ({len(permissions)}):")
        for p in permissions:
            print(f"- {p.codename}")

        if self.groupe:
            print(f"Mise à jour du groupe {self.groupe.name}")
            self.groupe.permissions.set(permissions)

        print("Mise à jour des permissions directes")
        self.permissions.set(permissions)

    @classmethod
    def init_permissions(cls):
        print("\nInitialisation globale des permissions par rôle...\n")
        for role, label in cls.ROLE_CHOICES:
            try:
                rp = cls.objects.get(role=role)
                print(f"✅ RolePermission déjà existant pour le rôle : {role}")
            except cls.DoesNotExist:
                print(f"🆕 Création de RolePermission pour le rôle : {role}")
                rp = cls(role=role)
                rp.save()

            # ✅ Mise à jour forcée des permissions pour le groupe
            print(f"🔄 Attribution des permissions au groupe pour le rôle : {role}")
            rp.update_permissions()

        print("\n✅ Initialisation complète des RolePermission terminée.\n")

    def _get_configured_permissions(self):
        print(f"\n_get_configured_permissions() pour {self.role}")
        permissions = []
        config = self.ROLE_PERMISSIONS_CONFIG.get(self.role, {})
        print(f"Configuration: {config}")

        for model, actions in config.items():
            if model == '*':
                print("Traitement des permissions globales (*)")
                perms = Permission.objects.filter(
                    codename__regex=r'^(%s)_[a-z]+' % '|'.join(actions)
                )
                print(f"Trouvé {perms.count()} permissions globales")
                permissions.extend(perms)
            else:
                print(f"\nTraitement du modèle {model}")
                try:
                    ct = ContentType.objects.get(model=model)
                    print(f"ContentType trouvé: {ct.app_label}.{ct.model}")

                    for action in actions:
                        perms = Permission.objects.filter(
                            content_type=ct,
                            codename__startswith=action
                        )
                        print(f"Permissions '{action}': {perms.count()} trouvées")
                        permissions.extend(perms)
                except ContentType.DoesNotExist:
                    print(f"ERREUR: ContentType inexistant pour {model}")
                    continue

        unique_perms = list(set(permissions))
        print(f"\nTotal permissions uniques: {len(unique_perms)}")
        return unique_perms