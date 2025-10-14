from django.db import models
from Utilisateur.models import Utilisateur,Etudiant
from Formation.models import BaseRoleModel,Classe,Parcours, AnneeAcademique
from django.core.exceptions import ValidationError
from decimal import Decimal, InvalidOperation


# Create your models here.
class Frais(BaseRoleModel):
    LIBELLE_CHOICES = [
        ('SCOLARITE', 'Scolarité'),
        ('INSCRIPTION', 'Inscription'),
        ('LABO', 'Laboratoire'),
        ('BIBLIOTHEQUE', 'Bibliothèque'),
        ('ASSURANCE', 'Assurance'),
        ('AUTRE', 'Autre'),
    ]

    libelle = models.CharField(max_length=20, choices=LIBELLE_CHOICES)
    montant = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Montant en FCFA (utiliser un point comme séparateur décimal)"
    )
    classe = models.ForeignKey(
        Classe,
        on_delete=models.CASCADE,
        null=False,  # obligatoire
        blank=False,  # obligatoire dans les formulaires
        related_name='frais'
    )

    description = models.TextField(blank=True, null=True)

    recurrent = models.BooleanField(default=False)

    def clean(self):
        from django.core.exceptions import ValidationError

        # Validation du montant
        if isinstance(self.montant, str):
            try:
                self.montant = Decimal(self.montant.replace(',', '.'))
            except (ValueError, InvalidOperation):
                raise ValidationError("Veuillez entrer un montant valide (ex: 15000.50)")

    def save(self, *args, **kwargs):
        self.full_clean()  # Force la validation avant sauvegarde
        super().save(*args, **kwargs)

    def get_montant_display(self):
        """Méthode pour afficher correctement le montant"""
        try:
            return f"{Decimal(self.montant):.2f} FCFA"
        except (TypeError, InvalidOperation):
            return "0.00 FCFA"

    def __str__(self):
        return f"{self.get_libelle_display()} - {self.get_montant_display()}"


class Paiement(BaseRoleModel):
    class MethodePaiement(models.TextChoices):
        CB = 'CB', 'Carte Bancaire'
        ESPECES = 'ES', 'Espèces'
        MOBILE_MONEY = 'MM', 'Mobile Money (Orange Money, Moov Money , Telecel Money)'
        CHEQUE = 'CH', 'Chèque'
        PAYPAL = 'PP', 'PayPal'

    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='paiements')
    frais = models.ForeignKey(Frais, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    methode = models.CharField(max_length=2, choices=MethodePaiement.choices)
    reference = models.CharField(max_length=50, unique=True, blank=True)
    date_paiement = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.reference:
            # Génère une valeur unique, exemple : "AUTO-<UUID>"
            self.reference = f"AUTO-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

class Document(models.Model):
    class TypeDocument(models.TextChoices):
        COURS = 'CO', 'Support de cours'
        DEVOIR = 'DE', 'Devoir'
        ANNONCE = 'AN', 'Annonce'
        INSCRIPTION= 'IN', 'Inscription'

    titre = models.CharField(max_length=200)
    fichier = models.FileField(upload_to='documents/')
    type = models.CharField(max_length=2, choices=TypeDocument.choices)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_upload = models.DateTimeField(auto_now_add=True)

class Devoir(Document):
    date_rendu = models.DateTimeField()
    est_rendu = models.BooleanField(default=False)

class Notification(models.Model):
    class TypeNotification(models.TextChoices):
        EMAIL = 'EM', 'Email'
        SMS = 'SM', 'SMS'
        PUSH = 'PU', 'Notification push'

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='notifications')
    contenu = models.TextField()
    type = models.CharField(max_length=2, choices=TypeNotification.choices)
    date_envoi = models.DateTimeField(auto_now_add=True)
    est_lu = models.BooleanField(default=False)


class DocumentInscription(models.Model):
    TYPE_CHOICES = [
        ('formulaire', "Formulaire d'inscription"),
        ('naissance', "Acte de naissance"),
        ('cni', "Carte nationale d'identité / Certificat d'identification"),
        ('parent_identite', "Identité des parents ou tuteurs"),
        ('bulletin', "Dernier bulletin de notes / Relevé"),
        ('diplome', "Diplôme ou attestation du niveau"),
        ('certificat_scolarite', "Certificat de scolarité"),
        ('motivation_cv', "Lettre de motivation ou CV"),
        ('frais', "Quittance de paiement / reçu"),
    ]

    inscription = models.ForeignKey(
        'Inscription',
        on_delete=models.CASCADE,
        related_name='documents_inscription'
    )
    type_document = models.CharField(max_length=50, choices=TYPE_CHOICES)
    fichier = models.FileField(upload_to='documents_inscription/')
    date_depot = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_document_display()} - {self.inscription.etudiant}"


