<div align="center">

# Système de Gestion des Examens — UMBB

**Planification automatique des examens, gestion des salles, des surveillants et des étudiants**

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)

</div>

---

## À propos

Application web développée avec **Streamlit** et connectée à une base **PostgreSQL**. Elle permet à une faculté de planifier ses sessions d'examens : un générateur construit automatiquement le planning en respectant des contraintes (salles, surveillants, jours de repos), puis le planning est validé par la direction avant d'être consulté par les enseignants et les étudiants.

## Fonctionnalités

| Module | Description |
|---|---|
| **Authentification** | Connexion par nom d'utilisateur et mot de passe (haché en SHA-256), accès limité selon le rôle |
| **Tableau de bord** | Statistiques et graphiques (Plotly) sur les examens, les salles et les inscriptions |
| **Génération du planning** | Création automatique de l'emploi du temps des examens sous contraintes |
| **Validation** | Validation du planning par le Vice-doyen ou le Doyen, avec détail avant et après validation |
| **Vue stratégique** | Indicateurs de synthèse réservés à la direction |
| **Gestion des données** | Départements, spécialités, formations, modules, étudiants, professeurs et salles |
| **Plannings personnels** | Consultation du planning par chaque professeur et chaque étudiant |

### Rôles

| Rôle | Accès principal |
|---|---|
| `Admin_examens` | Génération du planning et gestion des données |
| `Chef_departement` | Suivi de son département |
| `Professeur` | Consultation de ses surveillances |
| `Etudiant` | Consultation de son planning d'examens |
| `Vice-doyen` / `Doyen` | Validation du planning et vue stratégique |

### Contraintes du générateur

- Aucun examen le jour de repos (vendredi)
- Une seule spécialité par jour et un jour libre entre deux examens d'une même spécialité
- Choix de la plus petite salle dont la capacité suffit pour les inscrits
- Nombre de surveillants selon l'effectif : 1 jusqu'à 30 étudiants, 2 de 31 à 40, 3 au-delà
- Un professeur surveille au maximum 3 examens par jour
- Détection et signalement des conflits lorsqu'aucune solution n'est possible

## Technologies

| | |
|---|---|
| **Langage** | Python 3 |
| **Interface** | Streamlit |
| **Base de données** | PostgreSQL (accès via `psycopg2`) |
| **Données et graphiques** | pandas, Plotly |
| **Images** | Pillow |

## Base de données

Le script `schema.sql` crée les tables `departements`, `formations`, `roles`, `utilisateurs`, `professeurs`, `etudiants`, `modules`, `lieu_examen`, `inscriptions`, `examens`, `connexions_log` et `examens_historique`. Il définit aussi des déclencheurs (calcul de l'heure de fin, mise à jour du nombre d'inscrits, journal des connexions), une fonction de permissions et une vue de statistiques globales.

| Fichier | Rôle |
|---|---|
| `schema.sql` | Création des tables, déclencheurs et vue |
| `bda.sql` | Jeu de données de test : 7 départements, salles, professeurs, formations, modules, 13 000 étudiants et inscriptions |
| `admin.sql` / `remplire.sql` | Comptes utilisateurs de démonstration |
| `indexes.sql` | Index d'optimisation (syntaxe SQL Server, à adapter pour PostgreSQL) |

## Installation

### Prérequis
- Python 3.10 ou plus récent
- Un serveur PostgreSQL (local ou hébergé, par exemple Neon)

### Étapes

1. **Cloner le dépôt**
   ```bash
   git clone https://github.com/siamsell/exam_sheduler.git
   cd exam_sheduler
   ```
2. **Installer les dépendances**
   ```bash
   pip install streamlit pandas psycopg2-binary plotly pillow requests
   ```
3. **Créer la base de données** PostgreSQL, puis exécuter `schema.sql`.
4. **Charger les données** de test avec `bda.sql`, puis créer les comptes avec `admin.sql`.
5. **Configurer la connexion** : renseigner vos propres paramètres (hôte, base, utilisateur, mot de passe, port) dans le dictionnaire `db_config` de `app.py`. Ne publiez jamais vos identifiants réels sur GitHub.
6. **Lancer l'application**
   ```bash
   streamlit run app.py
   ```
