import random
import string
import uuid
from datetime import date
from unidecode import unidecode
from django.utils import timezone
from Utilisateur.models import Genre, FonctionAgent, Specialite, Utilisateur, AdminSysteme, AgentAdministration, Enseignant, Etudiant, Parent
from Formation.models import TypeFormation, Specification, Parcours, Formation, Classe, AnneeAcademique
from Finance.models import Inscription

# 1. Initialisation des données de référence
Genre.initialiser_genres()
FonctionAgent.initialiser_fonctions()
Specification.initialiser_specifications_par_defaut()
TypeFormation.initialiser_types_par_defaut()

for nom in ["Mathématiques", "Français", "SVT", "Histoire", "Anglais", "Physique", "Philosophie", "Informatique", "Comptabilité"]:
    Specialite.objects.get_or_create(nom=nom)

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

def creer_utilisateur(role, prenom, nom, genre):
    return Utilisateur.objects.create_user(
        matricule=generer_matricule(role[:3]),
        role=role,
        first_name=nettoyer_nom(prenom),
        last_name=nettoyer_nom(nom),
        genre=genre,
        email=f"{nettoyer_nom(prenom.lower())}.{nettoyer_nom(nom.lower())}{random.randint(1,999)}@gmail.com",
        telephone=generer_telephone(),
        password="passer123"
    )

# Admins
for _ in range(2):
    prenom = random.choice(prenoms_hommes)
    nom = random.choice(noms_famille)
    user = creer_utilisateur("ADMIN", prenom, nom, genres["H"])
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
    user = creer_utilisateur("AGENT", prenom, nom, genre)
    agent = AgentAdministration.objects.create(utilisateur=user)
    agent.fonctions.add(f)
    fonction_counts[f.code] += 1
    agents.append(agent)

# 2. Compléter jusqu'à ce que chaque fonction ait au plus 3 agents
while any(c < 3 for c in fonction_counts.values()):
    prenom = random.choice(prenoms_hommes + prenoms_femmes)
    nom = random.choice(noms_famille)
    genre = genres["H"] if prenom in prenoms_hommes else genres["F"]
    user = creer_utilisateur("AGENT", prenom, nom, genre)
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
specialites = list(Specialite.objects.all())
for _ in range(5):
    prenom = random.choice(prenoms_hommes)
    nom = random.choice(noms_famille)
    user = creer_utilisateur("ENSEIGNANT", prenom, nom, genres["H"])
    enseignant = Enseignant.objects.create(utilisateur=user)
    enseignant.specialites.set(random.sample(specialites, k=random.randint(1, 2)))

# Étudiants
etudiants = []
for classe in classes:
    nb_etudiants = random.randint(15, 20)
    for _ in range(nb_etudiants):
        prenom = random.choice(prenoms_hommes + prenoms_femmes)
        nom = random.choice(noms_famille)
        genre = genres["H"] if prenom in prenoms_hommes else genres["F"]
        user = creer_utilisateur("ETUDIANT", prenom, nom, genre)
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
    user = creer_utilisateur("PARENT", prenom, nom, genre)
    parent = Parent.objects.create(utilisateur=user)
    enfants = random.sample(etudiants, k=random.choice([1, 2]))
    parent.enfants.set(enfants)
    parents.append(parent)

print("✅ Base de données remplie avec succès.")