class Inscription(BaseRoleModel):
    STATUT_INSCRIT = 'inscrit'
    STATUT_REINSCRIT = 'reinscrit'
    STATUT_ABANDON = 'abandon'
    STATUT_SUSPENDU = 'suspendu'
    STATUT_EXCLU = 'exclu'
    STATUT_EN_ATTENTE = 'en_attente'
    STATUT_TRANSFERT = 'transfert'
    STATUT_DIPLOME = 'diplome'
    STATUT_REDUIRE = 'redoublant'
    STATUT_RESERVISTE = 'reserviste'

    STATUT_CHOICES = [
        (STATUT_INSCRIT, 'Inscrit'),
        (STATUT_REINSCRIT, 'Réinscrit'),
        (STATUT_ABANDON, 'Abandon'),
        (STATUT_SUSPENDU, 'Suspendu'),
        (STATUT_EXCLU, 'Exclu'),
        (STATUT_EN_ATTENTE, 'En attente de validation'),
        (STATUT_TRANSFERT, 'Transféré'),
        (STATUT_DIPLOME, 'Diplômé'),
        (STATUT_REDUIRE, 'Redoublant'),
        (STATUT_RESERVISTE, 'Réserviste'),
    ]

    etudiant = models.ForeignKey(
        Etudiant,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="inscriptions"
    )

    parcours = models.ForeignKey(
        Parcours,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="inscriptions"
    )

    motif = models.TextField(blank=True, null=True)
    Etablissement_accuiel = models.CharField(max_length=100, blank=True, null=True)

    annee_academique = models.ForeignKey(
        AnneeAcademique,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="inscriptions"
    )

    classe = models.ForeignKey(
        Classe,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="inscriptions"
    )

    date_inscription = models.DateField(auto_now_add=True)
    date_evenement = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Date et heure de l'événement"
    )

    duree = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Durée en jours (ex: suspension)"
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default=STATUT_INSCRIT,
        help_text="Sélectionnez le statut de l'étudiant"
    )

    resultat_annee_precedente = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.etudiant} → {self.classe} ({self.annee_academique})"

    @property
    def type_formation(self):
        """Déduit le type de formation du parcours"""
        return self.parcours.type_formation

    def clean(self):
        super().clean()

        # Autres contraintes métier selon le statut
        if self.statut == self.STATUT_INSCRIT:
            if self.classe.parcours != self.parcours:
                raise ValidationError("⚠️ La classe sélectionnée ne correspond pas au parcours.")
            if self.classe.annee_academique != self.annee_academique:
                raise ValidationError("⚠️ La classe sélectionnée ne correspond pas à l’année académique.")
            if Inscription.objects.exclude(pk=self.pk).filter(
                    etudiant=self.etudiant,
                    annee_academique=self.annee_academique
            ).exists():
                raise ValidationError("⚠️ Cet étudiant est déjà inscrit pour cette année académique.")

        elif self.statut in [self.STATUT_REINSCRIT, self.STATUT_REDUIRE, self.STATUT_DIPLOME]:
            if not self.resultat_annee_precedente:
                raise ValidationError("⚠️ Le résultat de l'année précédente est requis.")

        elif self.statut in [self.STATUT_ABANDON, self.STATUT_EXCLU]:
            if not self.motif:
                raise ValidationError("⚠️ Le motif est requis.")
            print("La date de l’événement :",self.date_evenement)
            if not self.date_evenement:
                raise ValidationError("⚠️ La date de l’événement est requis.")

        elif self.statut == self.STATUT_SUSPENDU:
            if not self.motif or not self.date_evenement or not self.duree:
                raise ValidationError("⚠️ Le motif, la date et la durée sont requis pour une suspension.")

        elif self.statut == self.STATUT_TRANSFERT:
            if not self.Etablissement_accuiel or not self.motif or not self.date_evenement:
                raise ValidationError("⚠️ Tous les champs de transfert doivent être renseignés.")

