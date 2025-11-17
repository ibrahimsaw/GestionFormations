from django.db import models
from django.utils import timezone
from Utilisateur.models import Etudiant, Enseignant
from Formation.models import BaseRoleModel, Classe
import random
import string
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

def generate_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Matiere(models.Model):
    nom = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=20, unique=True, help_text="Ex: MAT101")
    description = models.TextField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_code()
            while Matiere.objects.filter(code=self.code).exists():
                self.code = generate_code()
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.nom}"



class MatiereClasse(models.Model):
    """Relation entre une matière et une classe, avec ses paramètres propres."""
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name="matieres_classes")
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="matieres_classes")
    coefficient = models.PositiveIntegerField(default=1)
    volume_horaire = models.PositiveIntegerField(default=0, help_text="Heures par semaine")

    class Meta:
        unique_together = ('matiere', 'classe')  # Empêche les doublons

    def __str__(self):
        return f"{self.matiere.nom} - {self.classe.nom} (Coef: {self.coefficient}, {self.volume_horaire}h)"

# class Chapitre(BaseRoleModel):
#     """ Programme ou plan de cours lié à une matière """
#     matiere = models.ForeignKey(MatiereClasse, on_delete=models.CASCADE, related_name="chapitres")
#     titre = models.CharField(max_length=200)
#     objectifs = models.TextField(blank=True, null=True)

#     def __str__(self):
#         return f"{self.titre} - {self.matiere.nom}"


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

    matiereclasse = models.ForeignKey(MatiereClasse, on_delete=models.CASCADE, related_name="evaluations",default=1)
    titre = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=TYPE_EVAL, default="DEVOIR")
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.titre} -{self.type} {self.matiere} ({self.classe})"


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

class Enseignement(models.Model):
    enseignant = models.ForeignKey('Utilisateur.Enseignant', on_delete=models.CASCADE, related_name='enseignements')
    matiere_classe = models.ForeignKey(MatiereClasse, on_delete=models.CASCADE, related_name='enseignements')
    annee_academique = models.CharField(max_length=9, default="2025-2026")

    class Meta:
        unique_together = ('enseignant', 'matiere_classe', 'annee_academique')

    def __str__(self):
        return f"{self.enseignant} → {self.matiere_classe.matiere.nom} ({self.matiere_classe.classe.nom})"

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

    enseignement = models.ForeignKey(
        Enseignement,
        on_delete=models.CASCADE,
        related_name="cours",
        null=True, blank=True  
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
                fields=["enseignement", "date", "heure_debut", "heure_fin"],
                name="unique_classe_usage"
            ),
        ]

    def __str__(self):
        return f"{self.matiere} - {self.classe} ({self.date} {self.heure_debut}-{self.heure_fin})"