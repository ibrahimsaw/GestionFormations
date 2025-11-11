from django.db import models
from django.utils import timezone
from Utilisateur.models import Etudiant, Enseignant
from Formation.models import BaseRoleModel, Classe

# Create your models here.

class Salle(BaseRoleModel):
    TYPE_SALLE = [
        ("COURS", "Salle de cours"),
        ("INFO", "Salle informatique"),
        ("LABO", "Laboratoire"),
        ("AMPHI", "Amphithéâtre"),
        ("REUNION", "Salle de réunion"),
        ("AUTRE", "Autre"),
    ]

    nom = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_SALLE, default="COURS")
    capacite = models.PositiveIntegerField(default=20)

    batiment = models.CharField(max_length=100, blank=True, null=True)  # Ex: Bloc B, Bâtiment Sciences
    etage = models.PositiveIntegerField(blank=True, null=True)  # 0 = rez-de-chaussée

    # Equipements
    projecteur = models.BooleanField(default=False)
    climatisation = models.BooleanField(default=False)
    ordinateurs = models.BooleanField(default=False)
    tableau_blanc = models.BooleanField(default=True)

    est_actif = models.BooleanField(default=True)  # Salle utilisable ou non

    def __str__(self):
        return f"{self.nom} ({self.get_type_display()})"


class Matiere(BaseRoleModel):
    nom = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True, help_text="Ex: MAT101")
    coefficient = models.PositiveIntegerField(default=1)
    volume_horaire = models.PositiveIntegerField(default=0, help_text="Heures par semaine")

    # Une matière peut être enseignée dans plusieurs classes
    classes = models.ManyToManyField(Classe, related_name="matieres")

    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.nom} ({self.code})"


class Chapitre(BaseRoleModel):
    """ Programme ou plan de cours lié à une matière """
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="chapitres")
    titre = models.CharField(max_length=200)
    objectifs = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.titre} - {self.matiere.nom}"


class Evaluation(BaseRoleModel):
    """ Examens / Devoirs / Compositions """
    TYPE_EVAL = [
        ("DEVOIR", "Devoir"),
        ("DS", "Devoir Surveillé"),
        ("COMPO", "Composition"),
        ("EXAMEN", "Examen"),
        ("ORAL", "Oral"),
        ("TP", "Travaux Pratiques"),
    ]

    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="evaluations")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="evaluations")
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_EVAL, default="DEVOIR")
    date = models.DateField(default=timezone.now)
    coefficient = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.titre} - {self.matiere} ({self.classe})"


class Note(BaseRoleModel):
    """ Notes des élèves par matière & évaluation """
    evaluation = models.ForeignKey(Evaluation, on_delete=models.CASCADE, related_name="notes")
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name="notes")
    
    note = models.FloatField()
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ("evaluation", "etudiant")  # empêche double saisie

    def __str__(self):
        return f"{self.etudiant} - {self.evaluation} : {self.note}"

class Cours(BaseRoleModel):
    TYPE_COURS = [
        ("COURS", "Cours"),
        ("TP", "Travaux Pratiques"),
        ("TD", "Travaux Dirigés"),
        ("EXAMEN", "Examen"),
        ("COMPO", "Composition"),
        ("PROJET", "Projet"),
        ("AUTRE", "Autre"),
    ]

    # La matière (ex: Math, Physique, Histoire)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="cours")

    # La classe concernée (ex: 4ème A)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="cours")

    # L’enseignant
    enseignant = models.ForeignKey(Enseignant, 
        limit_choices_to={'role': 'ENSEIGNANT'},
        on_delete=models.SET_NULL, null=True, related_name="cours"
    )

    # La salle utilisée
    salle = models.ForeignKey(Salle, on_delete=models.SET_NULL, null=True, related_name="cours")

    # Horaire
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()

    # Type (cours ou examen ou projet etc.)
    type_cours = models.CharField(max_length=20, choices=TYPE_COURS, default="COURS")

    # Informations supplémentaires
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["date", "heure_debut"]
        # Empêcher la collision d’horaires pour une même salle
        constraints = [
            models.UniqueConstraint(
                fields=["salle", "date", "heure_debut", "heure_fin"],
                name="unique_salle_usage"
            ),
            models.UniqueConstraint(
                fields=["classe", "date", "heure_debut", "heure_fin"],
                name="unique_classe_usage"
            ),
        ]

    def __str__(self):
        return f"{self.matiere} - {self.classe} ({self.date} {self.heure_debut}-{self.heure_fin})"
