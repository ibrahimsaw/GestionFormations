import contextlib
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PrGestionFormation.settings")
django.setup()
import random
import string
import uuid
from datetime import date
from unidecode import unidecode
from django.utils import timezone
from Utilisateur.models import Genre, FonctionAgent, Utilisateur, AdminSysteme, AgentAdministration, Enseignant, Etudiant, Parent
from Cours.models import Matiere, MatiereClasse, Salle
from Formation.models import TypeFormation, Specification, Parcours, Formation, Classe, AnneeAcademique
from Finance.models import Inscription
from Utilisateur.models import RolePermission



# 1. Initialisation des données de référence
Genre.initialiser_genres()
RolePermission.init_permissions()
FonctionAgent.initialiser_fonctions()
Specification.initialiser_specifications_par_defaut()
TypeFormation.initialiser_types_par_defaut()

matieres = [
    {"nom": "Mathématiques", "code": "MAT101","description":"Cours de mathématiques de base"},
    {"nom": "Français", "code": "FR101","description":"Cours de langue française"},
    {"nom": "SVT", "code": "SVT101","description":"Sciences de la Vie et de la Terre"},
    {"nom": "Histoire", "code": "HIS101","description":"Cours d'histoire générale"},
    {"nom": "Anglais", "code": "ANG101","description":"Cours de langue anglaise"},
    {"nom": "Physique", "code": "PHY101","description":"Cours de physique fondamentale"},
    {"nom": "Philosophie", "code": "PHI101","description":"Introduction à la philosophie"},
    {"nom": "Informatique", "code": "INFO101","description":"Bases de l'informatique"},
    {"nom": "Comptabilité", "code": "COM101","description":"Cours de comptabilité de base"},
    {"nom": "Économie", "code": "ECO101","description":"Principes fondamentaux de l'économie"},
    {"nom": "Droit", "code": "DRO101","description":"Introduction au droit"},
    {"nom": "Gestion", "code": "GES101","description":"Principes de gestion d'entreprise"},
    {"nom": "Marketing", "code": "MAR101","description":"Bases du marketing"},
    {"nom": "Électronique", "code": "ELE101","description":"Introduction à l'électronique"},
    {"nom": "Mécanique", "code": "MEC101","description":"Principes de la mécanique"},
    {"nom": "Chimie", "code": "CHI101","description":"Cours de chimie générale"},     
    {"nom": "Biologie", "code": "BIO101","description":"Introduction à la biologie"},
    {"nom": "Géographie", "code": "GEO101","description":"Cours de géographie générale"},
    {"nom": "Arts Plastiques", "code": "ART101","description":"Introduction aux arts plastiques"},
    {"nom": "Musique", "code": "MUS101","description":"Bases de la musique"},
    {"nom": "Sport", "code": "SPO101","description":"Éducation physique et sportive"}
]

for m in matieres:
    Matiere.objects.get_or_create(
        nom=m["nom"],
        defaults={"code": m["code"], "description": m["description"]}
    )
# 2. Création des années académiques, parcours, formations et classes


annee, _ = AnneeAcademique.objects.get_or_create(
    nom="2025-2026",
    defaults={"date_debut": date(2025, 10, 1), "date_fin": date(2026, 7, 15)}
)

# 2. Création des parcours et formations
type_codes = ["LIC", "MAS", "SEC1", "SEC2", "PRO","PRIM","PR"]
specs = list(Specification.objects.all())
formations_prof = []
parcours_list = []
classes = []

for code in type_codes:
    type_formation = TypeFormation.objects.get(code=code)
    for i in range(2):  # 2 parcours par type
        spec = random.choice(specs)
        parcours, _ = Parcours.objects.get_or_create(
            nom=f"{type_formation.nom} - Parcours {i+1}",
            type_formation=type_formation,
            specification=spec,
            defaults={"structure_classes": type_formation.liste_classe, "diplome_final": "Diplôme générique"}
        )
        parcours_list.append(parcours)

        for j in range(2):  # 2 formations par parcours
            nom_formation = f"Formation {i+1}-{j+1} ({type_formation.code})"
            est_pro = (code == "PRO")
            formation, _ = Formation.objects.get_or_create(
                nom=nom_formation,
                parcours=parcours,
                defaults={"duree": 36, "est_professionnelle": est_pro, "avec_classes": True}
            )
            if est_pro:
                formations_prof.append(formation)
            formation.creer_classes(annee)
            classes += list(Classe.objects.filter(formation=formation, annee_academique=annee))

# 3. Ajout de 5 formations professionnelles spécifiques
pro_parcours, _ = Parcours.objects.get_or_create(
    nom="Parcours Professionnel Spécialisé",
    type_formation=TypeFormation.objects.get(code="PRO"),
    specification=Specification.objects.get(code="TH"),
    defaults={"structure_classes": ["1ère année", "2ème année"], "diplome_final": "CAP"}
)

