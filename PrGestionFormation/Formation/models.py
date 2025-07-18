from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from simple_history.models import HistoricalRecords

class BaseRoleModel(models.Model):
    """Classe de base pour les modèles liés à un utilisateur."""
    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True

    def save_with_user(self, user, *args, **kwargs):
        self.save(*args, **kwargs)
        last_history = self.history.first()
        if last_history and user:
            last_history.history_user = user
            last_history.save()

# Modèle TypeFormation
class TypeFormation(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    liste_classe = models.JSONField(default=list, blank=True)  # ✅ Nouveau champ

    class Meta:
        verbose_name = "Type de formation"
        verbose_name_plural = "Types de formation"
        ordering = ['nom']

    def __str__(self):
        return self.nom

    @classmethod
    def initialiser_types_par_defaut(cls):
        types_par_defaut = [
            {"code": "PR", "nom": "Préscolaire", "liste_classe": ['PS', 'MS', 'GS']},
            {"code": "PRIM", "nom": "Primaire", "liste_classe": ['CP1', 'CP2', 'CE1', 'CE2', 'CM1', 'CM2']},
            {"code": "SEC1", "nom": "Secondaire 1er cycle", "liste_classe": ['6e', '5e', '4e','3e']},
            {"code": "SEC2", "nom": "Secondaire 2nd cycle", "liste_classe": ['2nde', '1ère', 'Tle']},
            {"code": "PRO", "nom": "Professionnel", "liste_classe": []},
            {"code": "LIC", "nom": "Licence", "liste_classe": ['L1', 'L2', 'L3']},  # ✅ Ajout Licence
            {"code": "MAS", "nom": "Master", "liste_classe": ['M1', 'M2']},
        ]

        for type_data in types_par_defaut:
            cls.objects.get_or_create(
                code=type_data["code"],
                defaults={
                    "nom": type_data["nom"],
                    "liste_classe": type_data["liste_classe"],
                }
            )

# Modèle Specification
class Specification(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Spécification"
        verbose_name_plural = "Spécifications"
        ordering = ['nom']

    def __str__(self):
        return f"{self.code} - {self.nom}"

    @classmethod
    def initialiser_specifications_par_defaut(cls):
        specs_par_defaut = [
            {"code": "GN", "nom": "Générale"},
            {"code": "TH", "nom": "Technique"},
            {"code": "FO", "nom": "Formation"},
            {"code": "UN", "nom": "Université"},
        ]

        for spec in specs_par_defaut:
            cls.objects.get_or_create(code=spec["code"], defaults={"nom": spec["nom"]})

# Modèle Parcours corrigé avec ForeignKey
class Parcours(BaseRoleModel):
    type_formation = models.ForeignKey(TypeFormation, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.SET_NULL, null=True, blank=True)
    nom = models.CharField(max_length=100)
    code_serie = models.CharField(max_length=3, blank=True, null=True)
    structure_classes = models.JSONField(
        blank=True,
        default=list,
        help_text="Liste JSON des classes — automatiquement héritée du type de formation"
    )

    diplome_final = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Ex: BAC A, BEPC, CAP"
    )

    class Meta:
        verbose_name_plural = "Parcours"
        ordering = ['type_formation', 'nom']

    def __str__(self):
        return f"{self.type_formation.nom} - {self.nom}"

    def save(self, *args, **kwargs):
        if not self.structure_classes:
            self.structure_classes = self.type_formation.liste_classe
        super().save(*args, **kwargs)


# Modèle Formation
class Formation(BaseRoleModel):
    parcours = models.ForeignKey(
        Parcours,
        on_delete=models.CASCADE,
        related_name='formations'
    )
    nom = models.CharField(max_length=100)
    duree = models.IntegerField(
        null=True,  # Autorise les valeurs null en base
        blank=True,  # Autorise les champs vides dans les formulaires
        help_text="Durée en mois/années selon le type"
    )
    est_professionnelle = models.BooleanField(default=False)
    avec_classes = models.BooleanField(
        default=True,
        help_text="Cocher pour créer automatiquement les classes"
    )

    class Meta:
        ordering = ['parcours__type_formation__nom', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.parcours})"

    def creer_classes_auto(self):
        """Crée automatiquement les classes si configuré"""
        if not self.avec_classes:
            return

        annee_active = AnneeAcademique.objects.filter(classes_standards_creees=True).first()
        if annee_active:
            self.creer_classes(annee_active)

    def creer_classes(self, annee_academique):
        """Implémentation concrète de création des classes"""
        if self.est_professionnelle:
            Classe.objects.get_or_create(
                nom=f"{self.nom}",
                formation=self,
                annee_academique=annee_academique,
                defaults={'ordre': 1}
            )
        else:
            for ordre, nom_classe in enumerate(self.parcours.structure_classes, start=1):
                Classe.objects.get_or_create(
                    nom=nom_classe,
                    formation=self,
                    annee_academique=annee_academique,
                    defaults={'ordre': ordre}
                )

# Signal pour la création automatique des classes à la création d'une formation
@receiver(post_save, sender=Formation)
def formation_post_save(sender, instance, created, **kwargs):
    if created and instance.avec_classes:
        instance.creer_classes_auto()

# Modèle Classe (manquant dans l'original)
class Classe(BaseRoleModel):
    nom = models.CharField(max_length=100)
    ordre = models.IntegerField()
    formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name='classes')
    annee_academique = models.ForeignKey('AnneeAcademique', on_delete=models.CASCADE)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"{self.nom} ({self.annee_academique.nom})"

# Modèle AnneeAcademique
class AnneeAcademique(BaseRoleModel):
    nom = models.CharField(
        max_length=20,
        unique=True,
        default="2023-2024"  # Valeur par défaut essentielle
    )
    date_debut = models.DateField()
    date_fin = models.DateField()
    classes_standards_creees = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_debut']
        verbose_name = "Année Académique"
        verbose_name_plural = "Années Académiques"

    def __str__(self):
        return self.nom

    def creer_classes_standards(self):
        """Crée les classes pour toutes les formations standards"""
        if self.classes_standards_creees:
            return

        formations = Formation.objects.filter(avec_classes=True, est_professionnelle=False)
        for formation in formations:
            formation.creer_classes(self)

        self.classes_standards_creees = True
        self.save()

# Signal pour créer les classes standards automatiquement à la création d'une année académique
@receiver(post_save, sender=AnneeAcademique)
def creer_classes_auto(sender, instance, created, **kwargs):
    if created:
        instance.creer_classes_standards()