pro_formations = [
    "Maintenance Informatique",
    "Comptabilité et Gestion",
    "Électricité Bâtiment",
    "Secrétariat Bureautique",
    "Agroalimentaire"
]

for nom in pro_formations:
    formation, _ = Formation.objects.get_or_create(
        nom=nom,
        parcours=pro_parcours,
        defaults={"duree": 24, "est_professionnelle": True, "avec_classes": True}
    )
    formation.creer_classes(annee)
    classes += list(Classe.objects.filter(formation=formation, annee_academique=annee))

# Création des MatiereClasse pour toutes les classes
for classe in classes:
    # Pour chaque classe, choisir un sous-ensemble aléatoire de matières
    nombre_matieres = random.randint(4, len(matieres))  # chaque classe a 4 à n matières
    matieres_selectionnees = random.sample(matieres, nombre_matieres)

    for m in matieres_selectionnees:
        matiere = Matiere.objects.get(nom=m["nom"])
        coefficient = random.randint(1, 5)  # coefficient aléatoire entre 1 et 5
        volume_horaire = random.randint(10, 200)  # volume horaire entre 10 et 200 h

        MatiereClasse.objects.get_or_create(
            matiere=matiere,
            classe=classe,
            defaults={
                "coefficient": coefficient,
                "volume_horaire": volume_horaire
            }
        )

salles = [
    {"nom": "Salle A1", "type": "COURS", "capacite": 30, "projecteur": True},
    {"nom": "Salle A2", "type": "COURS", "capacite": 25, "projecteur": False},
    {"nom": "Salle B1", "type": "INFO", "capacite": 20, "ordinateurs": True},
    {"nom": "Salle B2", "type": "LABO", "capacite": 15, "projecteur": True},
    {"nom": "Amphi 1", "type": "AMPHI", "capacite": 100, "projecteur": True},
]

for s in salles:
    Salle.objects.get_or_create(
        nom=s["nom"],
        defaults={
            "type": s.get("type", "COURS"),
            "capacite": s.get("capacite", 20),
            "projecteur": s.get("projecteur", False),
            "climatisation": s.get("climatisation", False),
            "ordinateurs": s.get("ordinateurs", False),
            "tableau_blanc": s.get("tableau_blanc", True),
        }
    )

# 4. Génération des utilisateurs
prenoms_hommes = ["Adama", "Issa", "Salif", "Boureima", "Oumar", "Daouda", "Abdoul", "Ibrahim", "Souleymane"]
prenoms_femmes = ["Awa", "Mariam", "Aminata", "Fatoumata", "Rasmata", "Safiatou", "Rokiatou", "Alima", "Kadidia"]
noms_famille = ["Sawadogo", "Ouédraogo", "Zongo", "Kaboré", "Sanou", "Diallo", "Traoré", "Konaté", "Ilboudo", "Tapsoba"]
genres = { "H": Genre.objects.get(code="H"), "F": Genre.objects.get(code="F") }

def nettoyer_nom(nom):
    return unidecode(nom)

def generer_matricule(prefix):
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"

def generer_telephone():
    return random.choice(["01","02","03","04","05","06","07","08","09","25","50","51","52","53","54","55","56","57","58","59"]) + ''.join(random.choices(string.digits, k=6))

def generer_date_aleatoire_6mois():
    """Retourne une datetime aware aléatoire comprise entre maintenant et 6 mois en arrière."""
    import datetime as _dt
    now = timezone.now()
    six_months_ago = now - _dt.timedelta(days=180)
    # durée en secondes
    total_seconds = int((now - six_months_ago).total_seconds())
    rand_seconds = random.randint(0, max(0, total_seconds))
    rand_dt = six_months_ago + _dt.timedelta(seconds=rand_seconds)
    # s'assurer que la datetime est timezone-aware
    with contextlib.suppress(Exception):
        if timezone.is_naive(rand_dt):
            rand_dt = timezone.make_aware(rand_dt)
    return rand_dt

def creer_utilisateur(role, prenom, nom, genre, date_inscription=None):
    # On crée l'utilisateur puis on met à jour date_inscription si fourni.
    # Ceci évite de modifier la définition du modèle (auto_now_add=True).
    user = Utilisateur.objects.create_user(
        matricule=generer_matricule(role[:3]),
        role=role,
        first_name=nettoyer_nom(prenom),
        last_name=nettoyer_nom(nom),
        genre=genre,
        email=f"{nettoyer_nom(prenom.lower())}.{nettoyer_nom(nom.lower())}{random.randint(1,999)}@gmail.com",
        telephone=generer_telephone(),
        password="passer123"
    )
    # Si une date d'inscription est fournie, la convertir en datetime aware
    if date_inscription:
        import datetime as _dt
        dt = date_inscription
        if isinstance(date_inscription, _dt.date) and not isinstance(date_inscription, _dt.datetime):
            dt = _dt.datetime.combine(date_inscription, _dt.time.min)
        # Rendre la datetime timezone-aware si nécessaire
        with contextlib.suppress(Exception):
            if timezone.is_naive(dt):
                dt = timezone.make_aware(dt)
        user.date_inscription = dt
        user.save(update_fields=['date_inscription'])

    return user

# Admins
for _ in range(5):
    prenom = random.choice(prenoms_hommes)
    nom = random.choice(noms_famille)
    user = creer_utilisateur("ADMIN", prenom, nom, genres["H"], date_inscription=generer_date_aleatoire_6mois())
    AdminSysteme.objects.get_or_create(utilisateur=user)

# Agents
fonctions = list(FonctionAgent.objects.all())
fonction_counts = {f.code: 0 for f in fonctions}
agents = []

# 1. Créer d'abord 1 agent pour chaque fonction (garantit au moins 1 utilisateur par fonction)
for f in fonctions:
    prenom = random.choice(prenoms_hommes + prenoms_femmes)
    nom = random.choice(noms_famille)
    genre = genres["H"] if prenom in prenoms_hommes else genres["F"]
    user = creer_utilisateur("AGENT", prenom, nom, genre, date_inscription=generer_date_aleatoire_6mois())
    agent = AgentAdministration.objects.create(utilisateur=user)
    agent.fonctions.add(f)
    fonction_counts[f.code] += 1
    agents.append(agent)

# 2. Compléter jusqu'à ce que chaque fonction ait au plus 3 agents
while any(c < 3 for c in fonction_counts.values()):
    prenom = random.choice(prenoms_hommes + prenoms_femmes)
    nom = random.choice(noms_famille)
    genre = genres["H"] if prenom in prenoms_hommes else genres["F"]
    user = creer_utilisateur("AGENT", prenom, nom, genre, date_inscription=generer_date_aleatoire_6mois())
    agent = AgentAdministration.objects.create(utilisateur=user)
    # Sélectionner 1 à plusieurs fonctions qui n'ont pas encore 3 agents
    fonctions_dispo = [f for f in fonctions if fonction_counts[f.code] < 3]
    nb_fonctions = random.randint(1, min(3, len(fonctions_dispo)))
    assign = random.sample(fonctions_dispo, k=nb_fonctions)
    for f in assign:
        agent.fonctions.add(f)
        fonction_counts[f.code] += 1
    agents.append(agent)

# Enseignants
specialites = list(Matiere.objects.all())
for _ in range(10):
    prenom = random.choice(prenoms_hommes)
    nom = random.choice(noms_famille)
    user = creer_utilisateur("ENSEIGNANT", prenom, nom, genres["H"], date_inscription=generer_date_aleatoire_6mois())
    enseignant = Enseignant.objects.create(utilisateur=user)
    enseignant.matieres.set(random.sample(specialites, k=random.randint(1, 2)))

# Étudiants
etudiants = []
for classe in classes:
    nb_etudiants = random.randint(15, 20)
    for _ in range(nb_etudiants):
        prenom = random.choice(prenoms_hommes + prenoms_femmes)
        nom = random.choice(noms_famille)
        genre = genres["H"] if prenom in prenoms_hommes else genres["F"]
        user = creer_utilisateur("ETUDIANT", prenom, nom, genre, date_inscription=generer_date_aleatoire_6mois())
        etudiant = Etudiant.objects.create(utilisateur=user)
        Inscription.objects.create(
            etudiant=etudiant,
            parcours=classe.formation.parcours,
            classe=classe,
            annee_academique=annee,
            statut=Inscription.STATUT_INSCRIT
        )
        etudiants.append(etudiant)

# Parents avec logique avancée
parents = []

def choisir_nombre_enfants():
    return random.choices(
        population=[1, 2, 3, 4, 5],
        weights=[10, 15, 30, 35, 10],
        k=1
    )[0]

etudiants_disponibles = etudiants.copy()
random.shuffle(etudiants_disponibles)

while etudiants_disponibles:
    nb_enfants = choisir_nombre_enfants()
    enfants = [etudiants_disponibles.pop() for _ in range(min(nb_enfants, len(etudiants_disponibles)))]

    nom_enfant = enfants[0].utilisateur.last_name
    nom_parent = nom_enfant if random.random() < 0.8 else random.choice(noms_famille)

    prenom = random.choice(prenoms_hommes + prenoms_femmes)
    genre = genres["H"] if prenom in prenoms_hommes else genres["F"]
    user = creer_utilisateur("PARENT", prenom, nom, genre, date_inscription=generer_date_aleatoire_6mois())
    parent = Parent.objects.create(utilisateur=user)
    enfants = random.sample(etudiants, k=random.choice([1, 2]))
    parent.enfants.set(enfants)
    parents.append(parent)

print("✅ Base de données remplie avec succès.")
