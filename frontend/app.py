import streamlit as st
import pandas as pd
import psycopg2
from datetime import datetime, timedelta, time
import time as time_module
import hashlib
import base64
import traceback
from typing import List, Dict, Tuple, Optional, Set
import random
from collections import defaultdict, Counter
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px
import pandas as pd

from psycopg2 import errors

# =============================================
# CONFIGURATION
# =============================================

st.set_page_config(
    page_title="UMBB - Système de Gestion des Examens",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.markdown("""
    <style>
   
div[data-testid="stAppViewBlockContainer"] {
    z-index: 9999 !important;
}

/* Améliorer l'affichage en plein écran */
.fullScreenFrame {
    background: white !important;
    padding: 20px !important;
    border-radius: 12px !important;
}

/* Bouton plein écran plus visible */
.stDataFrame [data-testid="stFullScreenFrame"] button {
    background: rgba(79, 70, 229, 0.1) !important;
    border: 1px solid rgba(79, 70, 229, 0.3) !important;
    border-radius: 6px !important;
    color: #4f46e5 !important;
}

.stDataFrame [data-testid="stFullScreenFrame"] button:hover {
    background: rgba(79, 70, 229, 0.2) !important;
    border-color: #4f46e5 !important;
}
/* Cibler les 4 colonnes spécifiquement */
div[data-testid="column"]:nth-of-type(1):has(.stAlert),
div[data-testid="column"]:nth-of-type(2):has(.stAlert),
div[data-testid="column"]:nth-of-type(3):has(.stAlert),
div[data-testid="column"]:nth-of-type(4):has(.stAlert) {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(5px) !important;
    border-radius: 20px !important;
    padding: 25px 15px !important;
    margin: 10px 5px !important;
    border: 1px solid rgba(123, 36, 37, 0.2) !important;
}

/* Style commun pour toutes les alertes dans les stats */
div.stAlert[data-testid="stAlert"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    margin: 0 !important;
    text-align: center !important;
}

/* Chiffres en grand */
div.stAlert[data-testid="stAlert"] > div:first-child {
    font-size: 3rem !important;
    font-weight: 900 !important;
    color: black !important;
   
   
    margin-bottom: 15px !important;
}

/* Labels */
div.stAlert[data-testid="stAlert"] > div:nth-child(2) {
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    color:black!important;
    text-transform: uppercase !important;
    letter-spacing: 1px !important;
    margin-top: 10px !important;
}
.custom-add-professor-btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
    margin-top: 20px !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
}

.custom-add-professor-btn:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    background: linear-gradient(135deg, #5a6fd8 0%, #6a3a92 100%) !important;
}

.custom-add-professor-btn:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.3) !important;
}

/* Couleurs spécifiques */
div.stSuccess[data-testid="stAlert"] > div:first-child {
    background: linear-gradient(135deg, #10b981 2%, #047857 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

div.stWarning[data-testid="stAlert"] > div:first-child {
    background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

div.stError[data-testid="stAlert"] > div:first-child {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

div.stInfo[data-testid="stAlert"] > div:first-child {
    background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}
    /* Supprimer tout fond blanc par défaut */
    section.main, .stApp > div, .block-container,
    .st-emotion-cache-1wrcr25,
    .st-emotion-cache-uf99v8,
    .st-emotion-cache-1v0mbdj {
       backdrop-filter: blur(5px);
        background: rgba(255,255,255,0.1);
    }
    
    
    /* ============================================
       EN-TÊTE PRINCIPAL POUR TOUTES LES PAGES
       ============================================ */
    .main-header {
        border-radius: 16px;
        padding: 32px;
        ackdrop-filter: blur(5px);
        background: rgba(255,255,255,0.1);
        margin-bottom: 32px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        text-align: center;
    }
    
    .main-header h1 {
        color:white;
        font-weight: 700;
        font-size: 2.2rem;
        margin-bottom: 8px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        color: black;
        font-size: 1.1rem;
        margin-top: 0;
    }
    
    /* ============================================
       SIDEBAR STYLE (AMÉLIORÉ)
       ============================================ */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a237e 0%, #283593 100%);
        border-right: none;
        min-width: 280px;
    }
    
    .sidebar-logo-container {
        text-align: center;
        padding: 24px 20px;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
    }
    
    .logo-badge {
        width: 48px;
        height: 48px;
        border-radius: 12px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        font-size: 20px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .logo-text h3 {
        color: white;
        font-size: 1.4rem;
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        line-height: 1.2;
    }
    
    .logo-text p {
        color: rgba(255,255,255,0.7);
        font-size: 0.8rem;
        margin: 2px 0 0 0;
        line-height: 1.2;
    }
    
    .user-info {
        background: rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 16px;
        margin: 0 16px 24px 16px;
        text-align: center;
        backdrop-filter: blur(10px);
    }
    
    .user-name {
        color: white;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 4px;
    }
    
    .role-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        background: rgba(255,255,255,0.15);
        color: white;
    }
   
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    .kpi-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
        text-align: center;
        height: 100%;
    }
    
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border-color: #c7d2fe;
    }
    
    .kpi-title {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .kpi-value {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* ============================================
       BOUTONS
       ============================================ */
      section[data-testid="stSidebar"] .stButton button {
        background: transparent;
        border: 1px solid rgba(255,255,255,0.2);
        color: white;
        border-radius: 10px;
        padding: 12px 20px;
        width: 100%;
        text-align: left;
        font-weight: 500;
        transition: all 0.3s ease;
        margin: 4px 0;
    }
    
    
    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.1);
        border-color: rgba(255,255,255,0.3);
        transform: translateX(5px);
    }
    
    section[data-testid="stSidebar"] .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        font-weight: 600;
    }
    .stButton button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        font-weight: 600;
    }

       
.stButton button[kind="secondary"] {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}

.stButton button[type="secondary"] {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
    padding: 12px 24px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}
.stButton button[type="secondary"]:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}
.stButton button[kind="secondary"]:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

/* Style spécifique pour les boutons Envoyer */
.submit-button {
    width: 100% !important;
    margin: 10px 0 !important;
    padding: 14px !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}

.submit-button-primary {
    background: linear-gradient(135deg, #10b981 0%, #047857 100%) !important;
}

.submit-button-warning {
    background: linear-gradient(135deg, #f59e0b 0%, #b45309 100%) !important;
}

.submit-button-danger {
    background: linear-gradient(135deg, #ef4444 0%, #b91c1c 100%) !important;
}
     ============================================
       FORMULAIRES
       ============================================ */
    .stForm {
        background: white;
        border-radius: 16px;
        padding: 30px;
        
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* ============================================
       TABLEAUX
       ============================================ */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* ============================================
       ALERTES ET MESSAGES
       ============================================ */
    .alert-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
    }
    
    .success-card {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
    }
    
    .error-card {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
    }
    
    .info-card {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        border-left: 4px solid #3b82f6;
        padding: 16px;
        border-radius: 12px;
        margin: 8px 0;
    }
    
    /* ============================================
       ONGLETS
       ============================================ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        font-weight: 500;
    }
    
    /* ============================================
       EXPANDERS
       ============================================ */
    .streamlit-expanderHeader {
        font-weight: 600;
        border-radius: 12px;
    }
    
    /* ============================================
       CONFLIT CARDS
       ============================================ */
    .conflict-card {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
        padding: 16px;
        border-radius: 12px;
        margin: 12px 0;
        border: 1px solid rgba(245, 158, 11, 0.2);
    }
    
    /* ============================================
       FILTER CARDS
       ============================================ */
    .filter-card {
        background: white;
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
    }
    
    /* ============================================
       CONTRAINTES
       ============================================ */

            
    .constraint-item {
        background: #f8fafc;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 8px 0;
        border-left: 3px solid #4f46e5;
        font-size: 0.95rem;
    }
    
    .holiday-item {
        display: inline-block;
        background: #fee2e2;
        color: #dc2626;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 2px;
    }
    
    /* ============================================
       FOOTER
       ============================================ */
    .footer {
        text-align: center;
        font-size: 0.85rem;
        color: black; 
        margin-top: 48px;
        padding-top: 24px;
        border-top: 1px solid #e2e8f0;
    }
    
    
    /* ============================================
       CACHER LES ÉLÉMENTS STREAMLIT PAR DÉFAUT
       ============================================ */
    .stDeployButton, .stToolbar, #MainMenu {
        display: none !important;
    }
    
    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        .main-header {
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .main-header h1 {
            font-size: 1.8rem;
        }
        
        .kpi-value {
            font-size: 2rem;
        }
    }
    
    /* ============================================
       ANIMATIONS
       ============================================ */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-out;
    }
    
    /* ============================================
       SCROLLBAR PERSONNALISÉE
       ============================================ */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    </style>
""", unsafe_allow_html=True)
# =============================================
# CONNEXION BASE DE DONNÉES
# =============================================

db_config = {
    "host": "ep-twilight-lab-admqcbxg-pooler.c-2.us-east-1.aws.neon.tech",
    "dbname": "neondb",
    "user": "neondb_owner",
    "password": "npg_sTYKH8WLnDv2",
    "port": 5432,
    "sslmode": "require",
    "client_encoding": "UTF8" 
}

def get_db():
    """Établit une connexion à la base de données"""
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        st.error(f"Erreur de connexion à la base de données: {str(e)}")
        return None
    
def execute_query(query, params=None, fetch=True):
    """Exécute une requête SQL"""
    conn = get_db()
    if conn is None:
        return None
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, params)
            
            if fetch and query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cur.description]
                data = cur.fetchall()
                df = pd.DataFrame(data, columns=columns)
                return df
            else:
                conn.commit()
                return True
                
    except Exception as e:
        st.error(f"❌ Erreur SQL: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()
# \def get_db():
   # """Établit une connexion à la base de données"""
   # try:
       # conn = psycopg2.connect(
          #  dbname="ssbda",
            #user="postgres",
            #password="admin123", 
            #host="localhost",
            #port="5433"
       # )
        # return conn# 
   #except Exception as e:
        # st.error(f"Erreur de connexion à la base de données: {str(e)}")
       # return None

# =============================================
# CLASSES DE CONFIGURATION ET GÉNÉRATION
# =============================================

class ConfigContraintes:
    """Configuration des contraintes de génération optimisée"""
    
    def __init__(self):
        # Jours de travail : Samedi (5) à Jeudi (3)
        self.jours_travail = [5, 6, 0, 1, 2, 3]
        self.jour_repos = 4  # Vendredi
        
        # Horaires par niveau (1h30 d'examen)
        self.horaires_niveaux = {
            'L1': {'debut': time(8, 0), 'fin': time(9, 30), 'duree': 90},
            'L2': {'debut': time(9, 40), 'fin': time(11, 10), 'duree': 90},
            'L3': {'debut': time(11, 20), 'fin': time(12, 50), 'duree': 90},
            'M1': {'debut': time(14, 0), 'fin': time(15, 30), 'duree': 90},
            'M2': {'debut': time(15, 40), 'fin': time(17, 10), 'duree': 90}
        }
        
        # Jours fériés
        annee_courante = datetime.now().year
        self.jours_feries = [
            datetime(annee_courante, 1, 1).date(),
            datetime(annee_courante, 1, 12).date(),
            datetime(annee_courante, 5, 1).date(),
            datetime(annee_courante, 7, 5).date(),
            datetime(annee_courante, 7, 8).date(),
            datetime(annee_courante, 11, 1).date(),
        ]
        
        # Règles de surveillance
        self.surveillance_regles = [
            (0, 30, 1),   # 0-30 étudiants: 1 surveillant
            (31, 40, 2),  # 31-40 étudiants: 2 surveillants
            (41, 1000, 3) # 41+ étudiants: 3 surveillants
        ]
        
        # Contraintes strictes
        self.max_surveillances_par_jour = 3  # Un prof surveille max 3 examens par jour
        self.intervalle_specialite_jours = 1  # 1 jour libre entre 2 examens même spécialité
        self.une_specialite_par_jour = True   # 1 seule spécialité par jour

class GenerateurPlanning:
    """Générateur intelligent de planning d'examens avec optimisation complète"""
    
    def __init__(self):
        self.config = ConfigContraintes()
        self.planning = []
        self.conflits = []
        self.stats = {}
        self.salles_disponibles = []
        self.professeurs_disponibles = []
        self.specialites_modules = defaultdict(list)
        self.date_debut = None
        self.date_fin = None
    
    def date_valide(self, date_test: datetime.date) -> bool:
        """Vérifie si une date respecte toutes les contraintes"""
        # Vérifier jour de repos (Vendredi)
        if date_test.weekday() == self.config.jour_repos:
            return False
        
        # Vérifier jour férié
        if date_test in self.config.jours_feries:
            return False
        
        # Vérifier que c'est un jour de travail
        if date_test.weekday() not in self.config.jours_travail:
            return False
        
        return True
    
    def get_horaire_niveau(self, annee_etude: str) -> Dict:
        """Retourne l'horaire approprié pour un niveau donné"""
        niveau_map = {"1": 'L1', "2": 'L2', "3": 'L3', "4": 'M1', "5": 'M2'}
        niveau = niveau_map.get(str(annee_etude), 'L1')
        
        if niveau not in self.config.horaires_niveaux:
            return self.config.horaires_niveaux['L1']
        
        return self.config.horaires_niveaux[niveau]
    
    def calculer_nb_surveillants(self, nb_etudiants: int) -> int:
        """Calcule le nombre de surveillants nécessaires"""
        for min_etud, max_etud, nb_surv in self.config.surveillance_regles:
            if min_etud <= nb_etudiants <= max_etud:
                return nb_surv
        return 2
    
    def trouver_salle_disponible(self, date_exam: datetime.date, heure_debut: time, 
                                heure_fin: time, nb_etudiants: int, salle_exclue_id: int = None) -> Optional[int]:
        """Trouve une salle disponible pour un créneau donné"""
        if not self.salles_disponibles:
            return None
        
        # Trier les salles par capacité (la plus petite suffisante en premier)
        salles_triees = sorted(self.salles_disponibles, key=lambda x: x['capacite'])
        
        for salle in salles_triees:
            if salle_exclue_id and salle['id'] == salle_exclue_id:
                continue
            
            # Vérifier capacité suffisante
            if salle['capacite'] < nb_etudiants:
                continue
            
            # Vérifier si la salle est déjà occupée à ce créneau
            salle_occupee = False
            for exam in self.planning:
                if (exam['salle_id'] == salle['id'] and 
                    exam['date_exam'] == date_exam):
                    
                    # Vérifier chevauchement des horaires
                    if not (heure_fin <= exam['heure_debut'] or heure_debut >= exam['heure_fin']):
                        salle_occupee = True
                        break
            
            if not salle_occupee:
                return salle['id']
        
        return None
    
    def trouver_surveillants(self, date_exam: datetime.date, heure_debut: time, 
                            heure_fin: time, nb_surveillants: int) -> List[int]:
        """Trouve des surveillants disponibles pour un créneau donné"""
        if not self.professeurs_disponibles:
            return []
        
        surveillants_trouves = []
        
        # Trier les professeurs par nombre de surveillances (pour équilibrage)
        profs_tries = sorted(self.professeurs_disponibles, 
                           key=lambda x: len([e for e in self.planning 
                                            if x['id'] in e.get('surveillants_ids', [])]))
        
        for prof in profs_tries:
            if len(surveillants_trouves) >= nb_surveillants:
                break
            
            prof_id = prof['id']
            
            # Compter combien d'examens ce professeur surveille déjà ce jour
            nb_surveillances_jour = 0
            for exam in self.planning:
                if (exam['date_exam'] == date_exam and 
                    prof_id in exam.get('surveillants_ids', [])):
                    nb_surveillances_jour += 1
            
            # Vérifier la limite max par jour
            if nb_surveillances_jour >= self.config.max_surveillances_par_jour:
                continue
            
            # Vérifier disponibilité horaire
            disponible = True
            for exam in self.planning:
                if (exam['date_exam'] == date_exam and 
                    prof_id in exam.get('surveillants_ids', [])):
                    
                    # Vérifier chevauchement des horaires
                    if not (heure_fin <= exam['heure_debut'] or heure_debut >= exam['heure_fin']):
                        disponible = False
                        break
            
            if disponible:
                surveillants_trouves.append(prof_id)
        
        return surveillants_trouves if len(surveillants_trouves) == nb_surveillants else []
    
    def specialite_peut_avoir_examen(self, date_test: datetime.date, specialite_id: int) -> bool:
        """Vérifie si une spécialité peut avoir un examen à une date donnée"""
        if not self.config.une_specialite_par_jour:
            return True
        
        # Vérifier s'il y a déjà un examen de cette spécialité ce jour
        for exam in self.planning:
            if (exam['date_exam'] == date_test and 
                exam['specialite_id'] == specialite_id):
                return False
        
        # Vérifier intervalle minimum entre examens de même spécialité
        for exam in self.planning:
            if exam['specialite_id'] == specialite_id:
                jours_ecart = abs((date_test - exam['date_exam']).days)
                if jours_ecart < self.config.intervalle_specialite_jours:
                    return False
        
        return True
    
    def generer_planning_filtre(self, conn, date_debut: datetime.date, date_fin: datetime.date, 
                                user_id: int, specialite_id=None, annee_etude=None, semestre=None):
        """Génère un planning avec filtres et optimisation complète"""
        try:
            self.planning = []
            self.conflits = []
            self.stats = {}
            self.date_debut = date_debut
            self.date_fin = date_fin
            
            cursor = conn.cursor()
            
            # 1. Récupérer les modules avec filtres
            query = """
                SELECT m.id, m.code_module, m.nom, m.credits, m.specialite_id, 
                       m.annee_etude, m.semestre, m.prof_responsable_id,
                       s.nom as specialite_nom,
                       COUNT(DISTINCT i.etudiant_id) as nb_inscrits
                FROM modules m
                LEFT JOIN specialites s ON m.specialite_id = s.id
                LEFT JOIN inscriptions i ON m.id = i.module_id
                WHERE 1=1
            """
            params = []
            
            if specialite_id:
                query += " AND m.specialite_id = %s"
                params.append(str(specialite_id))
            
            if annee_etude:
                query += " AND m.annee_etude = %s"
                params.append(str(annee_etude))
            
            if semestre:
                query += " AND m.semestre = %s"
                params.append(str(semestre))
            
            query += " GROUP BY m.id, m.code_module, m.nom, m.credits, m.specialite_id, "
            query += "          m.annee_etude, m.semestre, m.prof_responsable_id, s.nom"
            query += " ORDER BY m.specialite_id, m.annee_etude, m.semestre"
            
            cursor.execute(query, params)
            modules = cursor.fetchall()
            
            if not modules:
                self.conflits.append({
                    'type': 'pas_de_donnees',
                    'message': "Aucun module trouvé avec les critères spécifiés"
                })
                return [], self.conflits
            
            # 2. Récupérer les salles disponibles
            cursor.execute("""
                SELECT id, nom, capacite, type, batiment 
                FROM lieu_examen 
                WHERE disponible_examen = true 
                ORDER BY capacite DESC
            """)
            salles_db = cursor.fetchall()
            
            if not salles_db:
                self.conflits.append({
                    'type': 'pas_de_salles',
                    'message': "Aucune salle disponible"
                })
                return [], self.conflits
            
            self.salles_disponibles = [
                {'id': sid, 'nom': nom, 'capacite': cap, 'type': typ, 'batiment': bat}
                for sid, nom, cap, typ, bat in salles_db
            ]
            
            # 3. Récupérer les professeurs surveillants
            cursor.execute("""
                SELECT id, nom, prenom, est_surveillant
                FROM professeurs 
                WHERE est_surveillant = true
                ORDER BY nom, prenom
            """)
            profs_db = cursor.fetchall()
            
            if not profs_db:
                self.conflits.append({
                    'type': 'pas_de_professeurs',
                    'message': "Aucun professeur surveillant disponible"
                })
                return [], self.conflits
            
            self.professeurs_disponibles = [
                {'id': pid, 'nom': nom, 'prenom': prenom, 'est_surveillant': est_surv}
                for pid, nom, prenom, est_surv in profs_db
            ]
            
            # 4. Organiser les modules par spécialité
            self.specialites_modules = defaultdict(list)
            for module in modules:
                (module_id, code_module, nom_module, credits, specialite_id_module, 
                 annee_etude_module, semestre_module, prof_responsable_id,
                 specialite_nom, nb_inscrits) = module
                
                nb_inscrits = nb_inscrits or 0
                
                self.specialites_modules[specialite_id_module].append({
                    'id': module_id,
                    'code': code_module,
                    'nom': nom_module,
                    'specialite_id': specialite_id_module,
                    'specialite_nom': specialite_nom,
                    'annee_etude': annee_etude_module,
                    'semestre': semestre_module,
                    'prof_responsable_id': prof_responsable_id,
                    'nb_inscrits': nb_inscrits
                })
            
            # 5. Planifier les examens avec optimisation
            jours_total = (date_fin - date_debut).days + 1
            date_courante = date_debut
            modules_planifies = 0
            
            # Parcourir les jours disponibles
            for jour_num in range(jours_total):
                if modules_planifies >= len(modules):
                    break
                
                if not self.date_valide(date_courante):
                    date_courante += timedelta(days=1)
                    continue
                
                # Pour chaque spécialité, planifier au plus un examen par jour
                specialites_planifiees_aujourdhui = set()
                
                for specialite_id, modules_specialite in self.specialites_modules.items():
                    if modules_planifies >= len(modules):
                        break
                    
                    # Vérifier si cette spécialité peut avoir un examen aujourd'hui
                    if not self.specialite_peut_avoir_examen(date_courante, specialite_id):
                        continue
                    
                    # Prendre le premier module non planifié de cette spécialité
                    for module in modules_specialite:
                        if any(exam['module_id'] == module['id'] for exam in self.planning):
                            continue
                        
                        # Déterminer l'horaire selon le niveau
                        horaire = self.get_horaire_niveau(module['annee_etude'])
                        heure_debut = horaire['debut']
                        heure_fin = horaire['fin']
                        
                        # Calculer nombre de surveillants nécessaires
                        nb_surveillants = self.calculer_nb_surveillants(module['nb_inscrits'])
                        
                        # Trouver une salle disponible
                        salle_id = self.trouver_salle_disponible(
                            date_courante, heure_debut, heure_fin, module['nb_inscrits']
                        )
                        
                        if not salle_id:
                            self.conflits.append({
                                'type': 'pas_de_salle_disponible',
                                'message': f"Aucune salle disponible pour {module['nom']} le {date_courante}",
                                'module': module['nom'],
                                'date': date_courante.strftime('%d/%m/%Y')
                            })
                            continue
                        
                        # Trouver des surveillants disponibles
                        surveillants_ids = self.trouver_surveillants(
                            date_courante, heure_debut, heure_fin, nb_surveillants
                        )
                        
                        if len(surveillants_ids) < nb_surveillants:
                            self.conflits.append({
                                'type': 'pas_de_surveillants',
                                'message': f"Pas assez de surveillants pour {module['nom']}",
                                'module': module['nom'],
                                'date': date_courante.strftime('%d/%m/%Y'),
                                'requis': nb_surveillants,
                                'trouves': len(surveillants_ids)
                            })
                            continue
                        
                        # Créer l'examen
                        examen = {
                            'module_id': module['id'],
                            'module_code': module['code'],
                            'module_nom': module['nom'],
                            'specialite_id': module['specialite_id'],
                            'specialite_nom': module['specialite_nom'],
                            'annee_etude': module['annee_etude'],
                            'semestre': module['semestre'],
                            'prof_responsable_id': module['prof_responsable_id'],
                            'date_exam': date_courante,
                            'heure_debut': heure_debut,
                            'heure_fin': heure_fin,
                            'salle_id': salle_id,
                            'nb_inscrits': module['nb_inscrits'],
                            'nb_surveillants': nb_surveillants,
                            'surveillants_ids': surveillants_ids,
                            'duree_minutes': horaire['duree'],
                            'created_by': user_id,
                            'created_at': datetime.now()
                        }
                        
                        self.planning.append(examen)
                        specialites_planifiees_aujourdhui.add(specialite_id)
                        modules_planifies += 1
                        break
                
                date_courante += timedelta(days=1)
            
            # 6. Calculer les statistiques
            self.calculer_statistiques()
            
            return self.planning, self.conflits
            
        except Exception as e:
            self.conflits.append({
                'type': 'erreur_generation',
                'message': f"Erreur lors de la génération: {str(e)}"
            })
            return [], self.conflits
    
    def calculer_statistiques(self):
        """Calcule les statistiques du planning généré"""
        if not self.planning:
            return
        
        self.stats = {
            'total_examens': len(self.planning),
            'total_etudiants': sum(e['nb_inscrits'] for e in self.planning),
            'total_surveillants': sum(e['nb_surveillants'] for e in self.planning),
            'jours_utilises': len(set(e['date_exam'] for e in self.planning)),
            'salles_utilisees': len(set(e['salle_id'] for e in self.planning)),
            'specialites_utilisees': len(set(e['specialite_id'] for e in self.planning)),
        }
        
        # Calculer taux d'occupation des salles
        occupation_salles = {}
        for exam in self.planning:
            salle_id = exam['salle_id']
            if salle_id not in occupation_salles:
                # Trouver capacité de la salle
                salle_info = next((s for s in self.salles_disponibles if s['id'] == salle_id), None)
                occupation_salles[salle_id] = {
                    'nom': salle_info['nom'] if salle_info else f"Salle {salle_id}",
                    'capacite': salle_info['capacite'] if salle_info else 0,
                    'etudiants': 0,
                    'examens': 0
                }
            occupation_salles[salle_id]['etudiants'] += exam['nb_inscrits']
            occupation_salles[salle_id]['examens'] += 1
        
        # Calculer les pourcentages
        for salle_id, info in occupation_salles.items():
            if info['capacite'] > 0:
                taux_occupation = (info['etudiants'] / (info['capacite'] * info['examens'])) * 100
                info['taux_occupation'] = min(100, taux_occupation)
            else:
                info['taux_occupation'] = 0
        
        self.stats['occupation_salles'] = occupation_salles
    
    def afficher_tableau_planning(self, conn) -> pd.DataFrame:
        """Affiche le planning dans un tableau DataFrame stylé"""
        if not self.planning:
            return None
        
        try:
            cursor = conn.cursor()
            table_data = []
            
            for exam in sorted(self.planning, key=lambda x: (x['date_exam'], x['heure_debut'])):
                # Récupérer les détails de la salle
                salle_nom = "N/A"
                batiment = "N/A"
                capacite = 0
                
                salle_info = next((s for s in self.salles_disponibles if s['id'] == exam['salle_id']), None)
                if salle_info:
                    salle_nom = salle_info['nom']
                    batiment = salle_info['batiment'] or "N/A"
                    capacite = salle_info['capacite']
                
                # Récupérer les noms des surveillants
                surveillants_noms = []
                for prof_id in exam['surveillants_ids']:
                    cursor.execute("SELECT nom, prenom FROM professeurs WHERE id = %s", (prof_id,))
                    prof = cursor.fetchone()
                    if prof:
                        surveillants_noms.append(f"{prof[1]} {prof[0]}")
                
                # Récupérer le nom du professeur responsable
                prof_principal_nom = "N/A"
                if exam['prof_responsable_id']:
                    cursor.execute("SELECT nom, prenom FROM professeurs WHERE id = %s", (exam['prof_responsable_id'],))
                    prof = cursor.fetchone()
                    if prof:
                        prof_principal_nom = f"{prof[1]} {prof[0]}"
                
                # Formatage des dates et heures
                date_str = exam['date_exam'].strftime('%d/%m/%Y')
                jour_str = exam['date_exam'].strftime('%A')
                heure_debut_str = exam['heure_debut'].strftime('%H:%M')
                heure_fin_str = exam['heure_fin'].strftime('%H:%M')
                heure_str = f"{heure_debut_str} - {heure_fin_str}"
                
                # Niveau formaté
                niveau_map = {"1": 'L1', "2": 'L2', "3": 'L3', "4": 'M1', "5": 'M2'}
                niveau = niveau_map.get(str(exam['annee_etude']), f"N{exam['annee_etude']}")
                
                table_data.append({
                    'ID': len(table_data) + 1,
                    'Date': date_str,
                    'Jour': jour_str,
                    'Heure': heure_str,
                    'Module': f"{exam['module_code']} - {exam['module_nom']}",
                    'Spécialité': exam['specialite_nom'],
                    'Niveau': niveau,
                    'Salle': salle_nom,
                    'Bâtiment': batiment,
                    'Capacité': capacite,
                    'Étudiants': exam['nb_inscrits'],
                    'Surveillants': ", ".join(surveillants_noms),
                    'Nb Sur.': exam['nb_surveillants'],
                    'Prof. Principal': prof_principal_nom,
                    'Durée': f"{exam['duree_minutes']} min",
                    'Semestre': exam['semestre'],
                    'Année Étude': exam['annee_etude']
                })
            
            if table_data:
                df = pd.DataFrame(table_data)
                return df
            
        except Exception as e:
            st.error(f"Erreur création tableau: {str(e)}")
        
        return None
    
    def afficher_statistiques(self):
        """Affiche les statistiques du planning"""
        if not self.stats:
            return
        
        st.markdown("### Statistiques du Planning")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("Examens", self.stats['total_examens'])
        with col2:
            st.metric("Étudiants", self.stats['total_etudiants'])
        with col3:
            st.metric("Surveillants", self.stats['total_surveillants'])
        with col4:
            st.metric("Jours utilisés", self.stats['jours_utilises'])
        with col5:
            st.metric("Salles utilisées", self.stats['salles_utilisees'])
        
        # Taux d'occupation moyen
        if 'occupation_salles' in self.stats:
            taux_moyen = sum(s['taux_occupation'] for s in self.stats['occupation_salles'].values()) / len(self.stats['occupation_salles'])
            st.metric("Occupation moyenne", f"{taux_moyen:.1f}%")
    
    def afficher_conflits(self):
        """Affiche les conflits détectés"""
        if not self.conflits:
            st.success("✅ Aucun conflit détecté!")
            return
        
        st.error(f"### ⚠️ Conflits détectés ({len(self.conflits)})")
        
        for conflit in self.conflits:
            st.markdown(f"""
            <div class="conflict-card">
                <strong>{conflit.get('type', 'Conflit').upper()}</strong><br>
                <strong>Problème:</strong> {conflit.get('message', 'N/A')}<br>
                {f"<strong>Module:</strong> {conflit.get('module', 'N/A')}<br>" if 'module' in conflit else ""}
                {f"<strong>Date:</strong> {conflit.get('date', 'N/A')}<br>" if 'date' in conflit else ""}
                {f"<strong>Surveillants requis/trouvés:</strong> {conflit.get('requis', 'N/A')}/{conflit.get('trouves', 'N/A')}" if 'requis' in conflit else ""}
            </div>
            """, unsafe_allow_html=True)
    
    def sauvegarder_planning(self, conn, nom_planning: str, user_id: int):
        """Sauvegarde le planning dans la base de données"""
        try:
            cursor = conn.cursor()
            
            # Insérer chaque examen
            for exam in self.planning:
                cursor.execute("""
                    INSERT INTO planning_automatique 
                    (nom_planning, module_id, date_exam, heure_debut, heure_fin,
                     salle_id, nb_inscrits, nb_surveillants, surveillants_ids,
                     created_by, created_at, statut)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    nom_planning,
                    exam['module_id'],
                    exam['date_exam'],
                    exam['heure_debut'],
                    exam['heure_fin'],
                    exam['salle_id'],
                    exam['nb_inscrits'],
                    exam['nb_surveillants'],
                    exam['surveillants_ids'],
                    user_id,
                    datetime.now(),
                    'en_attente'
                ))
            
            conn.commit()
            return True, f"Planning '{nom_planning}' sauvegardé avec succès! ({len(self.planning)} examens)"
            
        except Exception as e:
            conn.rollback()
            return False, f"Erreur sauvegarde: {str(e)}"
    
    def exporter_csv(self, conn) -> str:
        """Exporte le planning en format CSV"""
        try:
            df = self.afficher_tableau_planning(conn)
            if df is not None:
                return df.to_csv(index=False, encoding='utf-8-sig')
        except Exception as e:
            st.error(f"Erreur export CSV: {str(e)}")
        return ""

# =============================================
# FONCTIONS D'AUTHENTIFICATION 
# =============================================

def verify_password_simple(stored_hash, password):
    """Vérifie un mot de passe"""
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return stored_hash == hashed_password

def authenticate_user(username, password):
    """Authentifie un utilisateur"""
    conn = get_db()
    if not conn:
        return None, "Erreur de connexion"
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT u.id, u.username, u.password_hash, u.est_actif, r.nom as role_nom
            FROM utilisateurs u
            JOIN roles r ON u.role_id = r.id
            WHERE u.username = %s
        """, (username,))
        
        user_data = cursor.fetchone()
        
        if not user_data:
            return None, "Utilisateur non trouvé"
        
        user_id, username, password_hash, est_actif, role_nom = user_data
        
        if not est_actif:
            return None, "Compte désactivé"
        
        if not verify_password_simple(password_hash, password):
            return None, "Mot de passe incorrect"
        
        user_info = {
            'id': user_id,
            'username': username,
            'role': role_nom
        }
        
        # Si c'est un étudiant ou professeur, récupérer l'ID correspondant
        if role_nom == 'Etudiant':
            cursor.execute("SELECT id FROM etudiants WHERE utilisateur_id = %s", (user_id,))
            etudiant_data = cursor.fetchone()
            if etudiant_data:
                user_info['etudiant_id'] = etudiant_data[0]
        
        elif role_nom == 'Professeur':
            cursor.execute("SELECT id FROM professeurs WHERE utilisateur_id = %s", (user_id,))
            professeur_data = cursor.fetchone()
            if professeur_data:
                user_info['id_prof'] = professeur_data[0]
        
        return user_info, "Authentification réussie"
        
    except Exception as e:
        return None, f"Erreur: {str(e)}"
    finally:
        conn.close()



# =============================================
#  STYLES MODERNES – ANIMATIONS + GLASSMORPHISM
st.markdown("""
<style>
/* ===== RESET ===== */
html, body {
    height: 100%;
    margin: 0;
    
    
    color:black;
    padding: 0;
    background: transparent !important;
}

section.main {
    position: fixed;
    inset: 0;
    padding: 0;
     
    background: transparent !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

/* ===== FORM CONTAINER ===== */
[data-testid="stForm"] {
    background: rgba(255,255,255,0.1);
    border: none !important;
    padding: 40px !important;
    backdrop-filter: blur(5px);
    margin: 0 auto !important;
    width: 560px !important;
    height:560px;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
}

/* ===== FORM TITLE ===== */
.form-title {
    text-align: center;
    font-size: 32px;
    font-weight: 400;
    color: white;
    margin-top:25px;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    width: 100%;
    text-shadow: 0 2px 4px rgba(0,0,0,0.5);
}

/* ===== CHANGER COULEUR DES TITRES EMAIL ET PASSWORD ===== */




/* ===== INPUT FIELDS ===== */
[data-testid="stTextInput"] input {
    width: 100% !important;
    padding: 14px 16px !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 4px !important;
    color: #333 !important;
    font-size: 19px !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    box-sizing: border-box !important;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}

[data-testid="stTextInput"] input::placeholder {
    font-size: 10px !important;
    color: #333 !important;
}

[data-testid="stTextInput"] input:focus {
    outline: none !important;
    color: #333 !important;
    border-color: rgba(255, 255, 255, 0.6) !important;
    background: rgba(255, 255, 255, 0.15) !important;
    box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.1) !important;
}

/* ===== CHECKBOX ===== */
[data-testid="stCheckbox"] label {
    color: white !important;
    font-size: 16px !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ===== LOGIN BUTTON ===== */
[data-testid="stFormSubmitButton"] button {
    width: 100% !important;
    padding: 14px !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 4px !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 500 !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
    backdrop-filter: blur(5px);
    -webkit-backdrop-filter: blur(5px);
}

[data-testid="stFormSubmitButton"] button:hover {
    background: rgba(255, 255, 255, 0.25) !important;
    border-color: rgba(255, 255, 255, 0.5) !important;
}


/* ===== LOGIN ICON ===== */
.login-icon {
    text-align: center;
}

.login-icon svg {
    width: 60px;
    height: 60px;
    fill: white;
    filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));
}

.login-icon i {
    font-size: 50px;
    margin-top: 50px;
    color: white;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

/* ===== ALERTS ===== */
[data-testid="stAlert"] {
    background: rgba(0, 0, 0, 0.6) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
}
.custom-label {
    color: rgb(135, 106, 54) !important;  /* Rouge pour Email */
    font-size: 16px !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    display: block !important;
    font-family: -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.custom-label.password {
    color: rgb(135, 106, 54) !important;  /* Turquoise pour Password */
    margin-top: 20px !important;  /* Espacement entre les champs */
}

/* ===== HIDE STREAMLIT UI ===== */
#MainMenu, footer, header {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)
# =============================================
# BACKGROUND IMAGE
# =============================================
def set_login_background(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed !important;
        background-size: cover !important;
        
    }}
    
    /* Overlay semi-transparent */
    .stApp::before {{
        content: "";
        position: fixed;
        inset: 0;
         width: 600px;
         

        background: rgba(0, 0, 0, 0.4);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)

# =============================================
# LOGIN PAGE - SIMPLE ET PROPRE
# =============================================
def login_page():
    set_login_background("login.png")
    
    # Titre
   
    with st.form("login_form"):
        st.markdown('''
    <div class="login-icon">
        <!-- Option 1: SVG simple -->
        <svg viewBox="0 0 24 24">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
        </svg>
       
    </div>
    ''', unsafe_allow_html=True)
        # Email
        st.markdown('<div class="form-title">Log In</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-form-container">', unsafe_allow_html=True)
             # Email - Titre AU-DESSUS
        st.markdown('<div class="custom-label">Email</div>', unsafe_allow_html=True)
        email = st.text_input("", placeholder="Enter your email", label_visibility="collapsed")
        
        # Password - Titre AU-DESSUS
        st.markdown('<div class="custom-label password">Password</div>', unsafe_allow_html=True)
        password = st.text_input("", type="password", placeholder="Enter your password", label_visibility="collapsed")
        
        st.markdown('<div class="links-row">', unsafe_allow_html=True)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            remember_me = st.checkbox("Remember me", value=True)
        
        
        
        # Bouton
        submit = st.form_submit_button("LOG IN")
        
        # Logique d'authentification
        if submit:
            if not email or not password:
                st.error("Please enter both email and password")
            else:
                with st.spinner("Signing in..."):
                    user_info, message = authenticate_user(email, password)
                    if user_info:
                        st.session_state['authenticated'] = True
                        st.session_state['user_info'] = user_info
                        st.success(f"Welcome back!")
                        time_module.sleep(1)
                        st.rerun()
                    else:
                        st.error(message or "Invalid credentials")
    
    
    
    st.markdown('</div>', unsafe_allow_html=True)
# =============================================
# INITIALISATION SESSION
# =============================================

if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
if 'user_info' not in st.session_state:
    st.session_state['user_info'] = None
if 'planning_generated' not in st.session_state:
    st.session_state['planning_generated'] = None
if 'planning_conflits' not in st.session_state:
    st.session_state['planning_conflits'] = []
if 'generation_params' not in st.session_state:
    st.session_state['generation_params'] = {}
if 'menu' not in st.session_state:
    st.session_state['menu'] = 'dashboard'
if 'edit_mode' not in st.session_state:
    st.session_state['edit_mode'] = {}
if 'delete_mode' not in st.session_state:
    st.session_state['delete_mode'] = {}
if 'selected_planning' not in st.session_state:
    st.session_state['selected_planning'] = None
if 'strategic_view_mode' not in st.session_state:
    st.session_state['strategic_view_mode'] = 'occupation'
if 'generateur' not in st.session_state:
    st.session_state['generateur'] = None

# =============================================
# VÉRIFICATION AUTHENTIFICATION
# =============================================

if not st.session_state['authenticated']:
    login_page()
    st.stop()

# =============================================
# PAGE GÉNÉRATION DE PLANNING AMÉLIORÉE
# =============================================
def get_plain_password(conn, username):
    """Récupère le mot de passe en clair depuis la table password_log"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT plain_password 
            FROM password_log 
            WHERE username = %s 
            ORDER BY created_at DESC 
            LIMIT 1
        """, (username,))
        result = cursor.fetchone()
        return result[0] if result else None
    except Exception as e:
        # Si la table n'existe pas ou erreur, retourner None
        return None
def get_plain_password_for_professor(conn, username):
    """Récupère le mot de passe en clair pour un professeur"""
    return get_plain_password(conn, username)  



# ============================================
# STYLES CSS SPÉCIFIQUES POUR CETTE PAGE
# ============================================

st.markdown("""
<style>
/* ============================================
   STYLES SPÉCIFIQUES GESTION ÉTUDIANTS
   ============================================ */

/* Header principal */
.etudiant-header {
    background: linear-gradient(135deg, rgba(21, 94, 117, 0.9) 0%, rgba(29, 78, 216, 0.9) 100%);
    border-radius: 20px;
    padding: 35px;
    margin-bottom: 35px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
}

.etudiant-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" fill-opacity="1" d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,144C672,139,768,181,864,186.7C960,192,1056,160,1152,144C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
    background-size: cover;
    opacity: 0.3;
}

.etudiant-header h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 15px;
    background: linear-gradient(135deg, #ffffff 0%, #dbeafe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}

.etudiant-header p {
    font-size: 1.3rem;
    opacity: 0.9;
    margin-top: 10px;
    position: relative;
    z-index: 1;
}

/* Cartes étudiant améliorées */
.etudiant-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(226, 232, 240, 0.8);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.etudiant-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    border-color: #c7d2fe;
}

.etudiant-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 20px 0 0 20px;
}

/* Badges spéciaux */
.specialite-badge {
    display: inline-block;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(59, 130, 246, 0.2);
}

.niveau-badge {
    display: inline-block;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(16, 185, 129, 0.2);
}

.promo-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(245, 158, 11, 0.2);
}

/* Boutons améliorés */
.btn-etudiant-modify {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
}

.btn-etudiant-modify:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
}

.btn-etudiant-delete {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
}

.btn-etudiant-delete:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
}

/* Formulaire amélioré */
.form-container-etudiant {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 35px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(226, 232, 240, 0.8);
}

.form-label-etudiant {
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 8px;
    display: block;
    font-size: 1rem;
}

/* Statistiques améliorées */
.stat-card-etudiant {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(226, 232, 240, 0.8);
    transition: all 0.3s ease;
}

.stat-card-etudiant:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.stat-value-etudiant {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
}

.stat-label-etudiant {
    font-size: 0.95rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Onglets améliorés */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.1);
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 15px 25px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.15);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
}

/* Zone de recherche améliorée */
.search-box-etudiant {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(226, 232, 240, 0.8);
}

/* Bouton d'action principal */
.btn-primary-etudiant {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 16px 32px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
    width: 100% !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.btn-primary-etudiant:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4) !important;
    background: linear-gradient(135deg, #0da271 0%, #047857 100%) !important;
}

/* Bouton secondaire */
.btn-secondary-etudiant {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    color: #64748b !important;
    font-weight: 600 !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.btn-secondary-etudiant:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    color: #475569 !important;
    transform: translateY(-2px) !important;
}

/* Message d'alerte amélioré */
.alert-etudiant {
    background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
    border-left: 6px solid #ef4444;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
}

/* Card info étudiant */
.info-card-etudiant {
    background: linear-gradient(135deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.9) 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(226, 232, 240, 0.8);
}

/* Animation d'entrée */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
    .etudiant-header {
        padding: 25px 20px;
    }
    
    .etudiant-header h1 {
        font-size: 2.2rem;
    }
    
    .etudiant-card {
        padding: 20px;
    }
    
    .stat-value-etudiant {
        font-size: 2.2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ==================== FONCTIONS POUR LES SPÉCIALITÉS ====================

def get_all_specialites():
    """Récupère toutes les spécialités avec leurs détails"""
    query = """
    SELECT 
        s.id,
        s.nom as specialite,
        f.nom as formation,
        n.nom as niveau,
        s.code_specialite,
        COALESCE(CONCAT(p.nom, ' ', p.prenom), 'Non spécifié') as responsable,
        s.capacite_max,
        s.description
    FROM specialites s
    JOIN formations f ON s.formation_id = f.id
    JOIN niveaux n ON s.niveau_id = n.id
    LEFT JOIN professeurs p ON s.responsable_id = p.id
    ORDER BY s.id
    """
    return execute_query(query)

def get_all_formations():
    """Récupère toutes les formations"""
    query = "SELECT id, nom, code_formation FROM formations ORDER BY nom"
    return execute_query(query)

def get_all_niveaux():
    """Récupère tous les niveaux"""
    query = "SELECT id, nom, code FROM niveaux ORDER BY ordre"
    return execute_query(query)

def get_all_professeurs():
    """Récupère tous les professeurs avec leurs départements"""
    query = """
    SELECT 
        p.id,
        p.nom,
        p.prenom,
        p.specialite,
        d.nom as departement
    FROM professeurs p
    JOIN departements d ON p.dept_id = d.id
    ORDER BY p.nom, p.prenom
    """
    return execute_query(query)

def add_specialite(nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max):
    """Ajoute une nouvelle spécialité"""
    query = """
    INSERT INTO specialites 
        (nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    if responsable_id is None:
        responsable_id = None
    
    conn = get_db()
    if conn is None:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, (nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max))
            result = cur.fetchone()
            conn.commit()
            return result is not None
    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def update_specialite(specialite_id, nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max):
    """Met à jour une spécialité"""
    query = """
    UPDATE specialites 
    SET nom = %s, 
        formation_id = %s, 
        niveau_id = %s, 
        code_specialite = %s, 
        description = %s, 
        responsable_id = %s, 
        capacite_max = %s
    WHERE id = %s
    """
    return execute_query(query, (nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max, specialite_id), fetch=False)

def delete_specialite(specialite_id):
    """Supprime une spécialité"""
    return execute_query("DELETE FROM specialites WHERE id = %s", (specialite_id,), fetch=False)

def get_specialite_by_id(specialite_id):
    """Récupère une spécialité par son ID"""
    query = """
    SELECT 
        s.id,
        s.nom,
        s.formation_id,
        s.niveau_id,
        s.code_specialite,
        s.description,
        s.responsable_id,
        s.capacite_max
    FROM specialites s
    WHERE s.id = %s
    """
    return execute_query(query, (specialite_id,))

# ==================== PAGE DE GESTION DES SPÉCIALITÉS ====================

def page_gestion_specialites():
    """Page de gestion des spécialités"""
    set_page_background('dashboard')
    st.markdown("""
    <div class="etudiant-header fade-in-up">
        <h1> Gestion des Spécialités</h1>
        <p>Ajouter, modifier et gérer les spécialités universitaires</p>
        <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
            <i class="fas fa-users" style="margin-right: 5px;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Créer 4 onglets distincts
    tab1, tab2, tab3, tab4 = st.tabs([
        " Liste des Spécialités", 
        " Ajouter Spécialité", 
        " Modifier Spécialité",
        " Supprimer Spécialité"
    ])
    
    # Onglet 1: Liste des spécialités
    with tab1:
        st.header("Liste des Spécialités")
        specialites = get_all_specialites()
        
        if specialites is not None:
            if not specialites.empty:
                # Afficher le tableau
                st.dataframe(specialites, use_container_width=True, hide_index=True)
                
                # Statistiques
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Spécialités", len(specialites))
                with col2:
                    avg_capacite = specialites['capacite_max'].mean()
                    st.metric("Capacité Moyenne", f"{avg_capacite:.0f}")
                with col3:
                    unique_niveaux = specialites['niveau'].nunique()
                    st.metric("Niveaux", unique_niveaux)
                
                # Détails par formation
                st.subheader("Répartition par Formation")
                formation_stats = specialites.groupby('formation').size().reset_index(name='count')
                formation_stats = formation_stats.sort_values('count', ascending=False)
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.dataframe(formation_stats, use_container_width=True, hide_index=True)
                with col_b:
                    st.bar_chart(formation_stats.set_index('formation')['count'])
                    
            else:
                st.info("Aucune spécialité enregistrée")
        else:
            st.error("Impossible de charger les spécialités")
    
    # Onglet 2: Ajouter une spécialité
    with tab2:
        st.header(" Ajouter une Spécialité")
        
        # Récupérer les données nécessaires
        formations = get_all_formations()
        niveaux = get_all_niveaux()
        professeurs = get_all_professeurs()
        
        if formations is not None and not formations.empty and \
           niveaux is not None and not niveaux.empty:
            
            with st.form("form_ajouter_specialite"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nom = st.text_input("Nom de la spécialité*", placeholder="Intelligence Artificielle")
                    
                    # Sélection de la formation
                    formation_options = formations['nom'].tolist()
                    formation_codes = formations['code_formation'].tolist()
                    
                    # Créer un texte descriptif pour la sélection
                    formation_display = [f"{nom} ({code})" for nom, code in zip(formation_options, formation_codes)]
                    selected_formation_idx = st.selectbox("Formation*", range(len(formation_display)), 
                                                         format_func=lambda x: formation_display[x])
                    formation_id = int(formations.iloc[selected_formation_idx]['id'])
                    
                    # Sélection du niveau
                    niveau_options = niveaux['nom'].tolist()
                    niveau_codes = niveaux['code'].tolist()
                    niveau_display = [f"{nom} ({code})" for nom, code in zip(niveau_options, niveau_codes)]
                    selected_niveau_idx = st.selectbox("Niveau*", range(len(niveau_display)),
                                                      format_func=lambda x: niveau_display[x])
                    niveau_id = int(niveaux.iloc[selected_niveau_idx]['id'])
                    
                    code_specialite = st.text_input("Code de la spécialité*", placeholder="IA-M1")
                
                with col2:
                    description = st.text_area("Description", placeholder="Description de la spécialité...", height=100)
                    
                    # Sélection du responsable
                    if professeurs is not None and not professeurs.empty:
                        # Créer les options pour le selectbox
                        prof_options = ["Non spécifié"] + [f"{row['nom']} {row['prenom']} - {row['specialite']} ({row['departement']})" 
                                                          for _, row in professeurs.iterrows()]
                        prof_ids = [None] + [int(row['id']) for _, row in professeurs.iterrows()]
                        
                        selected_prof_idx = st.selectbox(
                            "Professeur responsable", 
                            range(len(prof_options)),
                            format_func=lambda x: prof_options[x]
                        )
                        responsable_id = prof_ids[selected_prof_idx]
                        
                        # Afficher quelques statistiques sur les professeurs
                        with st.expander("Informations sur les professeurs disponibles"):
                            st.write(f"**Total de professeurs:** {len(professeurs)}")
                            st.write("**Liste des professeurs:**")
                            for _, prof in professeurs.iterrows():
                                st.write(f"- {prof['nom']} {prof['prenom']} ({prof['specialite']}) - {prof['departement']}")
                    else:
                        st.error("❌ Aucun professeur trouvé dans la base de données!")
                        st.info("Veuillez d'abord ajouter des professeurs dans la base de données.")
                        responsable_id = None
                    
                    capacite_max = st.number_input("Capacité maximale", min_value=10, max_value=500, value=50, step=10)
                
                col_sub, col_reset = st.columns(2)
                
                with col_sub:
                    submitted = st.form_submit_button("Ajouter", type="primary", use_container_width=True)
                
                with col_reset:
                    reset = st.form_submit_button("Réinitialiser", use_container_width=True)
                
                if submitted:
                    if nom and code_specialite:
                        result = add_specialite(nom, formation_id, niveau_id, code_specialite, 
                                               description, responsable_id, capacite_max)
                        if result:
                            st.success(f"✅ Spécialité '{nom}' ajoutée avec succès!")
                            st.info("La spécialité a été enregistrée dans la base de données.")
                            # Petit délai avant de recharger
                            import time
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de l'ajout de la spécialité")
                            st.info("Vérifiez que le code de spécialité n'existe pas déjà (doit être unique).")
                    else:
                        if not nom:
                            st.error("❌ Le nom de la spécialité est obligatoire")
                        if not code_specialite:
                            st.error("❌ Le code de la spécialité est obligatoire")
                
                if reset:
                    st.rerun()
        else:
            st.error("❌ Données manquantes pour créer une spécialité")
            if formations is None or formations.empty:
                st.error("Aucune formation disponible")
            if niveaux is None or niveaux.empty:
                st.error("❌ Aucun niveau disponible")
    
    # Onglet 3: Modifier une spécialité
    with tab3:
        st.header(" Modifier une Spécialité")
        
        specialites = get_all_specialites()
        formations = get_all_formations()
        niveaux = get_all_niveaux()
        professeurs = get_all_professeurs()
        
        if specialites is not None and not specialites.empty and \
           formations is not None and not formations.empty and \
           niveaux is not None and not niveaux.empty:
            
            # Sélectionner la spécialité
            specialite_options = specialites['specialite'] + " (" + specialites['formation'] + " - " + specialites['niveau'] + ")"
            selected_idx = st.selectbox(
                "Choisir une spécialité à modifier",
                range(len(specialite_options)),
                format_func=lambda x: specialite_options.iloc[x],
                key="edit_specialite_select"
            )
            
            if selected_idx is not None:
                specialite = specialites.iloc[selected_idx]
                specialite_id = int(specialite['id'])
                
                # Récupérer les détails complets de la spécialité
                specialite_details = get_specialite_by_id(specialite_id)
                
                if specialite_details is not None and not specialite_details.empty:
                    specialite_details = specialite_details.iloc[0]
                    
                    with st.form("form_modifier_specialite"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_nom = st.text_input("Nom*", value=specialite_details['nom'], key="edit_nom")
                            
                            # Sélection de la formation
                            formation_options = formations['nom'].tolist()
                            formation_codes = formations['code_formation'].tolist()
                            formation_display = [f"{nom} ({code})" for nom, code in zip(formation_options, formation_codes)]
                            
                            # Trouver l'index de la formation actuelle
                            current_formation_id = int(specialite_details['formation_id'])
                            current_formation = formations[formations['id'] == current_formation_id]
                            if not current_formation.empty:
                                current_formation_name = current_formation.iloc[0]['nom']
                                current_formation_code = current_formation.iloc[0]['code_formation']
                                current_formation_display = f"{current_formation_name} ({current_formation_code})"
                                try:
                                    default_formation_idx = formation_display.index(current_formation_display)
                                except:
                                    default_formation_idx = 0
                            else:
                                default_formation_idx = 0
                            
                            selected_formation_idx = st.selectbox(
                                "Formation*",
                                range(len(formation_display)),
                                index=default_formation_idx,
                                format_func=lambda x: formation_display[x],
                                key="edit_formation"
                            )
                            formation_id = int(formations.iloc[selected_formation_idx]['id'])
                            
                            # Sélection du niveau
                            niveau_options = niveaux['nom'].tolist()
                            niveau_codes = niveaux['code'].tolist()
                            niveau_display = [f"{nom} ({code})" for nom, code in zip(niveau_options, niveau_codes)]
                            
                            # Trouver l'index du niveau actuel
                            current_niveau_id = int(specialite_details['niveau_id'])
                            current_niveau = niveaux[niveaux['id'] == current_niveau_id]
                            if not current_niveau.empty:
                                current_niveau_name = current_niveau.iloc[0]['nom']
                                current_niveau_code = current_niveau.iloc[0]['code']
                                current_niveau_display = f"{current_niveau_name} ({current_niveau_code})"
                                try:
                                    default_niveau_idx = niveau_display.index(current_niveau_display)
                                except:
                                    default_niveau_idx = 0
                            else:
                                default_niveau_idx = 0
                            
                            selected_niveau_idx = st.selectbox(
                                "Niveau*",
                                range(len(niveau_display)),
                                index=default_niveau_idx,
                                format_func=lambda x: niveau_display[x],
                                key="edit_niveau"
                            )
                            niveau_id = int(niveaux.iloc[selected_niveau_idx]['id'])
                            
                            new_code = st.text_input("Code*", value=specialite_details['code_specialite'], key="edit_code")
                        
                        with col2:
                            new_description = st.text_area(
                                "Description", 
                                value=specialite_details['description'] if specialite_details['description'] else "",
                                height=100,
                                key="edit_description"
                            )
                            
                            # Sélection du responsable
                            if professeurs is not None and not professeurs.empty:
                                # Créer les options pour le selectbox
                                prof_options = ["Non spécifié"] + [f"{row['nom']} {row['prenom']} - {row['specialite']} ({row['departement']})" 
                                                                  for _, row in professeurs.iterrows()]
                                prof_ids = [None] + [int(row['id']) for _, row in professeurs.iterrows()]
                                
                                # Trouver l'index du responsable actuel
                                current_responsable_id = specialite_details['responsable_id']
                                default_prof_idx = 0
                                
                                if current_responsable_id:
                                    current_prof = professeurs[professeurs['id'] == current_responsable_id]
                                    if not current_prof.empty:
                                        current_prof_name = f"{current_prof.iloc[0]['nom']} {current_prof.iloc[0]['prenom']} - {current_prof.iloc[0]['specialite']} ({current_prof.iloc[0]['departement']})"
                                        try:
                                            default_prof_idx = prof_options.index(current_prof_name)
                                        except ValueError:
                                            default_prof_idx = 0
                                
                                selected_prof_idx = st.selectbox(
                                    "Professeur responsable",
                                    range(len(prof_options)),
                                    index=default_prof_idx,
                                    format_func=lambda x: prof_options[x],
                                    key="edit_responsable"
                                )
                                responsable_id = prof_ids[selected_prof_idx]
                            else:
                                st.error("❌ Aucun professeur trouvé dans la base de données!")
                                responsable_id = None
                            
                            new_capacite = st.number_input(
                                "Capacité maximale", 
                                min_value=10, 
                                max_value=500, 
                                 value=int(specialite_details['capacite_max'] or 50),
                                step=10,
                                key="edit_capacite"
                            )
                        
                        col_mod, col_cancel = st.columns(2)
                        
                        with col_mod:
                            if st.form_submit_button("Enregistrer", type="primary", use_container_width=True):
                                if new_nom and new_code:
                                    result = update_specialite(
                                        specialite_id, 
                                        new_nom, 
                                        formation_id, 
                                        niveau_id, 
                                        new_code, 
                                        new_description, 
                                        responsable_id, 
                                        new_capacite
                                    )
                                    if result:
                                        st.success("✅ Spécialité modifiée avec succès!")
                                        st.info("Les modifications ont été enregistrées dans la base de données.")
                                        import time
                                        time.sleep(1.5)
                                        st.rerun()
                                    else:
                                        st.error("❌ Erreur lors de la modification de la spécialité")
                                        st.info("Vérifiez que le nouveau code n'existe pas déjà pour une autre spécialité.")
                                else:
                                    if not new_nom:
                                        st.error("❌ Le nom est obligatoire")
                                    if not new_code:
                                        st.error("❌ Le code est obligatoire")
                        
                        with col_cancel:
                            if st.form_submit_button("❌ Annuler", use_container_width=True):
                                st.rerun()
                else:
                    st.error("❌ Impossible de charger les détails de la spécialité")
        else:
            st.info("Aucune spécialité à modifier")
    
    # Onglet 4: Supprimer une spécialité
    with tab4:
        st.header(" Supprimer une Spécialité")
        
        specialites = get_all_specialites()
        
        if specialites is not None and not specialites.empty:
            # Sélectionner la spécialité
            specialite_options_del = specialites['specialite'] + " (" + specialites['formation'] + " - " + specialites['niveau'] + ")"
            selected_idx_del = st.selectbox(
                "Choisir une spécialité à supprimer",
                range(len(specialite_options_del)),
                format_func=lambda x: specialite_options_del.iloc[x],
                key="delete_specialite_select"
            )
            
            if selected_idx_del is not None:
                specialite = specialites.iloc[selected_idx_del]
                specialite_id = int(specialite['id'])
                
                st.warning("Action irréversible!")
                
                # Afficher les détails de la spécialité
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader("Détails de la spécialité")
                        st.write(f"**Nom:** {specialite['specialite']}")
                        st.write(f"**Formation:** {specialite['formation']}")
                        st.write(f"**Niveau:** {specialite['niveau']}")
                        st.write(f"**Code:** {specialite['code_specialite']}")
                        st.write(f"**Responsable:** {specialite['responsable']}")
                        st.write(f"**Capacité maximale:** {specialite['capacite_max']}")
                        
                        if specialite['description']:
                            with st.expander("Description"):
                                st.write(specialite['description'])
                    
                    with col2:
                        st.error(" Attention!")
                        st.error("Cette action supprimera également tous les modules associés!")
                
                st.divider()
                
                # Confirmation de suppression
                confirm = st.checkbox("Je confirme vouloir supprimer cette spécialité", key="confirm_delete_specialite")
                
                col_sup, col_ann = st.columns(2)
                
                with col_sup:
                    if st.button("Supprimer définitivement", 
                                use_container_width=True, 
                                type="primary",
                                disabled=not confirm):
                        result = delete_specialite(specialite_id)
                        if result:
                            st.success("✅ Spécialité supprimée avec succès!")
                            st.info(" La spécialité a été supprimée de la base de données.")
                            import time
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la suppression de la spécialité")
                            st.info("Vérifiez qu'aucun module n'est associé à cette spécialité.")
                
                with col_ann:
                    if st.button("❌ Annuler", use_container_width=True):
                        st.info("Suppression annulée")
        else:
            st.info("Aucune spécialité à supprimer")



def page_generation_planning():
    """Page principale de génération de planning """
    set_page_background('generation_planning')
    
    # En-tête principal
    st.markdown("""
        <div class="main-header">
            <h1 class="page-title">Générateur Automatique de Planning</h1>
            <p class="page-subtitle">Génération intelligente avec contraintes avancées</p>
        </div>
    """, unsafe_allow_html=True)
    user_info = st.session_state['user_info']
    
    # Vérifier les permissions
    if user_info['role'] not in ['Admin_examens', 'Vice-doyen', 'Doyen']:
        st.error("Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité")
        return
    
    conn = get_db()
    if not conn:
        st.error("Impossible de se connecter à la base de données")
        return
    
    # Section des contraintes
    with st.expander(" CONFIGURATION DES CONTRAINTES", expanded=True):
        st.markdown('<div class="section-header">', unsafe_allow_html=True)
        st.markdown("### Contraintes appliquées")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(" Jours de travail:")
            st.markdown("<div class='constraint-item'>Samedi à Jeudi (pas de Vendredi)</div>", unsafe_allow_html=True)
            
            st.markdown(" Horaires par niveau:")
            horaires = ConfigContraintes().horaires_niveaux
            for niveau, info in horaires.items():
                st.markdown(f"<div class='constraint-item'>{niveau}: {info['debut'].strftime('%H:%M')} - {info['fin'].strftime('%H:%M')} (1h30)</div>", unsafe_allow_html=True)
            
            st.markdown(f" Jours fériés {datetime.now().year}:")
            jours_feries_html = ""
            for jour in ConfigContraintes().jours_feries:
                jours_feries_html += f"<span class='holiday-item'>{jour.strftime('%d/%m')}</span> "
            st.markdown(f"<div class='constraint-item'>{jours_feries_html}</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("Surveillance:")
            st.markdown("<div class='constraint-item'>• ≤30 étudiants: 1 surveillant</div>", unsafe_allow_html=True)
            st.markdown("<div class='constraint-item'>• 31-40 étudiants: 2 surveillants</div>", unsafe_allow_html=True)
            st.markdown("<div class='constraint-item'>• ≥41 étudiants: 3 surveillants</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='constraint-item'>• Max 3 surveillances/prof/jour</div>", unsafe_allow_html=True)
            st.markdown("<div class='constraint-item'>• Équilibrage automatique des surveillances</div>", unsafe_allow_html=True)
            
            st.markdown(" Organisation:")
            st.markdown("<div class='constraint-item'>• 1 examen/spécialité/jour max</div>", unsafe_allow_html=True)
            st.markdown("<div class='constraint-item'>• 1 jour libre entre 2 examens de même spécialité</div>", unsafe_allow_html=True)
            st.markdown("<div class='constraint-item'>• Attribution optimale des salles selon capacité</div>", unsafe_allow_html=True)
    
    # Section des filtres
    st.markdown("---")
    st.markdown('<h1 style="color:rgb(123, 36, 37);border-radius: 16px;padding: 20px;ackdrop-filter: blur(5px);background: rgba(255,255,255,0.1);margin-bottom: 32px;box-shadow: 0 4px 20px rgba(0,0,0,0.05);border: 1px solid #e2e8f0;text-align: center;"> FILTRES DE GÉNÉRATION</h1>' , unsafe_allow_html=True)
    
    
    with st.container():
        
        
        col_filtre1, col_filtre2, col_filtre3 = st.columns(3)
        
        with col_filtre1:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nom FROM specialites ORDER BY nom")
                specialites = cursor.fetchall()
                
                if specialites:
                    specialites_list = [("Toutes les spécialités", None)] + [(f"{nom}", id) for id, nom in specialites]
                    
                    selected_specialite = st.selectbox(
                        "Spécialité",
                        options=range(len(specialites_list)),
                        format_func=lambda x: specialites_list[x][0],
                        help="Sélectionnez une spécialité spécifique"
                    )
                    specialite_id = specialites_list[selected_specialite][1]
                else:
                    st.warning("Aucune spécialité trouvée")
                    specialite_id = None
            except Exception as e:
                st.error(f"Erreur chargement spécialités: {str(e)}")
                specialite_id = None
        
        with col_filtre2:
            niveaux = [
                ("Tous les niveaux", None),
                ("Licence 1 (L1)", "1"),
                ("Licence 2 (L2)", "2"),
                ("Licence 3 (L3)", "3"),
                ("Master 1 (M1)", "4"),
                ("Master 2 (M2)", "5")
            ]
            
            selected_niveau = st.selectbox(
                "Niveau",
                options=range(len(niveaux)),
                format_func=lambda x: niveaux[x][0]
            )
            annee_etude = niveaux[selected_niveau][1]
        
        with col_filtre3:
            semestres = [
                ("Tous les semestres", None),
                ("Semestre 1", "1"),
                ("Semestre 2", "2")
            ]
            
            selected_semestre = st.selectbox(
                "Semestre",
                options=range(len(semestres)),
                format_func=lambda x: semestres[x][0]
            )
            semestre = semestres[selected_semestre][1]
        
        # Afficher la sélection
        filtres_text = []
        if specialite_id:
            try:
                cursor.execute("SELECT nom FROM specialites WHERE id = %s", (specialite_id,))
                nom_specialite = cursor.fetchone()
                if nom_specialite:
                    filtres_text.append(f"Spécialité: {nom_specialite[0]}")
            except:
                pass
        
        if annee_etude:
            niveau_nom = dict([(v, k) for k, v in niveaux if v])[annee_etude]
            filtres_text.append(f"Niveau:{niveau_nom}")
        
        if semestre:
            semestre_nom = "Semestre 1" if semestre == "1" else "Semestre 2"
            filtres_text.append(f"Semestre: {semestre_nom}")
        
        if filtres_text:
            st.info(" | ".join(filtres_text))
        else:
             st.markdown('<p style="color:rgb(123, 36, 37);border-radius: 16px;padding: 20px;ackdrop-filter: blur(5px);background: rgba(255,255,255,0.1);margin-bottom: 32px;box-shadow: 0 4px 20px rgba(0,0,0,0.05);border: 1px solid #e2e8f0;text-align: center;"><span style="font-size:2.2em;  "></span> Aucun filtre appliqué - Tous les modules seront inclus</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section des paramètres de période
    st.markdown("### Période de génération")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_date = datetime.now().date() + timedelta(days=7)
        date_debut = st.date_input(
            "Date de début",
            min_date,
            min_value=min_date,
            help="Date à partir de laquelle commencer la planification"
        )
    
    with col2:
        date_fin_default = date_debut + timedelta(days=60)
        date_fin = st.date_input(
            "Date de fin",
            date_fin_default,
            min_value=date_debut + timedelta(days=14),
            help="Date limite pour la planification"
        )
    
    with col3:
        nom_base = "Planning"
        if specialite_id:
            try:
                cursor.execute("SELECT nom FROM specialites WHERE id = %s", (specialite_id,))
                nom_specialite = cursor.fetchone()
                if nom_specialite:
                    nom_base += f"_{nom_specialite[0].replace(' ', '_')}"
            except:
                pass
        
        if annee_etude:
            niveau_code_map = {"1": "L1", "2": "L2", "3": "L3", "4": "M1", "5": "M2"}
            niveau_code = niveau_code_map.get(annee_etude, f"N{annee_etude}")
            nom_base += f"_{niveau_code}"
        
        if semestre:
            nom_base += f"_S{semestre}"
        
        nom_base += f"_{date_debut.strftime('%Y%m%d')}_{date_fin.strftime('%Y%m%d')}"
        
        nom_planning = st.text_input(
            "Nom du planning",
            nom_base,
            help="Nom pour identifier ce planning"
        )
    
    if date_fin <= date_debut:
        st.error("La date de fin doit être après la date de début")
        st.stop()
    
   
    st.markdown("---")
    st.markdown('<h1 style="color:rgb(123, 36, 37);border-radius: 16px;padding: 20px;ackdrop-filter: blur(5px);background: rgba(255,255,255,0.1);margin-bottom: 32px;box-shadow: 0 4px 20px rgba(0,0,0,0.05);border: 1px solid #e2e8f0;text-align: center;"> Vérification des données</h1>' , unsafe_allow_html=True)
    
    try:
        cursor = conn.cursor()
        
        
        query = "SELECT COUNT(*) FROM modules WHERE 1=1"
        params = []
        
        if specialite_id:
            query += " AND specialite_id = %s"
            params.append(str(specialite_id))
        
        if annee_etude:
            query += " AND annee_etude = %s"
            params.append(str(annee_etude))
        
        if semestre:
            query += " AND semestre = %s"
            params.append(str(semestre))
        
        cursor.execute(query, params)
        nb_modules = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = true AND capacite > 0")
        nb_salles = cursor.fetchone()[0] or 0
        
        cursor.execute("SELECT COUNT(*) FROM professeurs WHERE est_surveillant = true")
        nb_professeurs = cursor.fetchone()[0] or 0
        
        # Afficher les statistiques
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        
        with col_stat1:
            if nb_modules >= 5:
                st.success(f"{nb_modules}modules")
            elif nb_modules > 0:
                st.warning(f"{nb_modules} modules")
            else:
                st.error(f"{nb_modules} modules")
        
        with col_stat2:
            if nb_salles >= 5:
                st.success(f"{nb_salles} salles")
            else:
                st.warning(f"{nb_salles} salles")
        
        with col_stat3:
            if nb_professeurs >= 8:
                st.success(f"{nb_professeurs} professeurs")
            else:
                st.warning(f"{nb_professeurs} professeurs")
        
        with col_stat4:
            if nb_modules > 0:
                query_inscrits = """
                    SELECT COUNT(DISTINCT i.etudiant_id)
                    FROM inscriptions i
                    JOIN modules m ON i.module_id = m.id
                    WHERE 1=1
                """
                params_inscrits = []
                
                if specialite_id:
                    query_inscrits += " AND m.specialite_id = %s"
                    params_inscrits.append(str(specialite_id))
                
                if annee_etude:
                    query_inscrits += " AND m.annee_etude = %s"
                    params_inscrits.append(str(annee_etude))
                
                if semestre:
                    query_inscrits += " AND m.semestre = %s"
                    params_inscrits.append(str(semestre))
                
                cursor.execute(query_inscrits, params_inscrits)
                nb_etudiants = cursor.fetchone()[0] or 0
                
                if nb_etudiants >= 20:
                    st.success(f"{nb_etudiants} étudiants")
                else:
                    st.warning(f"{nb_etudiants} étudiants")
            else:
                st.info("0 étudiants")
        
        # Si données insuffisantes
        if nb_modules == 0:
            st.markdown("---")
            st.error("###  Aucun module trouvé avec ces critères")
            st.markdown("**Veuillez :**")
            st.markdown("- Changer les critères de filtrage")
            st.markdown("- OU ajouter des modules dans la base de données")
            
            conn.close()
            st.stop()
        
        elif nb_modules < 5 or nb_salles < 5 or nb_professeurs < 8:
            st.markdown("---")
            st.warning("###  Données insuffisantes pour une génération optimale")
            st.markdown("**Pour une génération complète, il est recommandé d'avoir:**")
            st.markdown("- Au moins 5 modules")
            st.markdown("- Au moins 5 salles disponibles")
            st.markdown("- Au moins 8 professeurs surveillants")
            
            st.markdown("---")
    
    except Exception as e:
        st.error(f"Erreur vérification données: {str(e)}")
        conn.close()
        st.stop()
    
    # Bouton de génération
    st.markdown("---")
    col_gen1, col_gen2 = st.columns([3, 1])
    
    with col_gen1:
        if st.button(" GÉNÉRER LE PLANNING FILTRÉ", type="primary", use_container_width=True):
            with st.spinner("Génération du planning en cours..."):
                generateur = GenerateurPlanning()
                planning, conflits = generateur.generer_planning_filtre(
                    conn, date_debut, date_fin, user_info['id'],
                    specialite_id, annee_etude, semestre
                )
                
                st.session_state['planning_generated'] = planning
                st.session_state['planning_conflits'] = conflits
                st.session_state['generation_params'] = {
                    'date_debut': date_debut,
                    'date_fin': date_fin,
                    'nom_planning': nom_planning,
                    'specialite_id': specialite_id,
                    'annee_etude': annee_etude,
                    'semestre': semestre
                }
                st.session_state['generateur'] = generateur
                
                st.rerun()
    
    with col_gen2:
        if st.button(" Réinitialiser", type="secondary", use_container_width=True):
            st.session_state['planning_generated'] = None
            st.session_state['planning_conflits'] = []
            st.session_state['generateur'] = None
            st.rerun()
    
    # Afficher les conflits s'il y en a
    if st.session_state.get('planning_conflits'):
        conflits = st.session_state['planning_conflits']
        
        if conflits:
            st.markdown("---")
            st.markdown(f"###  Conflits détectés ({len(conflits)})")
            
            for conflit in conflits[:10]:
                st.markdown(f"""
                <div class="conflict-card">
                    <strong>{conflit.get('type', 'Conflit').upper()}</strong><br>
                    <strong>Problème:</strong> {conflit.get('message', 'N/A')}<br>
                    {f"<strong>Module:</strong> {conflit.get('module', 'N/A')}<br>" if 'module' in conflit else ""}
                    {f"<strong>Date:</strong> {conflit.get('date', 'N/A')}<br>" if 'date' in conflit else ""}
                    {f"<strong>Niveau:</strong> {conflit.get('niveau', 'N/A')}" if 'niveau' in conflit else ""}
                </div>
                """, unsafe_allow_html=True)
            
            if len(conflits) > 10:
                st.info(f"Et {len(conflits) - 10} autres conflits...")
    
    # Afficher le planning généré
    if st.session_state.get('planning_generated') and st.session_state.get('generateur'):
        planning = st.session_state['planning_generated']
        generateur = st.session_state['generateur']
        
        if not planning:
            st.info("Aucun examen généré")
            conn.close()
            return
        
        st.markdown("---")
        
        # Créer un titre basé sur les filtres
        titre = " PLANNING GÉNÉRÉ"
        params = st.session_state.get('generation_params', {})
        
        if params.get('specialite_id'):
            try:
                cursor.execute("SELECT nom FROM specialites WHERE id = %s", (params['specialite_id'],))
                specialite_nom = cursor.fetchone()
                if specialite_nom:
                    titre += f" - {specialite_nom[0]}"
            except:
                pass
        
        if params.get('annee_etude'):
            niveau_map = {"1": 'L1', "2": 'L2', "3": 'L3', "4": 'M1', "5": 'M2'}
            niveau = niveau_map.get(params['annee_etude'], f"Niveau {params['annee_etude']}")
            titre += f" - {niveau}"
        
        if params.get('semestre'):
            titre += f" - Semestre {params['semestre']}"
        
        titre += f" ({len(planning)} examens)"
        st.markdown(f"### {titre}")
        
        # Affichage du planning dans un tableau
        df = generateur.afficher_tableau_planning(conn)
        
        if df is not None:
            # Configurer les colonnes pour un meilleur affichage
            column_config = {
                "ID": st.column_config.NumberColumn("ID", width="small"),
                "Date": st.column_config.TextColumn("Date", width="small"),
                "Jour": st.column_config.TextColumn("Jour", width="small"),
                "Heure": st.column_config.TextColumn("Heure", width="small"),
                "Module": st.column_config.TextColumn("Module", width="large"),
                "Spécialité": st.column_config.TextColumn("Spécialité", width="medium"),
                "Niveau": st.column_config.TextColumn("Niveau", width="small"),
                "Salle": st.column_config.TextColumn("Salle", width="medium"),
                "Bâtiment": st.column_config.TextColumn("Bâtiment", width="small"),
                "Capacité": st.column_config.NumberColumn("Capacité", width="small"),
                "Étudiants": st.column_config.NumberColumn("Étudiants", width="small"),
                "Surveillants": st.column_config.TextColumn("Surveillants", width="large"),
                "Nb Sur.": st.column_config.NumberColumn("Nb Sur.", width="small"),
                "Prof. Principal": st.column_config.TextColumn("Prof. Principal", width="medium"),
                "Durée": st.column_config.TextColumn("Durée", width="small"),
                "Semestre": st.column_config.NumberColumn("Semestre", width="small"),
                "Année Étude": st.column_config.NumberColumn("Année", width="small")
            }
            
    
    # Déterminer la hauteur en fonction du mode
    
            
            st.dataframe(
                df,
                use_container_width=True,
                column_config=column_config,
                hide_index=True
            )
            
        
        # Afficher les statistiques
        generateur.afficher_statistiques()
        
        # Afficher les conflits
        if generateur.conflits:
            generateur.afficher_conflits()
        
        # Boutons d'action
        st.markdown("---")
        st.markdown("###  Actions")
        
        col_act1, col_act2, col_act3 = st.columns(3)
        
        with col_act1:
            if st.button(" SAUVEGARDER LE PLANNING", type="primary", use_container_width=True):
                with st.spinner("Sauvegarde en cours..."):
                    success, message = generateur.sauvegarder_planning(
                        conn, 
                        params.get('nom_planning', 'Planning_Non_Nomme'),
                        user_info['id']
                    )
                    
                    if success:
                        st.success(message)
                        st.session_state['planning_generated'] = None
                        st.session_state['planning_conflits'] = []
                        st.session_state['generateur'] = None
                        time_module.sleep(2)
                        st.rerun()
                    else:
                        st.error(message)
        
        with col_act2:
            csv = generateur.exporter_csv(conn)
            
            if csv:
                st.download_button(
                    label=" EXPORTER EN CSV",
                    data=csv,
                    file_name=f"{params.get('nom_planning', 'planning')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col_act3:
            if st.button(" EFFACER CE PLANNING", type="secondary", use_container_width=True):
                st.session_state['planning_generated'] = None
                st.session_state['planning_conflits'] = []
                st.session_state['generateur'] = None
                st.rerun()
    
    # Si pas encore généré
    else:
        st.markdown("---")
        with st.expander("GUIDE UTILISATION", expanded=True):
            st.markdown("""
            ### Comment générer un planning filtré :
            
            1. **Sélectionnez les filtres** :
               - **Spécialité** : Choisissez une spécialité spécifique ou toutes
               - **Niveau** : Sélectionnez un niveau (L1, L2, etc.)
               - **Semestre** : Choisissez un semestre (1 ou 2)
            
            2. **Configurez la période** :
               - Choisissez une date de début (minimum 7 jours après aujourd'hui)
               - Choisissez une date de fin
            
            3. **Vérifiez les données disponibles**
            
            4. **Cliquez sur "GÉNÉRER LE PLANNING FILTRÉ"**
            
            ### Toutes ces contraintes sont automatiquement gérées :
            
            **Calendrier:**
            - Pas d'examen le vendredi
            - Jours fériés exclus automatiquement
            - Planning du samedi au jeudi
            
             **Horaires par niveau:**
            - L1: 8h00 - 9h30
            - L2: 9h40 - 11h10  
            - L3: 11h20 - 12h50
            - M1: 14h00 - 15h30
            - M2: 15h40 - 17h10
            - Durée fixe: 1h30 par examen
            
            **Surveillance:**
            - 1-30 étudiants: 1 surveillant
            - 31-40 étudiants: 2 surveillants
            - 41+ étudiants: 3 surveillants
            - Max 3 surveillances/professeur/jour
            - Équilibrage automatique des surveillances
            
            **Organisation:**
            - 1 examen maximum par spécialité par jour
            - 1 jour libre minimum entre 2 examens d'une même spécialité
            - Attribution optimale des salles selon capacité
            
            ### Après génération :
            
            - **Tableau détaillé** avec toutes les informations
            - **Statistiques complètes** par niveau, spécialité, semestre
            - **Export CSV** avec toutes les données
            - **Sauvegarde** en base de données
            - **Visualisation** des conflits éventuels
            """)
    
    conn.close()

# =============================================
# PAGE VALIDATION EDT (AMÉLIORÉE)
# =============================================

def page_validation_edt():
    """Page de validation des EDT améliorée"""
  
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown(f'<h1>Validation des EDT Générés</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Valider, modifier ou supprimer les plannings générés</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    if user_info['role'] not in ['Vice-doyen', 'Doyen']:
        st.error("Accès réservé au vice-doyen et doyen")
        return
    
    conn = get_db()
    if not conn:
        st.error("Erreur de connexion")
        return
    
    # Onglets
    tab1, tab2 = st.tabs(["⏳ Plannings à valider", "✅ Plannings validés"])
    
    with tab1:
        st.markdown("### Plannings en attente de validation")
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT nom_planning, 
                       COUNT(*) as total_examens,
                       MIN(date_exam) as date_debut,
                       MAX(date_exam) as date_fin,
                       MIN(created_at) as created_at,
                       MIN(statut) as statut,
                       MIN(created_by) as created_by,
                       SUM(nb_inscrits) as total_etudiants,
                       SUM(nb_surveillants) as total_surveillants
                FROM planning_automatique
                WHERE statut = 'en_attente'
                GROUP BY nom_planning
                ORDER BY MIN(created_at) DESC
            """)
            
            plannings = cursor.fetchall()
            
            if not plannings:
                st.info("✅ Aucun planning en attente de validation")
            else:
                st.info(f" {len(plannings)} planning(s) en attente de validation")
                
                for planning in plannings:
                    (nom, total_examens, date_debut, date_fin, 
                     created_at, statut, created_by, total_etudiants, total_surveillants) = planning
                    
                    with st.expander(f"**{nom}** - {total_examens} examens - {total_etudiants} étudiants", expanded=False):
                        col_info1, col_info2, col_info3, col_info4 = st.columns(4)
                        
                        with col_info1:
                            st.metric(" Examens", total_examens)
                            st.metric(" Statut", "⏳ En attente")
                        
                        with col_info2:
                            st.metric(" Étudiants", total_etudiants)
                            st.metric(" Surveillants", total_surveillants)
                        
                        with col_info3:
                            st.metric("Période", f"{date_debut.strftime('%d/%m')} → {date_fin.strftime('%d/%m')}")
                            st.metric("Jours", (date_fin - date_debut).days + 1)
                        
                        with col_info4:
                            st.metric(" Créé le", created_at.strftime('%d/%m à %H:%M'))
                            st.metric("Par", f"ID: {created_by}")
                        
                        # Actions
                        st.markdown("---")
                        col_act1, col_act2, col_act3, col_act4 = st.columns(4)
                        
                        with col_act1:
                            if st.button("👁️ Voir détails", key=f"view_{nom}", use_container_width=True):
                                st.session_state['selected_planning'] = nom
                                st.session_state['menu'] = 'detail_planning_validation'
                                st.rerun()
                        
                        with col_act2:
                            if st.button("✅ Valider", key=f"val_{nom}", type="primary", use_container_width=True):
                                if update_planning_statut(conn, nom, 'validé', user_info['id']):
                                    st.success(f"✅ Planning '{nom}' validé!")
                                    time_module.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(" Erreur lors de la validation")
                        
                        with col_act3:
                            if st.button("✏ Modifier", key=f"edit_{nom}", use_container_width=True):
                                st.session_state['edit_planning'] = nom
                                st.session_state['menu'] = 'edit_planning'
                                st.rerun()
                        
                        with col_act4:
                            if st.button("🗑️ Supprimer", key=f"del_{nom}", type="secondary", use_container_width=True):
                                if st.checkbox(f"Confirmer suppression de '{nom}'?", key=f"confirm_del_{nom}"):
                                    success, message = supprimer_planning(conn, nom)
                                    if success:
                                        st.success(f"✅ {message}")
                                        time_module.sleep(1)
                                        st.rerun()
                                    else:
                                        st.error(f"❌ {message}")
        
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
    with tab2:
        st.markdown("### Plannings déjà validés")
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT nom_planning, 
                       COUNT(*) as total_examens,
                       MIN(date_exam) as date_debut,
                       MAX(date_exam) as date_fin,
                       MIN(created_at) as created_at,
                       MIN(statut) as statut,
                       MIN(created_by) as created_by,
                       SUM(nb_inscrits) as total_etudiants,
                       SUM(nb_surveillants) as total_surveillants,
                       MIN(validated_by) as validated_by,
                       MIN(validated_at) as validated_at
                FROM planning_automatique
                WHERE statut = 'validé'
                GROUP BY nom_planning
                ORDER BY MIN(validated_at) DESC
                LIMIT 10
            """)
            
            plannings_valides = cursor.fetchall()
            
            if not plannings_valides:
                st.info("ℹ️ Aucun planning validé")
            else:
                st.success(f"✅ {len(plannings_valides)} planning(s) validé(s)")
                
                for planning in plannings_valides:
                    (nom, total_examens, date_debut, date_fin, 
                     created_at, statut, created_by, total_etudiants, 
                     total_surveillants, validated_by, validated_at) = planning
                    
                    # Récupérer le nom du validateur
                    validateur_nom = "N/A"
                    if validated_by:
                        cursor.execute("SELECT username FROM utilisateurs WHERE id = %s", (validated_by,))
                        result = cursor.fetchone()
                        if result:
                            validateur_nom = result[0]
                    
                    with st.expander(f"✅ {nom} - {total_examens} examens", expanded=False):
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(" Examens", total_examens)
                            st.metric(" Étudiants", total_etudiants)
                        
                        with col2:
                            st.metric("Surveillants", total_surveillants)
                            st.metric(" Période", f"{date_debut.strftime('%d/%m')} → {date_fin.strftime('%d/%m')}")
                        
                        with col3:
                            st.metric(" Créé le", created_at.strftime('%d/%m à %H:%M'))
                            st.metric(" Créé par", f"ID: {created_by}")
                        
                        with col4:
                            st.metric("✅ Validé le", validated_at.strftime('%d/%m à %H:%M') if validated_at else "N/A")
                            st.metric(" Validé par", validateur_nom)
                        
                        # Bouton pour voir les détails
                        if st.button("👁️ Voir détails", key=f"view_valide_{nom}", use_container_width=True):
                            st.session_state['selected_planning'] = nom
                            st.session_state['menu'] = 'detail_planning_valide'
                            st.rerun()
    
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
    conn.close()

# =============================================
# FONCTIONS UTILITAIRES POUR LA VALIDATION
# =============================================

def update_planning_statut(conn, nom_planning, statut, user_id):
    """Met à jour le statut d'un planning"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE planning_automatique 
            SET statut = %s, 
                validated_by = %s, 
                validated_at = CURRENT_TIMESTAMP
            WHERE nom_planning = %s
        """, (statut, user_id, nom_planning))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        st.error(f"❌ Erreur mise à jour statut: {str(e)}")
        return False

def supprimer_planning(conn, nom_planning):
    """Supprime un planning"""
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM planning_automatique WHERE nom_planning = %s", (nom_planning,))
        conn.commit()
        return True, "✅ Planning supprimé avec succès"
    except Exception as e:
        conn.rollback()
        return False, f"❌ Erreur suppression: {str(e)}"

# =============================================
# PAGE DÉTAIL PLANNING POUR VALIDATION
# =============================================

def page_detail_planning_validation():
    """Page de détail d'un planning avec options de modification"""
    planning_name = st.session_state.get('selected_planning')
    
    if not planning_name:
        st.error("Aucun planning sélectionné")
        return
    
    st.markdown(f"""
        <div class="main-header">
            <h1 class="page-title">Détail du Planning: {planning_name}</h1>
            <p class="page-subtitle">Examen détaillé avec options de modification</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<div class="main-header">', unsafe_allow_html=True)
    st.markdown(f'<h1>Détail du Planning: {planning_name}</h1>', unsafe_allow_html=True)
    st.markdown('<p>Examen détaillé avec options de modification</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    conn = get_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Récupérer les informations générales
        cursor.execute("""
            SELECT COUNT(*) as total_examens,
                   MIN(date_exam) as date_debut,
                   MAX(date_exam) as date_fin,
                   SUM(nb_inscrits) as total_etudiants,
                   SUM(nb_surveillants) as total_surveillants,
                   MIN(statut) as statut
            FROM planning_automatique
            WHERE nom_planning = %s
            GROUP BY nom_planning
        """, (planning_name,))
        
        planning_info = cursor.fetchone()
        
        if planning_info:
            total_examens, date_debut, date_fin, total_etudiants, total_surveillants, statut = planning_info
            
            # Métriques
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(" Examens", total_examens)
            with col2:
                st.metric(" Étudiants", total_etudiants)
            with col3:
                st.metric(" Surveillants", total_surveillants)
            with col4:
                st.metric(" Statut", " En attente" if statut == 'en_attente' else "✅ Validé")
        
        # Récupérer les examens avec détails
        cursor.execute("""
            SELECT pa.id, pa.date_exam, pa.heure_debut, pa.heure_fin,
                   m.code_module, m.nom as module_nom,
                   l.nom as salle_nom, l.batiment, l.capacite,
                   pa.nb_inscrits, pa.nb_surveillants,
                   pa.surveillants_ids,
                   s.nom as specialite_nom,
                   m.annee_etude,
                   p.nom as prof_nom, p.prenom as prof_prenom
            FROM planning_automatique pa
            LEFT JOIN modules m ON pa.module_id = m.id
            LEFT JOIN lieu_examen l ON pa.salle_id = l.id
            LEFT JOIN specialites s ON m.specialite_id = s.id
            LEFT JOIN professeurs p ON m.prof_responsable_id = p.id
            WHERE pa.nom_planning = %s
            ORDER BY pa.date_exam, pa.heure_debut
        """, (planning_name,))
        
        exams = cursor.fetchall()
        
        if exams:
            st.markdown("###  Liste des examens")
            
            # Boutons d'action globaux
            col_global1, col_global2, col_global3 = st.columns(3)
            with col_global1:
                if st.button("⬅️ Retour aux validations", use_container_width=True):
                    st.session_state['menu'] = 'validation_edt'
                    st.rerun()
            
            with col_global2:
                if statut == 'en_attente':
                    if st.button(" Valider ce planning", type="primary", use_container_width=True):
                        if update_planning_statut(conn, planning_name, 'validé', st.session_state['user_info']['id']):
                            st.success(" Planning validé!")
                            time_module.sleep(2)
                            st.session_state['menu'] = 'validation_edt'
                            st.rerun()
            
            with col_global3:
                # Export CSV
                df_exams = pd.DataFrame(exams, columns=[
                    'ID', 'Date', 'Heure début', 'Heure fin', 'Code module', 'Module',
                    'Salle', 'Bâtiment', 'Capacité', 'Étudiants', 'Surveillants',
                    'IDs Surveillants', 'Spécialité', 'Année étude', 'Prof Nom', 'Prof Prénom'
                ])
                csv = df_exams.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label=" Exporter en CSV",
                    data=csv,
                    file_name=f"{planning_name}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            st.markdown("---")
            
            # Affichage des examens dans un tableau
            table_data = []
            for exam in exams:
                (exam_id, date_exam, heure_debut, heure_fin, code_module, module_nom,
                 salle, batiment, capacite, nb_etud, nb_surv, surveillants_ids,
                 specialite, annee_etude, prof_nom, prof_prenom) = exam
                
                # Formatage des surveillants
                surveillants_list = []
                if surveillants_ids:
                    for prof_id in surveillants_ids:
                        cursor.execute("SELECT nom, prenom FROM professeurs WHERE id = %s", (prof_id,))
                        prof = cursor.fetchone()
                        if prof:
                            surveillants_list.append(f"{prof[1]} {prof[0]}")
                
                table_data.append({
                    'ID': exam_id,
                    'Date': date_exam.strftime('%d/%m/%Y'),
                    'Jour': date_exam.strftime('%A'),
                    'Heure': f"{heure_debut.strftime('%H:%M')}-{heure_fin.strftime('%H:%M')}",
                    'Module': f"{code_module} - {module_nom}",
                    'Spécialité': specialite,
                    'Niveau': f"Année {annee_etude}",
                    'Salle': f"{salle} ({batiment})",
                    'Capacité': capacite,
                    'Étudiants': nb_etud,
                    'Surveillants': ", ".join(surveillants_list[:2]),
                    'Nb Sur.': nb_surv,
                    'Prof. Resp.': f"{prof_prenom} {prof_nom}" if prof_nom else "N/A"
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Options de modification par examen
            st.markdown("###  Modification d'examen")
            selected_exam_id = st.selectbox(
                "Sélectionnez un examen à modifier",
                options=df['ID'].tolist(),
                format_func=lambda x: f"ID {x}: {df[df['ID'] == x]['Module'].iloc[0]}"
            )
            
            if selected_exam_id:
                selected_exam = next((e for e in exams if e[0] == selected_exam_id), None)
                
                if selected_exam:
                    with st.form(f"modifier_examen_{selected_exam_id}"):
                        st.markdown(f"**Module:** {selected_exam[4]} - {selected_exam[5]}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            new_date = st.date_input("Nouvelle date", value=selected_exam[1])
                        with col2:
                            new_heure_debut = st.time_input("Nouvelle heure début", value=selected_exam[2])
                            new_heure_fin = st.time_input("Nouvelle heure fin", value=selected_exam[3])
                        
                        # Liste des salles disponibles
                        cursor.execute("""
                            SELECT id, nom, capacite 
                            FROM lieu_examen 
                            WHERE disponible_examen = true 
                            AND capacite >= %s
                            ORDER BY capacite
                        """, (selected_exam[9],))
                        
                        salles = cursor.fetchall()
                        salles_options = {f"{nom} ({capacite} places)": id for id, nom, capacite in salles}
                        
                        # Trouver l'index de la salle actuelle
                        current_salle = f"{selected_exam[6]} ({selected_exam[8]} places)"
                        salle_index = 0
                        if current_salle in salles_options:
                            salle_index = list(salles_options.keys()).index(current_salle)
                        
                        selected_salle = st.selectbox(
                            "Salle",
                            list(salles_options.keys()),
                            index=salle_index
                        )
                        new_salle_id = salles_options[selected_salle]
                        
                        # Boutons
                        col_submit, col_cancel = st.columns(2)
                        with col_submit:
                            submit = st.form_submit_button(" Enregistrer", use_container_width=True)
                        with col_cancel:
                            cancel = st.form_submit_button(" Annuler", use_container_width=True)
                        
                        if submit:
                            # Vérifier les conflits
                            cursor.execute("""
                                SELECT COUNT(*) 
                                FROM planning_automatique
                                WHERE nom_planning = %s
                                AND id != %s
                                AND date_exam = %s
                                AND salle_id = %s
                                AND (
                                    (heure_debut < %s AND heure_fin > %s)
                                    OR (heure_debut >= %s AND heure_debut < %s)
                                )
                            """, (planning_name, selected_exam_id, new_date, new_salle_id,
                                  new_heure_fin, new_heure_debut, new_heure_debut, new_heure_fin))
                            
                            conflits = cursor.fetchone()[0]
                            
                            if conflits > 0:
                                st.error("Cette salle est déjà occupée à cette heure!")
                            else:
                                # Mettre à jour l'examen
                                cursor.execute("""
                                    UPDATE planning_automatique 
                                    SET date_exam = %s,
                                        heure_debut = %s,
                                        heure_fin = %s,
                                        salle_id = %s
                                    WHERE id = %s AND nom_planning = %s
                                """, (new_date, new_heure_debut, new_heure_fin, 
                                      new_salle_id, selected_exam_id, planning_name))
                                
                                conn.commit()
                                st.success(" Examen modifié avec succès!")
                                time_module.sleep(2)
                                st.rerun()
        
        else:
            st.info("ℹ Aucun examen trouvé dans ce planning")
    
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
    finally:
        conn.close()

# =============================================
# PAGE DÉTAIL PLANNING VALIDÉ (LECTURE SEULE)
# =============================================

def page_detail_planning_valide():
    """Page de détails d'un planning validé (mode lecture seule)"""
  
    planning_name = st.session_state.get('selected_planning')
    
    if not planning_name:
        st.error(" Aucun planning sélectionné")
        return
    
    st.markdown(f'<div class="main-header">', unsafe_allow_html=True)
    st.markdown(f'<h1>Planning Validé: {planning_name}</h1>', unsafe_allow_html=True)
    st.markdown('<p>Consultation en lecture seule</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    conn = get_db()
    if not conn:
        return
    
    try:
        cursor = conn.cursor()
        
        # Vérifier que le planning est bien validé
        cursor.execute("""
            SELECT MIN(statut) FROM planning_automatique 
            WHERE nom_planning = %s
        """, (planning_name,))
        
        statut = cursor.fetchone()[0]
        
        if statut != 'validé':
            st.error(" Ce planning n'est pas validé")
            conn.close()
            return
        
        # Récupérer les informations générales
        cursor.execute("""
            SELECT 
                COUNT(*) as total_examens,
                MIN(date_exam) as date_debut,
                MAX(date_exam) as date_fin,
                SUM(nb_inscrits) as total_etudiants,
                SUM(nb_surveillants) as total_surveillants,
                COUNT(DISTINCT date_exam) as jours_utilises,
                COUNT(DISTINCT salle_id) as salles_utilisees,
                MIN(validated_at) as validated_at,
                MIN(validated_by) as validated_by
            FROM planning_automatique
            WHERE nom_planning = %s
        """, (planning_name,))
        
        planning_info = cursor.fetchone()
        
        if planning_info:
            (total_examens, date_debut, date_fin, total_etudiants, 
             total_surveillants, jours_utilises, salles_utilisees,
             validated_at, validated_by) = planning_info
            
            # Récupérer le nom du validateur
            validateur_nom = "N/A"
            if validated_by:
                cursor.execute("SELECT username FROM utilisateurs WHERE id = %s", (validated_by,))
                result = cursor.fetchone()
                if result:
                    validateur_nom = result[0]
            
            # Métriques
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric(" Examens", total_examens)
                st.metric("📆 Jours utilisés", jours_utilises)
            with col2:
                st.metric(" Étudiants", total_etudiants)
                st.metric(" Période", f"{date_debut.strftime('%d/%m')} → {date_fin.strftime('%d/%m')}")
            with col3:
                st.metric("👨‍🏫 Surveillants", total_surveillants)
                st.metric(" Salles utilisées", salles_utilisees)
            with col4:
                st.success("✅ Validé")
                st.metric("✅ Validé le", validated_at.strftime('%d/%m à %H:%M') if validated_at else "N/A")
                if st.button("⬅️ Retour", use_container_width=True):
                    st.session_state.pop('selected_planning', None)
                    st.session_state.pop('view_mode', None)
                    st.rerun()
        
        # Récupérer les examens avec détails
        cursor.execute("""
            SELECT 
                pa.date_exam, pa.heure_debut, pa.heure_fin,
                m.code_module, m.nom as module_nom,
                s.nom as specialite_nom,
                m.annee_etude, m.semestre,
                l.nom as salle_nom, l.batiment, l.capacite,
                pa.nb_inscrits, pa.nb_surveillants,
                pa.surveillants_ids,
                p.nom as prof_nom, p.prenom as prof_prenom
            FROM planning_automatique pa
            LEFT JOIN modules m ON pa.module_id = m.id
            LEFT JOIN specialites s ON m.specialite_id = s.id
            LEFT JOIN lieu_examen l ON pa.salle_id = l.id
            LEFT JOIN professeurs p ON m.prof_responsable_id = p.id
            WHERE pa.nom_planning = %s
            ORDER BY pa.date_exam, pa.heure_debut
        """, (planning_name,))
        
        exams = cursor.fetchall()
        
        if exams:
            st.markdown("### 📋 Liste des examens")
            
            # Tableau des examens
            table_data = []
            for exam in exams:
                (date_exam, heure_debut, heure_fin, code_module, module_nom,
                 specialite_nom, annee_etude, semestre, salle_nom, batiment,
                 capacite, nb_etud, nb_surv, surveillants_ids, prof_nom, prof_prenom) = exam
                
                # Récupérer les noms des surveillants
                surveillants_noms = []
                if surveillants_ids:
                    for prof_id in surveillants_ids:
                        cursor.execute("SELECT nom, prenom FROM professeurs WHERE id = %s", (prof_id,))
                        prof = cursor.fetchone()
                        if prof:
                            surveillants_noms.append(f"{prof[1]} {prof[0]}")
                
                # Format niveau
                niveau_map = {"1": 'L1', "2": 'L2', "3": 'L3', "4": 'M1', "5": 'M2'}
                niveau = niveau_map.get(str(annee_etude), f"N{annee_etude}")
                
                table_data.append({
                    'Date': date_exam.strftime('%d/%m/%Y'),
                    'Jour': date_exam.strftime('%A'),
                    'Heure': f"{heure_debut.strftime('%H:%M')} - {heure_fin.strftime('%H:%M')}",
                    'Module': f"{code_module} - {module_nom}",
                    'Spécialité': specialite_nom,
                    'Niveau': niveau,
                    'Salle': f"{salle_nom} ({batiment})",
                    'Capacité': capacite,
                    'Étudiants': nb_etud,
                    'Surveillants': ", ".join(surveillants_noms[:2]),
                    'Nb Sur.': nb_surv,
                    'Prof. Resp.': f"{prof_prenom} {prof_nom}" if prof_nom else "N/A",
                    'Semestre': semestre
                })
            
            df = pd.DataFrame(table_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Options d'export
            st.markdown("---")
            col_exp1, col_exp2 = st.columns(2)
            
            with col_exp1:
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="📥 Exporter en CSV",
                    data=csv,
                    file_name=f"{planning_name}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col_exp2:
                if st.button("📊 Voir statistiques", use_container_width=True):
                    # Afficher des statistiques avancées
                    st.markdown("#### 📈 Statistiques avancées")
                    
                    # Calculer l'occupation des salles
                    occupation_data = []
                    for exam in exams:
                        _, _, _, _, _, _, _, _, salle_nom, _, capacite, nb_etud, _, _, _, _ = exam
                        taux_occupation = (nb_etud / capacite * 100) if capacite > 0 else 0
                        occupation_data.append({
                            'Salle': salle_nom,
                            'Taux Occupation': f"{taux_occupation:.1f}%",
                            'Étudiants': nb_etud,
                            'Capacité': capacite
                        })
                    
                    if occupation_data:
                        df_occupation = pd.DataFrame(occupation_data)
                        st.dataframe(df_occupation, use_container_width=True)
        
        else:
            st.info("ℹ️ Aucun examen trouvé dans ce planning")
    
    except Exception as e:
        st.error(f"❌ Erreur: {str(e)}")
    finally:
        conn.close()

# =============================================
# PAGE GÉNÉRATION MANUELLE D'EXAMEN
# =============================================


# =============================================
# PAGE TABLEAU DE BORD PRINCIPAL AMÉLIORÉE
# =============================================
def set_page_background(page_name="dashboard"):
    """Définit l'image de fond selon la page"""
    
    # Mapping des pages aux images
    page_images = {
        'dashboard': 'pp.jpg',
        'generation_planning': 'pp.png',
        'validation_edt': 'pp.png',
        'login': 'pp.jpg',
        'default': 'pp.jpg'
    }
    
    image_file = page_images.get(page_name, page_images['default'])
    
    try:
        with open(image_file, "rb") as f:
            encoded = base64.b64encode(f.read()).decode()
        
        overlay_opacity = {
            'dashboard': 0.4,
            'login': 0.5,
            'default': 0.3
        }.get(page_name, 0.4)
        
        st.markdown(f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}") no-repeat center center fixed !important;
            background-size: cover !important;
            

        }}
        
        .stApp::before {{
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(0, 0, 0, {overlay_opacity});
            z-index: -1;
        }}
        </style>
        """, unsafe_allow_html=True)
        return True
    except:
        # Fallback à un fond uni si l'image n'existe pas
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        return False


def page_dashboard():
    """Tableau de bord amélioré avec visualisations avancées"""
    
    # ================= STYLE SUPPLEMENTAIRE =================
    st.markdown("""
    <style>
    
    .metric-card {
        border-radius: 16px;
        padding: 20px;
        margin: 10px 0;
        background: white;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.08);
        border-color: #c7d2fe;
    }
    
    .trend-up {
        color: #10b981;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .trend-down {
        color: #ef4444;
        font-weight: bold;
        font-size: 0.9rem;
    }
    
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-green { background-color: #10b981; }
    .status-yellow { background-color: #f59e0b; }
    .status-red { background-color: #ef4444; }
    
    /* Animation pour les KPI */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .pulse {
        animation: pulse 2s infinite;
    }
    
    /* Timeline */
    .timeline-item {
        position: relative;
        padding-left: 30px;
        margin-bottom: 20px;
        border-left: 2px solid #c7d2fe;
    }
    
    .timeline-dot {
        position: absolute;
        left: -8px;
        top: 0;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: #4f46e5;
    }
    
    /* Quick stats */
    .quick-stat {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px 15px;
        background: #f8fafc;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    .stat-icon {
        font-size: 1.5rem;
        margin-right: 10px;
    }
    
    /* Progress bars */
    .progress-container {
        width: 100%;
        background-color: #e2e8f0;
        border-radius: 10px;
        margin: 10px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 8px;
        border-radius: 10px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    }
    
    /* KPI cards spéciales */
    .kpi-highlight {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
        border-left: 4px solid #4f46e5;
    }
    
    .kpi-warning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-left: 4px solid #f59e0b;
    }
    
    .kpi-critical {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
    }
    
    /* Donut chart container */
    .donut-container {
        text-align: center;
        padding: 15px;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }
    
    
    .legend-item {
        display: flex;
        align-items: center;
        margin: 5px 0;
        font-size: 0.85rem;
    }
    
    .legend-color {
        width: 12px;
        height: 12px;
        border-radius: 3px;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ================= HEADER DYNAMIQUE =================
    set_page_background('default')
    current_time = datetime.now()
    # Déterminer le message de bienvenue
    if current_time.hour < 12:
        greeting = "Bonjour"
    elif current_time.hour < 18:
        greeting = "Bon après-midi"
    else:
        greeting = "Bonsoir"
    
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; justify-content: space-between; align-items: center; ">
            <div>
                <h1>{greeting}, {st.session_state['user_info'].get('username', 'Cher utilisateur')} !</h1>
                <p>Système intelligent de planification des examens | {current_time.strftime('%A %d %B %Y, %H:%M')}</p>
            </div>
            <div style="backdrop-filter: blur(5px);
        background: rgba(255,255,255,0.1);
                      padding: 10px 20px; border-radius: 12px; color: white; font-weight: 600;">
                Tableau de bord UMBB
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    conn = get_db()
    if not conn:
        st.error("Connexion à la base de données impossible")
        return
    
    try:
        cursor = conn.cursor()
        
        # ================= INDICATEURS CLÉS DE PERFORMANCE AMÉLIORÉS =================
        st.markdown("## Indicateurs clés de performance")
        
        # Récupérer des données de base d'abord
        cursor.execute("""
            SELECT 
                -- Données globales
                (SELECT COUNT(*) FROM etudiants) as total_etudiants,
                (SELECT COUNT(*) FROM professeurs) as total_profs,
                (SELECT COUNT(*) FROM modules) as total_modules,
                (SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = true) as salles_disponibles,
                
                -- Statistiques de plannings
                (SELECT COUNT(*) FROM planning_automatique WHERE statut = 'validé') as examens_valides,
                (SELECT COUNT(*) FROM planning_automatique WHERE statut = 'en_attente') as examens_en_attente,
                (SELECT COUNT(*) FROM planning_automatique WHERE statut = 'rejeté') as examens_rejetes
        """)
        
        kpi_basics = cursor.fetchone()
        
        # Récupérer les données supplémentaires
        cursor.execute("""
            SELECT 
                -- Taux d'occupation
                COALESCE(
                    (SELECT ROUND(AVG(CASE WHEN pa.nb_inscrits * 100.0 / NULLIF(l.capacite, 0) > 100 THEN 100 
                                 ELSE pa.nb_inscrits * 100.0 / NULLIF(l.capacite, 0) END), 1)
                     FROM planning_automatique pa
                     JOIN lieu_examen l ON pa.salle_id = l.id
                     WHERE pa.statut = 'validé' 
                       AND pa.date_exam >= CURRENT_DATE), 0) as taux_occupation_futur,
                
                -- Conflits potentiels
                COALESCE(
                    (SELECT COUNT(DISTINCT pa1.id)
                     FROM planning_automatique pa1
                     JOIN planning_automatique pa2 ON pa1.salle_id = pa2.salle_id 
                         AND pa1.date_exam = pa2.date_exam
                         AND pa1.id != pa2.id
                     WHERE (pa1.heure_debut < pa2.heure_fin AND pa1.heure_fin > pa2.heure_debut)
                         AND pa1.statut = 'validé' 
                         AND pa2.statut = 'validé'
                         AND pa1.date_exam >= CURRENT_DATE), 0) as conflits_detectes,
                
                -- Taux de réussite planning
                COALESCE(
                    (SELECT ROUND(COUNT(CASE WHEN statut = 'validé' THEN 1 END) * 100.0 / 
                                  NULLIF(COUNT(*), 0), 1)
                     FROM planning_automatique), 0) as taux_reussite_planning
        """)
        
        kpi_advanced = cursor.fetchone()
        
        # Récupérer les données d'évolution
        cursor.execute("""
            SELECT 
                -- Évolution des données
                COALESCE((SELECT COUNT(*) FROM planning_automatique 
                     WHERE created_at >= CURRENT_DATE - INTERVAL '7 days'), 0) as examens_7j,
                
                COALESCE((SELECT COUNT(*) FROM etudiants 
                     WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'), 0) as etudiants_30j
        """)
        
        kpi_evolution = cursor.fetchone()
        
        # Récupérer les taux d'utilisation
        cursor.execute("""
            SELECT 
                -- Taux d'utilisation des ressources
                COALESCE(
                    (SELECT ROUND(COUNT(DISTINCT l.id) * 100.0 / 
                                  NULLIF((SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = true), 0), 1)
                     FROM planning_automatique pa
                     JOIN lieu_examen l ON pa.salle_id = l.id
                     WHERE pa.date_exam >= CURRENT_DATE), 0) as taux_utilisation_salles,
                
                -- Charge moyenne des professeurs
                COALESCE(
                    (SELECT ROUND(AVG(nb_surveillants), 1)
                     FROM planning_automatique 
                     WHERE date_exam >= CURRENT_DATE), 0) as moyenne_surveillants
        """)
        
        kpi_usage = cursor.fetchone()
        
        # Combiner toutes les données
        if kpi_basics and kpi_advanced and kpi_evolution and kpi_usage:
            total_etudiants = kpi_basics[0] or 0
            total_profs = kpi_basics[1] or 0
            total_modules = kpi_basics[2] or 0
            salles_disponibles = kpi_basics[3] or 0
            examens_valides = kpi_basics[4] or 0
            examens_en_attente = kpi_basics[5] or 0
            examens_rejetes = kpi_basics[6] or 0
            
            taux_occupation = kpi_advanced[0] or 0
            conflits_detectes = kpi_advanced[1] or 0
            taux_reussite = kpi_advanced[2] or 0
            
            examens_7j = kpi_evolution[0] or 0
            etudiants_30j = kpi_evolution[1] or 0
            
            taux_utilisation_salles = kpi_usage[0] or 0
            moyenne_surveillants = kpi_usage[1] or 0
            
            # KPI en 4 colonnes avec indicateurs améliorés
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Indicateur 1: Étudiants
                st.markdown(f"""
                <div class="metric-card kpi-highlight">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Étudiants inscrits
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 10px 0;">
                        {total_etudiants:,}
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div class="trend-up">
                            +{etudiants_30j} nouveaux (30j)
                        </div>
                        <div style="font-size: 0.85rem; color: #64748b;">
                            Actifs
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Indicateur 2: Taux d'occupation
                occupation_class = "kpi-highlight"
                if taux_occupation > 80:
                    occupation_class = "kpi-warning"
                elif taux_occupation > 95:
                    occupation_class = "kpi-critical"
                
                st.markdown(f"""
                <div class="metric-card {occupation_class}">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Taux d'occupation
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 10px 0;">
                        {taux_occupation}%
                    </div>
                    <div class="progress-container">
                        <div class="progress-bar" style="width: {min(taux_occupation, 100)}%"></div>
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b; margin-top: 5px;">
                        Moyenne des salles futures
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                # Indicateur 3: Examens validés
                st.markdown(f"""
                <div class="metric-card kpi-highlight">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Examens programmés
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 10px 0;">
                        {examens_valides:,}
                    </div>
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <div class="trend-up">
                            +{examens_7j} cette semaine
                        </div>
                        <div style="font-size: 0.85rem; color: #64748b;">
                            Validés
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Indicateur 4: Taux de réussite planning
                reussite_class = "kpi-critical"
                if taux_reussite > 60:
                    reussite_class = "kpi-warning"
                if taux_reussite > 85:
                    reussite_class = "kpi-highlight"
                
                st.markdown(f"""
                <div class="metric-card {reussite_class}">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Taux de validation
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 10px 0;">
                        {taux_reussite}%
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        {examens_en_attente} en attente • {examens_rejetes} rejetés
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Indicateur 5: Salles disponibles
                st.markdown(f"""
                <div class="metric-card kpi-highlight">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Salles disponibles
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 10px 0;">
                        {salles_disponibles:,}
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        Taux d'utilisation: {taux_utilisation_salles}%
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b; margin-top: 5px;">
                        Capacité moyenne optimisée
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Indicateur 6: Conflits détectés
                conflits_class = "kpi-highlight"
                if conflits_detectes > 0:
                    conflits_class = "kpi-warning"
                if conflits_detectes > 5:
                    conflits_class = "kpi-critical"
                
                st.markdown(f"""
                <div class="metric-card {conflits_class}">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Conflits détectés
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 10px 0;">
                        {conflits_detectes}
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        Dans les plannings futurs
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                # Indicateur 7: Professeurs
                st.markdown(f"""
                <div class="metric-card kpi-highlight">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Enseignants
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 10px 0;">
                        {total_profs:,}
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        Charge moyenne: {moyenne_surveillants} surveillants/examen
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Indicateur 8: Modules
                st.markdown(f"""
                <div class="metric-card kpi-highlight">
                    <div style="color: #64748b; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px;">
                        Modules actifs
                    </div>
                    <div style="font-size: 2.5rem; font-weight: 800; color: black; margin: 10px 0;">
                        {total_modules:,}
                    </div>
                    <div style="font-size: 0.85rem; color: black;">
                        Base de données académique
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.error("Impossible de charger les indicateurs de performance")
            conn.close()
            return
        
        # ================= VISUALISATIONS INTERACTIVES (CERCLES/DONUTS) =================
        st.markdown("---")
        st.markdown("## Visualisations interactives")
        
        # Deux colonnes pour les visualisations en cercle
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Répartition des examens")
            
            # Données pour le graphique en anneau
            cursor.execute("""
                SELECT 
                    statut,
                    COUNT(*) as nombre
                FROM planning_automatique
                GROUP BY statut
                ORDER BY nombre DESC
            """)
            
            data_statuts = cursor.fetchall()
            
            if data_statuts:
                df_statuts = pd.DataFrame(data_statuts, columns=["Statut", "Nombre"])
                
                # Calculer les pourcentages
                total = df_statuts["Nombre"].sum()
                df_statuts["Pourcentage"] = df_statuts["Nombre"] / total * 100
                
                # Graphique en anneau interactif
                fig = px.pie(df_statuts, 
                           values="Nombre", 
                           names="Statut",
                           hole=0.6,
                           color_discrete_sequence=['#10b981', '#f59e0b', '#ef4444'])
                
                fig.update_traces(textposition='inside', 
                                textinfo='percent+label',
                                hovertemplate="<b>%{label}</b><br>Quantité: %{value}<br>Pourcentage: %{percent}")
                
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#1e293b'),
                    margin=dict(t=30, l=0, r=0, b=0),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.1,
                        xanchor="center",
                        x=0.5
                    ),
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Légende détaillée
                st.markdown("#### Détails par statut:")
                for _, row in df_statuts.iterrows():
                    couleur = {
                        'validé': '#10b981',
                        'en_attente': '#f59e0b',
                        'rejeté': '#ef4444'
                    }.get(row['Statut'], '#64748b')
                    
                    st.markdown(f"""
                    <div class="legend-item">
                        <div class="legend-color" style="background-color: {couleur};"></div>
                        <div><strong>{row['Statut'].capitalize()}</strong>: {row['Nombre']} examens ({row['Pourcentage']:.1f}%)</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aucun examen disponible")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_viz2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Occupation des salles par type")
            
            # Données pour le graphique en cercle
            cursor.execute("""
                SELECT 
                    COALESCE(l.type, 'Non spécifié') as type_salle,
                    COUNT(DISTINCT pa.id) as nb_examens
                FROM planning_automatique pa
                LEFT JOIN lieu_examen l ON pa.salle_id = l.id
                WHERE pa.statut = 'validé'
                GROUP BY l.type
                ORDER BY nb_examens DESC
            """)
            
            data_salles = cursor.fetchall()
            
            if data_salles:
                df_salles = pd.DataFrame(data_salles, 
                                       columns=["Type", "Nombre d'examens"])
                
                # Graphique en cercle avec anneau
                fig = px.pie(df_salles, 
                           values="Nombre d'examens", 
                           names="Type",
                           hole=0.5,
                           color_discrete_sequence=px.colors.sequential.Viridis)
                
                fig.update_traces(textposition='outside', 
                                textinfo='percent+label',
                                hovertemplate="<b>%{label}</b><br>Examens: %{value}")
                
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#1e293b'),
                    margin=dict(t=30, l=0, r=0, b=0),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.1,
                        xanchor="center",
                        x=0.5
                    ),
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Tableau des performances
                st.markdown("#### Répartition par type:")
                for _, row in df_salles.iterrows():
                    st.markdown(f"""
                    <div style="background: #f8fafc; padding: 10px; border-radius: 8px; margin: 5px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div><strong>{row['Type'].capitalize()}</strong></div>
                            <div style="font-weight: 600;">{row["Nombre d'examens"]}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aucune donnée de salle disponible")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ================= TROISIÈME VISUALISATION EN CERCLES MULTIPLES =================
        st.markdown("---")
        col_viz3, col_viz4 = st.columns(2)
        
        with col_viz3:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Répartition par niveau d'étude")
            
            # Données pour les niveaux d'étude
            cursor.execute("""
                SELECT 
                    COALESCE(CAST(m.annee_etude AS VARCHAR), 'Non spécifié') as niveau,
                    COUNT(DISTINCT pa.id) as nb_examens
                FROM planning_automatique pa
                LEFT JOIN modules m ON pa.module_id = m.id
                WHERE pa.statut = 'validé'
                GROUP BY m.annee_etude
                ORDER BY niveau
            """)
            
            data_niveaux = cursor.fetchall()
            
            if data_niveaux:
                df_niveaux = pd.DataFrame(data_niveaux, 
                                        columns=["Niveau", "Nombre d'examens"])
                
                # Ajouter des libellés pour les niveaux
                niveau_labels = {
                    "1": "Licence 1",
                    "2": "Licence 2", 
                    "3": "Licence 3",
                    "4": "Master 1",
                    "5": "Master 2"
                }
                
                df_niveaux["Niveau Libellé"] = df_niveaux["Niveau"].map(lambda x: niveau_labels.get(x, x))
                
                # Graphique en anneau
                fig = px.pie(df_niveaux, 
                           values="Nombre d'examens", 
                           names="Niveau Libellé",
                           hole=0.4,
                           color_discrete_sequence=px.colors.qualitative.Pastel)
                
                fig.update_traces(textposition='inside', 
                                textinfo='percent+label',
                                hovertemplate="<b>%{label}</b><br>Examens: %{value}")
                
                fig.update_layout(
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font=dict(color='#1e293b'),
                    margin=dict(t=30, l=0, r=0, b=0),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=-0.1,
                        xanchor="center",
                        x=0.5
                    ),
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Statistiques par niveau
                st.markdown("#### Détails par niveau:")
                for _, row in df_niveaux.iterrows():
                    st.markdown(f"""
                    <div style="background: #f8fafc; padding: 8px 12px; border-radius: 8px; margin: 5px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div><strong>{row['Niveau Libellé']}</strong></div>
                            <div>{row['Nombre d\'examens']} examens</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aucune donnée par niveau disponible")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_viz4:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Utilisation des ressources")
            
            # Données pour l'utilisation des ressources
            cursor.execute("""
                SELECT 'Salles utilisées' as categorie, 
                       COALESCE((
                           SELECT ROUND(COUNT(DISTINCT l.id) * 100.0 / 
                                        NULLIF((SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = true), 0), 1)
                           FROM planning_automatique pa
                           JOIN lieu_examen l ON pa.salle_id = l.id
                           WHERE pa.date_exam >= CURRENT_DATE
                       ), 0) as valeur
                UNION ALL
                SELECT 'Plannings validés' as categorie,
                       COALESCE((
                           SELECT ROUND(COUNT(*) * 100.0 / 
                                        NULLIF((SELECT COUNT(*) FROM planning_automatique), 0), 1)
                           FROM planning_automatique WHERE statut = 'validé'
                       ), 0) as valeur
                UNION ALL
                SELECT 'Sans conflits' as categorie,
                       COALESCE((
                           SELECT ROUND((COUNT(*) - 
                                        COALESCE((
                                            SELECT COUNT(DISTINCT pa1.id)
                                            FROM planning_automatique pa1
                                            JOIN planning_automatique pa2 ON pa1.salle_id = pa2.salle_id 
                                                AND pa1.date_exam = pa2.date_exam
                                                AND pa1.id != pa2.id
                                            WHERE (pa1.heure_debut < pa2.heure_fin AND pa1.heure_fin > pa2.heure_debut)
                                                AND pa1.statut = 'validé' 
                                                AND pa2.statut = 'validé'
                                        ), 0)) * 100.0 / NULLIF(COUNT(*), 0), 1)
                           FROM planning_automatique WHERE statut = 'validé'
                       ), 0) as valeur
            """)
            
            data_ressources = cursor.fetchall()
            
            if data_ressources:
                df_ressources = pd.DataFrame(data_ressources, 
                                           columns=["Catégorie", "Taux"])
                
                # Graphique en barres radiales simplifié
                fig = px.bar_polar(df_ressources, 
                                  r="Taux", 
                                  theta="Catégorie",
                                  color="Taux",
                                  template="plotly_white",
                                  color_continuous_scale=px.colors.sequential.Viridis)
                
                fig.update_traces(
                    hovertemplate="<b>%{theta}</b><br>Taux: %{r}%<extra></extra>"
                )
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=False,
                    font=dict(color='#1e293b'),
                    height=350
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Détails des indicateurs de ressources
                st.markdown("#### Détails des indicateurs:")
                
                for _, row in df_ressources.iterrows():
                    valeur = row["Taux"]
                    couleur = "#10b981" if valeur > 75 else "#f59e0b" if valeur > 50 else "#ef4444"
                    
                    st.markdown(f"""
                    <div style="margin: 10px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                            <div style="font-weight: 500;">{row['Catégorie']}</div>
                            <div style="color: {couleur}; font-weight: 600;">{valeur}%</div>
                        </div>
                        <div class="progress-container">
                            <div class="progress-bar" style="width: {valeur}%; background: {couleur};"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Indicateurs de ressources non disponibles")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # ================= ACTIVITÉS ET ALERTES =================
        st.markdown("---")
        
        col_activity, col_alerts = st.columns([2, 1])
        
        with col_activity:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Activités récentes")
            
            cursor.execute("""
                SELECT 
                    'Examen' as type_activite,
                    pa.nom_planning,
                    pa.created_at,
                    COALESCE(u.username, 'Système') as utilisateur,
                    pa.statut
                FROM planning_automatique pa
                LEFT JOIN utilisateurs u ON pa.created_by = u.id
                WHERE pa.created_at >= CURRENT_DATE - INTERVAL '3 days'
                ORDER BY pa.created_at DESC
                LIMIT 5
            """)
            
            activities = cursor.fetchall()
            
            if activities:
                for activity in activities:
                    type_act, nom, created_at, username, statut = activity
                    
                    time_diff = current_time - created_at
                    if time_diff.days > 0:
                        time_text = f"{time_diff.days} jour(s)"
                    elif time_diff.seconds // 3600 > 0:
                        time_text = f"{time_diff.seconds // 3600} heure(s)"
                    else:
                        time_text = f"{time_diff.seconds // 60} minute(s)"
                    
                    couleur_type = {
                        'Examen': '#4f46e5',
                        'Module': '#10b981'
                    }.get(type_act, '#64748b')
                    
                    st.markdown(f"""
                    <div style="padding: 12px 0; border-bottom: 1px solid #f1f5f9;">
                        <div style="display: flex; align-items: start; gap: 12px;">
                            <div style="background: {couleur_type}; color: white; width: 24px; height: 24px; 
                                      border-radius: 6px; display: flex; align-items: center; justify-content: center; 
                                      font-size: 0.8rem; font-weight: 600;">
                                E
                            </div>
                            <div style="flex: 1;">
                                <div style="font-weight: 600; color: #1e293b;">
                                    {nom}
                                </div>
                                <div style="font-size: 0.85rem; color: #64748b; margin-top: 2px;">
                                    Par {username} • Statut: {statut} • Il y a {time_text}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Aucune activité récente")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_alerts:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown("### Alertes système")
            
            # Vérifier différentes alertes
            alertes = []
            
            # 1. Alertes de conflits
            if conflits_detectes > 0:
                alertes.append(("Conflits détectés", f"{conflits_detectes} conflits dans les plannings futurs", "critique"))
            
            # 2. Alertes de surcharge
            cursor.execute("""
                SELECT COUNT(*) 
                FROM planning_automatique pa
                JOIN lieu_examen l ON pa.salle_id = l.id
                WHERE pa.nb_inscrits > l.capacite * 0.95
                  AND pa.statut = 'validé'
                  AND pa.date_exam >= CURRENT_DATE
            """)
            surcharge = cursor.fetchone()[0] or 0
            if surcharge > 0:
                alertes.append(("Salles surchargées", f"{surcharge} examen(s) avec occupation >95%", "critique"))
            
            # 3. Alertes d'attente
            if examens_en_attente > 5:
                alertes.append(("Validations en attente", f"{examens_en_attente} plannings nécessitent validation", "avertissement"))
            
            # 4. Alertes de ressources
            cursor.execute("""
                SELECT COUNT(*)
                FROM professeurs p
                WHERE NOT EXISTS (
                    SELECT 1 FROM planning_automatique pa
                    WHERE p.id = ANY(pa.surveillants_ids)
                    AND pa.date_exam >= CURRENT_DATE - INTERVAL '30 days'
                )
                AND p.est_surveillant = true
            """)
            profs_inactifs = cursor.fetchone()[0] or 0
            if profs_inactifs > 5:
                alertes.append(("Ressources sous-utilisées", f"{profs_inactifs} professeurs inactifs (30j)", "information"))
            
            # Afficher les alertes
            if alertes:
                for titre, description, niveau in alertes:
                    couleur = {
                        'critique': '#ef4444',
                        'avertissement': '#f59e0b',
                        'information': '#3b82f6'
                    }.get(niveau, '#64748b')
                    
                    st.markdown(f"""
                    <div style="background: {couleur}10; border-left: 4px solid {couleur}; 
                              padding: 12px; border-radius: 8px; margin: 8px 0;">
                        <div style="font-weight: 600; color: #1e293b; margin-bottom: 4px;">
                            {titre}
                        </div>
                        <div style="font-size: 0.85rem; color: #64748b;">
                            {description}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #10b98110; border-left: 4px solid #10b981; 
                          padding: 12px; border-radius: 8px; margin: 8px 0;">
                    <div style="font-weight: 600; color: #1e293b; margin-bottom: 4px;">
                        Système optimal
                    </div>
                    <div style="font-size: 0.85rem; color: #64748b;">
                        Aucune alerte critique détectée
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            
        
        # ================= FOOTER AVEC SYSTÈME =================
        st.markdown("---")
        
        # Récupérer les stats système (sans colonne est_actif qui n'existe pas)
        cursor.execute("""
            SELECT 
                -- Tous les étudiants sont considérés comme actifs
                (SELECT COUNT(*) FROM etudiants) as etudiants_total,
                
                -- Tous les professeurs surveillants sont actifs
                (SELECT COUNT(*) FROM professeurs WHERE est_surveillant = true) as profs_surveillants,
                
                -- Tous les modules sont considérés comme actifs
                (SELECT COUNT(*) FROM modules) as modules_total,
                
                -- Examens futurs
                COALESCE((SELECT COUNT(*) FROM planning_automatique WHERE date_exam >= CURRENT_DATE), 0) as examens_futurs,
                
                -- Grandes salles
                COALESCE((SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = true AND capacite >= 50), 0) as grandes_salles,
                
                -- Moyenne étudiants par examen
                COALESCE((SELECT ROUND(AVG(nb_inscrits), 1) FROM planning_automatique WHERE statut = 'validé'), 0) as moyenne_etudiants
        """)
        
        system_stats = cursor.fetchone()
        
        if system_stats:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%); 
                      border-radius: 16px; padding: 20px; margin-top: 20px;">
                <div style="text-align: center; margin-bottom: 20px;">
                    <div style="font-size: 1.2rem; font-weight: 600; color: #1e293b;">
                        Vue d'ensemble du système
                    </div>
                    <div style="font-size: 0.9rem; color: #64748b;">
                        Statistiques opérationnelles
                    </div>
                </div>
                
                
            """, unsafe_allow_html=True)
            
            stats_items = [
                ("Étudiants", system_stats[0], "#4f46e5"),
                ("Surveillants actifs", system_stats[1], "#10b981"),
                ("Modules", system_stats[2], "#f59e0b"),
                ("Examens à venir", system_stats[3], "#8b5cf6"),
                ("Grandes salles", system_stats[4], "#ef4444"),
                ("Moyenne étudiants", f"{system_stats[5]:.1f}", "#64748b")
            ]
            
            for label, value, color in stats_items:
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <div style="font-size: 1.1rem; font-weight: 600; color: {color}; margin-bottom: 5px;">
                        {value}
                    </div>
                    <div style="font-size: 0.8rem; color: #64748b; line-height: 1.2;">
                        {label}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Informations de version et mise à jour
        st.markdown(f"""
        <div style="text-align: center; margin-top: 30px; padding: 15px; border-top: 1px solid #e2e8f0;">
            <div style="font-size: 0.85rem; color: black; margin-bottom: 5px;">
                Système de Gestion des Examens UMBB • Version 2.3 • Base de données active
            </div>
            <div style="font-size: 0.8rem; color: black;">
                Dernière actualisation: {current_time.strftime('%d/%m/%Y à %H:%M:%S')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erreur lors du chargement du tableau de bord: {str(e)}")
        import traceback
        st.code(f"Détails de l'erreur:\n{traceback.format_exc()}")
    finally:
        if conn:
            conn.close()


            
def afficher_sidebar():
    with st.sidebar:
        # ================= STYLE SIDEBAR AVEC LOGO =================
        st.markdown("""
        <style>
        .sidebar-logo-container {
            text-align: center;
            padding: 24px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
        }
        
        .logo-badge {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .logo-text {
            text-align: left;
        }
        
        .logo-text h3 {
            color: white;
            font-size: 1.4rem;
            font-weight: 700;
            margin: 0;
            background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            line-height: 1.2;
        }
        
        .logo-text p {
            color: rgba(255,255,255,0.7);
            font-size: 0.8rem;
            margin: 2px 0 0 0;
            line-height: 1.2;
        }
        
        .user-info {
            background: rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 16px;
            margin: 0 16px 24px 16px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        
        .user-name {
            color: white;
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 4px;
        }
        
        .role-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
            background: rgba(255,255,255,0.15);
            color: white;
        }
        
        .sidebar-section {
            color: rgba(255,255,255,0.5);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 0 24px;
            margin: 20px 0 10px 0;
            font-weight: 600;
        }
        
        .sidebar-footer {
            position: absolute;
            margin-top:10px;
            left: 0;
            right: 0;
            padding: 20px;
            text-align: center;
            color: rgba(255,255,255,0.5);
            font-size: 0.8rem;
            border-top: 1px solid rgba(255,255,255,0.1);
            background: rgba(0,0,0,0.1);
        }
        
        /* Effet de survol pour tous les boutons */
        .stButton button div p {
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover div p {
            color: #c7d2fe;
        }
        
        /* Style pour les statistiques */
        .stats-container {
            padding: 0 20px;
            margin-bottom: 20px;
        }
        
        .stat-item {
            margin-bottom: 16px;
        }
        
        .stat-label {
            color: rgba(255,255,255,0.7);
            font-size: 0.85rem;
            margin-bottom: 4px;
        }
        
        .stat-value {
            color: white;
            font-size: 1.4rem;
            font-weight: 700;
        } .logout-button-container {
            margin-top: auto;
            padding: 16px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        /* Centrer le bouton déconnexion */
        .logout-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        </style>
        """, unsafe_allow_html=True)

        # ================= LOGO UMBB =================
        st.markdown("""
        <div class="sidebar-logo-container">
            <div class="logo-badge">U</div>
            <div class="logo-text">
                <h3>UMBB</h3>
                <p>Gestion Examens</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        user_info = st.session_state.get('user_info', {})
        role = user_info.get('role', 'Utilisateur')
        menu_actif = st.session_state.get("menu", "dashboard")

        # ================= USER INFO =================
        st.markdown(f"""
        <div class="user-info">
            <div class="user-name">{user_info.get('username', 'Utilisateur')}</div>
            <div class="role-badge">{role}</div>
        </div>
        """, unsafe_allow_html=True)

        # ================= NAVIGATION =================
        st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

        def nav_button(label, key, primary=False):
            if st.button(label, use_container_width=True, type="primary" if menu_actif == key else "secondary"):
                st.session_state['menu'] = key
                st.rerun()

        if role in ['Admin_examens', 'Vice-doyen', 'Doyen']:
            nav_button("Tableau de bord", "dashboard", menu_actif == "dashboard")
            nav_button("Générer planning", "generation_planning", menu_actif == "generation_planning")
            
            if role in ['Vice-doyen', 'Doyen']:
                nav_button("Validation EDT", "validation_edt", menu_actif == "validation_edt")

            st.markdown('<div class="sidebar-section">Gestion des données</div>', unsafe_allow_html=True)
            nav_button("Départements", "gestion_departements", menu_actif == "gestion_departements")
            nav_button("Spécialités", "gestion_specialites", menu_actif == "gestion_specialites")
            nav_button("Formations", "gestion_formations", menu_actif == "gestion_formations")
            nav_button("Étudiants", "gestion_etudiants", menu_actif == "gestion_etudiants")
            nav_button("Professeurs", "gestion_professeurs", menu_actif == "gestion_professeurs")
            nav_button("Modules", "gestion_modules", menu_actif == "gestion_modules")
            nav_button("Salles", "gestion_salles", menu_actif == "gestion_salles")

        elif role == 'Professeur':
            nav_button("Mes plannings", "professeur_plannings", True)

        elif role == 'Etudiant':
            nav_button("Planning examens", "etudiant_plannings", True)

        st.divider()

        # ================= STATISTIQUES RAPIDES =================
        st.markdown('<div class="sidebar-section">Statistiques</div>', unsafe_allow_html=True)
        
        try:
            conn = get_db()
            if conn:
                cursor = conn.cursor()
                
                # Nombre d'examens aujourd'hui
                cursor.execute("SELECT COUNT(*) FROM planning_automatique WHERE DATE(created_at) = CURRENT_DATE")
                exams_aujourdhui = cursor.fetchone()[0] or 0
                
                # Nombre d'examens cette semaine
                cursor.execute("""
                    SELECT COUNT(*) FROM planning_automatique 
                    WHERE EXTRACT(WEEK FROM created_at) = EXTRACT(WEEK FROM CURRENT_DATE)
                """)
                exams_semaine = cursor.fetchone()[0] or 0
                
                # Nombre total d'étudiants
                cursor.execute("SELECT COUNT(*) FROM etudiants")
                total_etudiants = cursor.fetchone()[0] or 0
                
                st.markdown(f"""
                <div class="stats-container">
                    <div class="stat-item">
                        <div class="stat-label">Examens aujourd'hui</div>
                        <div class="stat-value">{exams_aujourdhui}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Examens cette semaine</div>
                        <div class="stat-value">{exams_semaine}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Étudiants inscrits</div>
                        <div class="stat-value">{total_etudiants}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                conn.close()
        except:
            st.markdown("""
            <div class="stats-container">
                <div style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">
                    Statistiques non disponibles
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ================= LOGOUT =================
        st.markdown('<div class="logout-button-container">', unsafe_allow_html=True)
        if st.button("Déconnexion", key="logout_btn", use_container_width=True, 
                    type="primary", help="Se déconnecter du système"):
            st.session_state.clear()
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        # ================= FOOTER =================
        from datetime import datetime
        st.markdown(f"""
        <div class="sidebar-footer">
            <div style="margin-bottom: 8px; font-size: 0.7rem; opacity: 0.6; color:black;">
                VERSION 2.3
            </div>
            <div style="font-size: 0.75rem;">
                © 2025 UMBB
            </div>
            <div style="font-size: 0.7rem; margin-top: 4px; color:black; opacity: 0.6; color:black;">
                {datetime.now().strftime('%d %B %Y')}
            </div>
        </div>
        """, unsafe_allow_html=True)
# =============================================
# PAGE PROFESSEUR - PLANNINGS VALIDÉS
# =============================================

def page_professeur_plannings():
    """Page pour professeur: afficher les plannings validés avec filtrage par spécialité"""
    
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown(f'<h1>Plannings d\'Examens - Espace Professeur</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Visualisation des plannings validés</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    conn = get_db()
    if not conn:
        st.error("Impossible de se connecter à la base de données")
        return
    
    try:
        cursor = conn.cursor()
        
        # Récupérer les spécialités disponibles
        cursor.execute("""
            SELECT DISTINCT s.nom 
            FROM specialites s
            JOIN modules m ON s.id = m.specialite_id
            JOIN planning_automatique pa ON m.id = pa.module_id
            WHERE pa.statut = 'validé'
            ORDER BY s.nom
        """)
        
        specialites = [s[0] for s in cursor.fetchall()]
        
        # Ajouter l'option "Toutes"
        specialites_options = ["Toutes"] + specialites
        
        # Filtre par spécialité
        specialite_filter = st.selectbox(
            "Filtrer par spécialité",
            specialites_options,
            help="Sélectionnez une spécialité pour filtrer les plannings"
        )
        
        # Récupérer les plannings
        plannings = get_validated_plannings_for_professor(conn, 
                                                         specialite_filter if specialite_filter != "Toutes" else None)
        
        if not plannings:
            st.info("Aucun planning validé trouvé")
            conn.close()
            return
        
        st.markdown(f"### {len(plannings)} planning(s) validé(s) trouvé(s)")
        
        for planning in plannings:
            (nom_planning, total_examens, date_debut, date_fin, 
             specialite_id, specialite_nom, statut) = planning
            
            with st.expander(f"{nom_planning} - {specialite_nom} ({total_examens} examens)", expanded=True):
                col_plan1, col_plan2, col_plan3 = st.columns(3)
                
                with col_plan1:
                    st.metric("Examens", total_examens)
                    st.metric("Statut", statut)
                
                with col_plan2:
                    st.metric("Spécialité", specialite_nom)
                    st.metric("Période", f"{date_debut.strftime('%d/%m')} → {date_fin.strftime('%d/%m/%Y')}")
                
                with col_plan3:
                    jours = (date_fin - date_debut).days + 1 if date_debut and date_fin else 0
                    st.metric("Durée", f"{jours} jours")
                    st.metric("Dates", f"{date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}")
                
                # Afficher les détails du planning
                details = get_planning_details(conn, nom_planning)
                
                if details:
                    # Filtrer par spécialité si un filtre est appliqué
                    if specialite_filter != "Toutes":
                        details = [d for d in details if d[6] == specialite_filter]
                    
                    if details:
                        st.markdown(f"#### Examens ({len(details)})")
                        
                        df_examens = pd.DataFrame(details, columns=[
                            'Date', 'Heure début', 'Heure fin', 'Code module', 
                            'Module', 'ID Spécialité', 'Spécialité', 'Année étude',
                            'Semestre', 'Salle', 'Bâtiment', 'Étudiants', 
                            'Surveillants', 'Statut', 'Créé le'
                        ])
                        
                        # Formater l'affichage
                        df_display = df_examens[['Date', 'Heure début', 'Heure fin', 
                                                'Module', 'Spécialité', 'Année étude',
                                                'Salle', 'Étudiants', 'Surveillants']].copy()
                        df_display['Date'] = df_display['Date'].apply(lambda x: x.strftime('%d/%m/%Y'))
                        df_display['Heure début'] = df_display['Heure début'].apply(lambda x: x.strftime('%H:%M'))
                        df_display['Heure fin'] = df_display['Heure fin'].apply(lambda x: x.strftime('%H:%M'))
                        
                        st.dataframe(df_display, use_container_width=True, hide_index=True)
                        
                        # Statistiques
                        st.markdown("#### Statistiques")
                        col_stat1, col_stat2, col_stat3 = st.columns(3)
                        
                        with col_stat1:
                            total_etudiants = df_examens['Étudiants'].sum()
                            st.metric("Total étudiants", total_etudiants)
                        
                        with col_stat2:
                            total_surveillants = df_examens['Surveillants'].sum()
                            st.metric("Total surveillants", total_surveillants)
                        
                        with col_stat3:
                            salles_uniques = df_examens['Salle'].nunique()
                            st.metric("Salles utilisées", salles_uniques)
                        
                        # Export CSV
                        csv = df_examens.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="Exporter le planning en CSV",
                            data=csv,
                            file_name=f"{nom_planning}_{specialite_nom}.csv",
                            mime="text/csv",
                            key=f"export_prof_{nom_planning}"
                        )
                    else:
                        st.info("Aucun examen trouvé pour ce filtre")
                else:
                    st.info("Aucun détail disponible pour ce planning")
    
    except Exception as e:
        st.error(f"Erreur: {str(e)}")
    finally:
        conn.close()
        
def creer_compte_etudiant(conn, etudiant_id, username, password):
    """Crée un compte pour un étudiant"""
    try:
        cursor = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("""
            INSERT INTO utilisateurs (username, password_hash, role_id, est_actif)
            VALUES (%s, %s, 4, true) RETURNING id
        """, (username, password_hash))
        
        user_id = cursor.fetchone()[0]
        
        cursor.execute("""
            UPDATE etudiants SET utilisateur_id = %s WHERE id = %s
        """, (user_id, etudiant_id))
        
        # Stocker le mot de passe en clair
        try:
            cursor.execute("""
                INSERT INTO password_log (username, plain_password)
                VALUES (%s, %s)
            """, (username, password))
        except:
            pass
        
        conn.commit()
        return True, "Compte créé"
    except Exception as e:
        conn.rollback()
        return False, str(e)
def changer_mot_de_passe_etudiant(conn, etudiant_id, username, new_password):
    """Change le mot de passe d'un étudiant"""
    try:
        cursor = conn.cursor()
        
        # 1. Hacher le nouveau mot de passe
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        # 2. Mettre à jour le mot de passe dans utilisateurs
        cursor.execute("""
            UPDATE utilisateurs 
            SET password_hash = %s
            WHERE id = (SELECT utilisateur_id FROM etudiants WHERE id = %s)
        """, (password_hash, etudiant_id))
        
        # 3. Stocker le mot de passe en clair dans password_log
        cursor.execute("""
            INSERT INTO password_log (username, plain_password)
            VALUES (%s, %s)
            ON CONFLICT (username) 
            DO UPDATE SET plain_password = EXCLUDED.plain_password, created_at = CURRENT_TIMESTAMP
        """, (username, new_password))
        
        conn.commit()
        return True, "Mot de passe changé avec succès"
    except Exception as e:
        conn.rollback()
        return False, f"Erreur: {str(e)}"    
def creer_compte_professeur(conn, professeur_id, username, password):
    """Crée un compte pour un professeur"""
    try:
        cursor = conn.cursor()
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        cursor.execute("""
            INSERT INTO utilisateurs (username, password_hash, role_id, est_actif)
            VALUES (%s, %s, 3, true) RETURNING id
        """, (username, password_hash))
        
        user_id = cursor.fetchone()[0]
        
        cursor.execute("""
            UPDATE professeurs SET utilisateur_id = %s WHERE id = %s
        """, (user_id, professeur_id))
        
        # Stocker le mot de passe en clair
        try:
            cursor.execute("""
                INSERT INTO password_log (username, plain_password)
                VALUES (%s, %s)
            """, (username, password))
        except:
            pass
        
        conn.commit()
        return True, "Compte créé"
    except Exception as e:
        conn.rollback()
        return False, str(e)
    
def changer_mot_de_passe_professeur(conn, professeur_id, username, new_password):
    """Change le mot de passe d'un professeur"""
    try:
        cursor = conn.cursor()
        
        # 1. Hacher le nouveau mot de passe
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        # 2. Mettre à jour le mot de passe dans utilisateurs
        cursor.execute("""
            UPDATE utilisateurs 
            SET password_hash = %s
            WHERE id = (SELECT utilisateur_id FROM professeurs WHERE id = %s)
        """, (password_hash, professeur_id))
        
        # 3. Stocker le mot de passe en clair dans password_log
        cursor.execute("""
            INSERT INTO password_log (username, plain_password)
            VALUES (%s, %s)
            ON CONFLICT (username) 
            DO UPDATE SET plain_password = EXCLUDED.plain_password, created_at = CURRENT_TIMESTAMP
        """, (username, new_password))
        
        conn.commit()
        return True, "Mot de passe changé avec succès"
    except Exception as e:
        conn.rollback()
        return False, f"Erreur: {str(e)}"
# =============================================
# FONCTIONS POUR LA VUE STRATÉGIQUE (VICE-DOYEN)
# =============================================

def get_strategic_data(conn):
    """Récupère les données pour la vue stratégique"""
    try:
        cursor = conn.cursor()
        
        # Occupation globale des amphis et salles
        cursor.execute("""
            SELECT 
                l.nom as salle,
                l.type,
                COUNT(DISTINCT pa.id) as nb_examens,
                SUM(pa.nb_inscrits) as total_etudiants,
                ROUND(COUNT(DISTINCT pa.date_e+xam) * 100.0 / 
                      (SELECT COUNT(DISTINCT date_exam) FROM planning_automatique WHERE statut = 'validé'), 2) as taux_occupation
            FROM planning_automatique pa
            JOIN lieu_examen l ON pa.salle_id = l.id
            WHERE pa.statut = 'validé'
            GROUP BY l.nom, l.type
            ORDER BY l.type, taux_occupation DESC
        """)
        occupation_data = cursor.fetchall()
        
        # Taux de conflits par département
        cursor.execute("""
            SELECT 
                s.nom as specialite,
                COUNT(DISTINCT pa.id) as total_examens,
                SUM(CASE 
                    WHEN EXISTS (
                        SELECT 1 FROM planning_automatique pa2 
                        WHERE pa2.date_exam = pa.date_exam 
                        AND pa2.heure_debut < pa.heure_fin 
                        AND pa2.heure_fin > pa.heure_debut 
                        AND pa2.salle_id = pa.salle_id 
                        AND pa2.id != pa.id
                    ) THEN 1 ELSE 0 END) as conflits,
                ROUND(
                    SUM(CASE 
                        WHEN EXISTS (
                            SELECT 1 FROM planning_automatique pa2 
                            WHERE pa2.date_exam = pa.date_exam 
                            AND pa2.heure_debut < pa.heure_fin 
                            AND pa2.heure_fin > pa.heure_debut 
                            AND pa2.salle_id = pa.salle_id 
                            AND pa2.id != pa.id
                        ) THEN 1 ELSE 0 END) * 100.0 / 
                    NULLIF(COUNT(DISTINCT pa.id), 0), 2
                ) as taux_conflits
            FROM planning_automatique pa
            JOIN modules m ON pa.module_id = m.id
            JOIN specialites s ON m.specialite_id = s.id
            WHERE pa.statut = 'validé'
            GROUP BY s.nom
            ORDER BY taux_conflits DESC
        """)
        conflits_data = cursor.fetchall()
        
        # KPIs académiques
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT p.id) as total_profs,
                SUM(CASE WHEN pa.statut = 'validé' THEN pa.nb_surveillants ELSE 0 END) as heures_surveillance_total,
                ROUND(AVG(pa.nb_surveillants), 1) as moyenne_surveillants_par_examen,
                COUNT(DISTINCT l.id) as salles_utilisees,
                (SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = true) as salles_totales,
                ROUND(COUNT(DISTINCT l.id) * 100.0 / NULLIF((SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = true), 0), 2) as taux_utilisation_salles
            FROM planning_automatique pa
            CROSS JOIN professeurs p
            JOIN lieu_examen l ON pa.salle_id = l.id
            WHERE pa.statut = 'validé'
        """)
        kpis_data = cursor.fetchone()
        
        # Heures par professeur
        cursor.execute("""
            SELECT 
                p.nom || ' ' || p.prenom as professeur,
                COUNT(DISTINCT pa.id) as nb_examens_surveilles,
                SUM(pa.nb_surveillants) * 1.5 as heures_surveillance
            FROM planning_automatique pa
            JOIN professeurs p ON p.id = ANY(pa.surveillants_ids)
            WHERE pa.statut = 'validé'
            GROUP BY p.id, p.nom, p.prenom
            ORDER BY heures_surveillance DESC
            LIMIT 10
        """)
        profs_data = cursor.fetchall()
        
        return {
            'occupation': occupation_data,
            'conflits': conflits_data,
            'kpis': kpis_data,
            'profs': profs_data
        }
    except Exception as e:
        st.error(f"Erreur chargement données stratégiques: {str(e)}")
        return None

        
def page_vue_strategique():
    """Vue stratégique globale pour le vice-doyen"""
  
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown('<h1>Vue Stratégique Globale</h1>', unsafe_allow_html=True)
    st.markdown('<p>Tableau de bord décisionnel pour le vice-doyen</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    conn = get_db()
    if not conn:
        st.error("Erreur de connexion")
        return
    
    # Onglets pour les différentes vues
    tab1, tab2, tab3, tab4 = st.tabs([
        " Occupation des salles",
        "⚠ Conflits par département",
        "📈 KPIs Académiques",
        "‍ Charge des professeurs"
    ])
    
    with tab1:
        st.markdown("### Occupation globale des amphis et salles")
        data = get_strategic_data(conn)
        
        if data and data['occupation']:
            df_occupation = pd.DataFrame(data['occupation'], 
                columns=['Salle', 'Type', 'Nb Examens', 'Total Étudiants', 'Taux Occupation %'])
            
            # Filtres
            col1, col2 = st.columns(2)
            with col1:
                type_filter = st.selectbox("Filtrer par type", ['Tous', 'salle', 'amphi', 'labo'])
            
            if type_filter != 'Tous':
                df_occupation = df_occupation[df_occupation['Type'] == type_filter]
            
            # Métriques
            col_met1, col_met2, col_met3, col_met4 = st.columns(4)
            with col_met1:
                st.metric("Salles utilisées", len(df_occupation))
            with col_met2:
                st.metric("Total examens", df_occupation['Nb Examens'].sum())
            with col_met3:
                st.metric("Total étudiants", df_occupation['Total Étudiants'].sum())
            with col_met4:
                taux_moyen = df_occupation['Taux Occupation %'].mean()
                st.metric("Occupation moyenne", f"{taux_moyen:.1f}%")
            
            # Graphique
            st.markdown("#### Taux d'occupation par salle")
            st.bar_chart(df_occupation.set_index('Salle')['Taux Occupation %'])
            
            # Tableau détaillé
            st.markdown("#### Détails par salle")
            st.dataframe(df_occupation, use_container_width=True)
        else:
            st.info("Aucune donnée d'occupation disponible")
    
    with tab2:
        st.markdown("### Taux de conflits par département")
        data = get_strategic_data(conn)
        
        if data and data['conflits']:
            df_conflits = pd.DataFrame(data['conflits'],
                columns=['Spécialité', 'Total Examens', 'Conflits', 'Taux Conflits %'])
            
            # Métriques
            col_met1, col_met2, col_met3 = st.columns(3)
            with col_met1:
                st.metric("Spécialités", len(df_conflits))
            with col_met2:
                st.metric("Total examens", df_conflits['Total Examens'].sum())
            with col_met3:
                conflits_totaux = df_conflits['Conflits'].sum()
                st.metric("Conflits totaux", conflits_totaux)
            
            # Graphique
            st.markdown("#### Taux de conflits par spécialité")
            st.bar_chart(df_conflits.set_index('Spécialité')['Taux Conflits %'])
            
            # Alertes
            if not df_conflits.empty:
                max_conflit = df_conflits.loc[df_conflits['Taux Conflits %'].idxmax()]
                if max_conflit['Taux Conflits %'] > 10:
                    st.error(f"⚠ **ALERTE:** {max_conflit['Spécialité']} a un taux de conflits de {max_conflit['Taux Conflits %']}%")
            
            # Tableau détaillé
            st.markdown("#### Détails par spécialité")
            st.dataframe(df_conflits, use_container_width=True)
        else:
            st.info("Aucun conflit détecté")
    
    with tab3:
        st.markdown("### KPIs Académiques")
        data = get_strategic_data(conn)
        
        if data and data['kpis']:
            kpis = data['kpis']
            
            # Métriques principales
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Professeurs", kpis[0])
            with col2:
                st.metric("Heures surveillance", f"{kpis[1]:.0f}h")
            with col3:
                st.metric("Moy. surveillants/examen", kpis[2])
            with col4:
                st.metric("Salles utilisées", f"{kpis[3]}/{kpis[4]} ({kpis[5]}%)")
            
            # KPIs avancés
            st.markdown("#### Indicateurs de performance")
            
            col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
            with col_kpi1:
                if kpis[5] > 80:
                    st.error(f" Taux d'utilisation salles: {kpis[5]}%")
                    st.info("Saturation des salles détectée")
                elif kpis[5] > 60:
                    st.warning(f"⚠️ Taux d'utilisation salles: {kpis[5]}%")
                else:
                    st.success(f"✅ Taux d'utilisation salles: {kpis[5]}%")
            
            with col_kpi2:
                if kpis[2] > 2.5:
                    st.warning(f"⚠ Moyenne surveillants: {kpis[2]}")
                    st.info("Charge de surveillance élevée")
                else:
                    st.success(f"✅ Moyenne surveillants: {kpis[2]}")
            
            with col_kpi3:
                heures_par_prof = kpis[1] / kpis[0] if kpis[0] > 0 else 0
                if heures_par_prof > 20:
                    st.error(f" Charge/professeur: {heures_par_prof:.1f}h")
                elif heures_par_prof > 15:
                    st.warning(f"⚠ Charge/professeur: {heures_par_prof:.1f}h")
                else:
                    st.success(f"✅ Charge/professeur: {heures_par_prof:.1f}h")
        else:
            st.info("Aucune donnée KPI disponible")
    
    with tab4:
        st.markdown("### Charge de surveillance par professeur")
        data = get_strategic_data(conn)
        
        if data and data['profs']:
            df_profs = pd.DataFrame(data['profs'],
                columns=['Professeur', 'Nb Examens', 'Heures Surveillance'])
            
            # Métriques
            col_met1, col_met2, col_met3 = st.columns(3)
            with col_met1:
                st.metric("Top 10 professeurs", len(df_profs))
            with col_met2:
                st.metric("Heures totales", f"{df_profs['Heures Surveillance'].sum():.0f}h")
            with col_met3:
                moyenne_heures = df_profs['Heures Surveillance'].mean()
                st.metric("Moyenne/heure", f"{moyenne_heures:.1f}h")
            
            # Graphique
            st.markdown("#### Charge de surveillance")
            st.bar_chart(df_profs.set_index('Professeur')['Heures Surveillance'])
            
            # Détection de surcharge
            st.markdown("#### Alertes de surcharge")
            for idx, row in df_profs.iterrows():
                if row['Heures Surveillance'] > 25:
                    st.error(f" **{row['Professeur']}**: {row['Heures Surveillance']:.1f}h (surveille {row['Nb Examens']} examens)")
                elif row['Heures Surveillance'] > 20:
                    st.warning(f"⚠ **{row['Professeur']}**: {row['Heures Surveillance']:.1f}h (surveille {row['Nb Examens']} examens)")
            
            # Tableau détaillé
            st.markdown("#### Détails par professeur")
            st.dataframe(df_profs, use_container_width=True)
        else:
            st.info("Aucune donnée de charge disponible")
    
    conn.close()

# =============================================
# PAGE VALIDATION EDT (MODIFIÉE)
# =============================================

def page_validation_edt():
    """Page de validation des EDT avec fonctionnalités étendues"""

    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown(f'<h1>Validation des EDT Générés</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Valider, modifier ou supprimer les plannings générés</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    if user_info['role'] not in ['Vice-doyen', 'Doyen']:
        st.error("Accès réservé au vice-doyen et doyen")
        return
    
    conn = get_db()
    if not conn:
        st.error("Erreur de connexion")
        return
    
    # Onglets
    tab1, tab2 = st.tabs([" Plannings à valider", "✅ Plannings validés"])
    
    with tab1:
        st.markdown("### Plannings en attente de validation")
        
        plannings = get_plannings_a_valider(conn)
        
        if not plannings:
            st.info("Aucun planning en attente de validation")
        else:
            for planning in plannings:
                (nom, total_examens, date_debut, date_fin, 
                 created_at, statut, created_by, total_etudiants, total_surveillants) = planning
                
                with st.expander(f"**{nom}** - {total_examens} examens - {total_etudiants} étudiants", expanded=True):
                    col_info1, col_info2, col_info3, col_info4 = st.columns(4)
                    
                    with col_info1:
                        st.metric("Examens", total_examens)
                        st.metric("Statut", " En attente")
                    
                    with col_info2:
                        st.metric("Étudiants", total_etudiants)
                        st.metric("Surveillants", total_surveillants)
                    
                    with col_info3:
                        st.metric("Période", f"{date_debut.strftime('%d/%m')} → {date_fin.strftime('%d/%m')}")
                        st.metric("Jours", (date_fin - date_debut).days + 1)
                    
                    with col_info4:
                        st.metric("Créé le", created_at.strftime('%d/%m à %H:%M'))
                        st.metric("Par", f"ID: {created_by}")
                    
                    # Actions
                    st.markdown("---")
                    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
                    
                    with col_act1:
                        if st.button("👁 Voir détails", key=f"view_{nom}", use_container_width=True):
                            st.session_state['selected_planning'] = nom
                            st.session_state['menu'] = 'detail_planning_validation'
                            st.rerun()
                    
                    with col_act2:
                        if st.button(" Valider", key=f"val_{nom}", type="primary", use_container_width=True):
                            if update_planning_statut(conn, nom, 'validé', user_info['id']):
                                st.success(f"Planning '{nom}' validé!")
                                time_module.sleep(1)
                                st.rerun()
                            else:
                                st.error("Erreur lors de la validation")
                    
                    with col_act3:
                        if st.button("✏️ Modifier", key=f"edit_{nom}", use_container_width=True):
                            st.session_state['edit_planning'] = nom
                            st.session_state['menu'] = 'edit_planning'
                            st.rerun()
                    
                    with col_act4:
                        if st.button("🗑️ Supprimer", key=f"del_{nom}", type="secondary", use_container_width=True):
                            if st.checkbox(f"Confirmer suppression de '{nom}'?", key=f"confirm_del_{nom}"):
                                success, message = supprimer_planning(conn, nom)
                                if success:
                                    st.success(message)
                                    time_module.sleep(1)
                                    st.rerun()
                                else:
                                    st.error(f"Erreur: {message}")
    
    with tab2:
        st.markdown("### Plannings déjà validés")
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT nom_planning, 
                       COUNT(*) as total_examens,
                       MIN(date_exam) as date_debut,
                       MAX(date_exam) as date_fin,
                       MIN(created_at) as created_at,
                       MIN(statut) as statut,
                       MIN(created_by) as created_by,
                       SUM(nb_inscrits) as total_etudiants,
                       SUM(nb_surveillants) as total_surveillants
                FROM planning_automatique
                WHERE statut = 'validé'
                GROUP BY nom_planning
                ORDER BY MIN(created_at) DESC
            """)
            
            plannings_valides = cursor.fetchall()
            
            if not plannings_valides:
                st.info("Aucun planning validé")
            else:
                for planning in plannings_valides:
                    (nom, total_examens, date_debut, date_fin, 
                     created_at, statut, created_by, total_etudiants, total_surveillants) = planning
                    
                    st.markdown(f"""
                    <div class="planning-item">
                        <strong>{nom}</strong><br>
                        <small>
                            📅 {date_debut.strftime('%d/%m')} → {date_fin.strftime('%d/%m/%Y')} | 
                            📚 {total_examens} examens | 
                            👥 {total_etudiants} étudiants |
                            👨‍🏫 {total_surveillants} surveillants
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Erreur: {str(e)}")
    
    conn.close()

# ===========================#
def page_gestion_etudiants():
    """Page de gestion des étudiants - Version améliorée"""
    set_page_background('login')
    
    # Ajout de styles CSS spécifiques pour cette page
    st.markdown("""
    <style>
    /* ============================================
       STYLES SPÉCIFIQUES GESTION ÉTUDIANTS
       ============================================ */
    
    /* Header principal */
    .etudiant-header {
        background: linear-gradient(135deg, rgba(21, 94, 117, 0.9) 0%, rgba(29, 78, 216, 0.9) 100%);
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .etudiant-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" fill-opacity="1" d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,144C672,139,768,181,864,186.7C960,192,1056,160,1152,144C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
        background-size: cover;
        opacity: 0.3;
    }
    
    .etudiant-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #dbeafe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
    }
    
    .etudiant-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }
    
    /* Cartes étudiant améliorées */
    .etudiant-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .etudiant-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        border-color: #c7d2fe;
    }
    
    .etudiant-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 20px 0 0 20px;
    }
    
    /* Badges spéciaux */
    .specialite-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.2);
    }
    
    .niveau-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.2);
    }
    
    .promo-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(245, 158, 11, 0.2);
    }
    
    /* Boutons améliorés */
    .btn-etudiant-modify {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .btn-etudiant-modify:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    .btn-etudiant-delete {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    .btn-etudiant-delete:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
    }
    
    /* Formulaire amélioré */
    .form-container-etudiant {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 35px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .form-label-etudiant {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 8px;
        display: block;
        font-size: 1rem;
    }
    
    /* Statistiques améliorées */
    .stat-card-etudiant {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    
    .stat-card-etudiant:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value-etudiant {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .stat-label-etudiant {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Onglets améliorés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 15px 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    /* Zone de recherche améliorée */
    .search-box-etudiant {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Bouton d'action principal */
    .btn-primary-etudiant {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 16px 32px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .btn-primary-etudiant:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(135deg, #0da271 0%, #047857 100%) !important;
    }
    
    /* Bouton secondaire */
    .btn-secondary-etudiant {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        color: #64748b !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .btn-secondary-etudiant:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #475569 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Message d'alerte amélioré */
    .alert-etudiant {
        background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
        border-left: 6px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
    }
    
    /* Card info étudiant */
    .info-card-etudiant {
        background: linear-gradient(135deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Animation d'entrée */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .etudiant-header {
            padding: 25px 20px;
        }
        
        .etudiant-header h1 {
            font-size: 2.2rem;
        }
        
        .etudiant-card {
            padding: 20px;
        }
        
        .stat-value-etudiant {
            font-size: 2.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    
    st.markdown("""
    <div class="etudiant-header fade-in-up">
        <h1>🎓 Gestion des Étudiants</h1>
        <p>Ajouter, modifier et gérer les étudiants de l'UMBB</p>
        <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
            <i class="fas fa-users" style="margin-right: 5px;">gérer les étudiants</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    if user_info['role'] not in ['Vice-doyen', 'Admin_examens']:
        st.error(" Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité")
        return
    
    conn = get_db()
    if not conn:
        st.error(" Impossible de se connecter à la base de données")
        return
    
    # Onglets avec style amélioré
    tab1, tab2, tab3 = st.tabs([
        " Ajouter un étudiant",
        " Liste des étudiants", 
        " Gestion des comptes"
    ])
    
    with tab1:
        st.markdown("###  Ajouter un nouvel étudiant")
        st.markdown("Remplissez le formulaire pour ajouter un nouvel étudiant à la base de données.")
        
        with st.form("ajout_etudiant", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="form-label-etudiant">Nom *</div>', unsafe_allow_html=True)
                nom = st.text_input("", placeholder="Entrez le nom de l'étudiant", label_visibility="collapsed")
            with col2:
                st.markdown('<div class="form-label-etudiant">Prénom *</div>', unsafe_allow_html=True)
                prenom = st.text_input("", placeholder="Entrez le prénom de l'étudiant", label_visibility="collapsed")
            
            st.markdown('<div class="form-label-etudiant">Email</div>', unsafe_allow_html=True)
            email = st.text_input("", placeholder="exemple@umbb.dz", label_visibility="collapsed")
            
            col_spec, col_niv = st.columns(2)
            with col_spec:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id, nom FROM specialites ORDER BY nom")
                    specialites = cursor.fetchall()
                    specialite_options = {nom: id for id, nom in specialites}
                    st.markdown('<div class="form-label-etudiant">Spécialité *</div>', unsafe_allow_html=True)
                    specialite = st.selectbox("", list(specialite_options.keys()), 
                                            format_func=lambda x: f" {x}",
                                            label_visibility="collapsed")
                    specialite_id = specialite_options[specialite]
                except Exception as e:
                    st.error(f"❌ Erreur de chargement des spécialités: {e}")
                    specialite_id = None
            
            with col_niv:
                try:
                    cursor.execute("SELECT id, nom FROM niveaux ORDER BY nom")
                    niveaux = cursor.fetchall()
                    niveau_options = {nom: id for id, nom in niveaux}
                    st.markdown('<div class="form-label-etudiant">Niveau actuel *</div>', unsafe_allow_html=True)
                    niveau = st.selectbox("", list(niveau_options.keys()),
                                        format_func=lambda x: f" {x}",
                                        label_visibility="collapsed")
                    niveau_id = niveau_options[niveau]
                except Exception as e:
                    st.error(f"❌ Erreur de chargement des niveaux: {e}")
                    niveau_id = None
            
            col_annee, col_promo = st.columns(2)
            with col_annee:
                st.markdown('<div class="form-label-etudiant">Année d\'étude *</div>', unsafe_allow_html=True)
                annee_etude = st.number_input("", min_value=1, max_value=5, value=1, 
                                            format="%d", label_visibility="collapsed")
            
            with col_promo:
                st.markdown('<div class="form-label-etudiant">Promotion *</div>', unsafe_allow_html=True)
                promo = st.number_input("", value=2024, min_value=2000, max_value=2030,
                                      format="%d", label_visibility="collapsed")
            
            st.markdown("---")
            
            # Boutons améliorés
            col_btn1, col_btn2, col_btn3 = st.columns(3)
            
            with col_btn1:
                submit_btn = st.form_submit_button(" AJOUTER L'ÉTUDIANT", 
                                                 type="primary",
                                                 use_container_width=True)
            
            with col_btn2:
                reset_btn = st.form_submit_button(" RÉINITIALISER",
                                                type="secondary",
                                                use_container_width=True)
            
            with col_btn3:
                cancel_btn = st.form_submit_button(" ANNULER",
                                                 type="secondary",
                                                 use_container_width=True)
            
            if submit_btn:
                if nom and prenom and specialite_id and niveau_id:
                    try:
                        cursor = conn.cursor()
                        cursor.execute(
                            "INSERT INTO etudiants (nom, prenom, email, promo, specialite_id, niveau_courant_id, annee_etude) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                            (nom, prenom, email if email else None, promo, specialite_id, niveau_id, annee_etude)
                        )
                        conn.commit()
                        
                        # Message de succès avec style
                        st.markdown(f"""
                        <div style="background: linear-gradient(135deg, rgba(209, 250, 229, 0.9) 0%, rgba(167, 243, 208, 0.9) 100%);
                                    border-left: 6px solid #10b981;
                                    border-radius: 12px;
                                    padding: 20px;
                                    margin: 15px 0;">
                            <div style="display: flex; align-items: center; gap: 15px;">
                                <div style="font-size: 2.5rem;">🎓</div>
                                <div>
                                    <h3 style="margin: 0; color: #065f46;">Étudiant ajouté avec succès!</h3>
                                    <p style="margin: 5px 0 0 0; color: #047857;">
                                        <strong>{prenom} {nom}</strong> a été ajouté à la base de données.
                                    </p>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        time_module.sleep(2)
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erreur: {str(e)}")
                else:
                    st.error("⚠ Les champs marqués d'un * sont obligatoires")
                    st.info("Veuillez remplir tous les champs obligatoires.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="search-box-etudiant fade-in-up">', unsafe_allow_html=True)
        st.markdown("###  Rechercher un étudiant")
        
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search = st.text_input("", 
                                 placeholder="Rechercher par nom, prénom, email ou spécialité...",
                                 label_visibility="collapsed")
        
        with col_filter:
            filter_option = st.selectbox("Filtrer par:", 
                                       ["Tous", "Avec email", "Sans email"],
                                       label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT e.id, e.nom, e.prenom, e.email, e.promo, 
                       s.nom as specialite, n.nom as niveau, e.annee_etude,
                       (SELECT COUNT(*) FROM inscriptions WHERE etudiant_id = e.id) as nb_modules
                FROM etudiants e 
                LEFT JOIN specialites s ON e.specialite_id = s.id
                LEFT JOIN niveaux n ON e.niveau_courant_id = n.id
                ORDER BY e.nom, e.prenom
            """)
            
            etudiants = cursor.fetchall()
            
            if etudiants:
                # Appliquer les filtres
                etudiants_filtres = etudiants
                
                if search:
                    search_lower = search.lower()
                    etudiants_filtres = [
                        e for e in etudiants_filtres 
                        if (search_lower in str(e[1]).lower() or 
                            search_lower in str(e[2]).lower() or 
                            search_lower in str(e[3]).lower() or
                            search_lower in str(e[5]).lower())
                    ]
                
                if filter_option == "Avec email":
                    etudiants_filtres = [e for e in etudiants_filtres if e[3]]
                elif filter_option == "Sans email":
                    etudiants_filtres = [e for e in etudiants_filtres if not e[3]]
                
                # Statistiques
                st.markdown("### 📊 Statistiques")
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.markdown(f"""
                    <div class="stat-card-etudiant">
                        <div class="stat-value-etudiant">{len(etudiants_filtres)}</div>
                        <div class="stat-label-etudiant">Étudiants trouvés</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_stat2:
                    avec_email = len([e for e in etudiants_filtres if e[3]])
                    st.markdown(f"""
                    <div class="stat-card-etudiant">
                        <div class="stat-value-etudiant">{avec_email}</div>
                        <div class="stat-label-etudiant">Avec email</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_stat3:
                    moy_modules = sum([e[8] for e in etudiants_filtres]) / len(etudiants_filtres) if etudiants_filtres else 0
                    st.markdown(f"""
                    <div class="stat-card-etudiant">
                        <div class="stat-value-etudiant">{moy_modules:.1f}</div>
                        <div class="stat-label-etudiant">Moy. modules</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_stat4:
                    niveaux_unique = len(set([e[6] for e in etudiants_filtres if e[6]]))
                    st.markdown(f"""
                    <div class="stat-card-etudiant">
                        <div class="stat-value-etudiant">{niveaux_unique}</div>
                        <div class="stat-label-etudiant">Niveaux</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("---")
                st.markdown(f"###  Liste des étudiants ({len(etudiants_filtres)})")
                
                for idx, etudiant in enumerate(etudiants_filtres):
                    id_etudiant, nom, prenom, email, promo, specialite, niveau, annee_etude, nb_modules = etudiant
                    
                    with st.expander(f"🎓 **{prenom} {nom}** - {specialite if specialite else 'Non assignée'}", expanded=False):
                        col_info, col_actions = st.columns([3, 1])
                        
                        with col_info:
                            st.markdown(f"""
                            <div class="info-card-etudiant">
                                <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 15px;">
                                    <div style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); 
                                                color: white; width: 60px; height: 60px; border-radius: 50%; 
                                                display: flex; align-items: center; justify-content: center; 
                                                font-size: 24px; font-weight: bold;">
                                        {prenom[0].upper()}{nom[0].upper()}
                                    </div>
                                    <div>
                                        <h3 style="margin: 0; color: #1e293b;">{prenom} {nom}</h3>
                                        <p style="margin: 5px 0 0 0; color: #64748b;">
                                            ID: {id_etudiant} | Promotion: {promo}
                                        </p>
                                    </div>
                                </div>
                                
                                <div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 15px 0;">
                                    <span class="specialite-badge"> {specialite if specialite else 'Non assignée'}</span>
                                    <span class="niveau-badge"> {niveau if niveau else 'Non assigné'}</span>
                                    <span class="promo-badge"> Promotion {promo}</span>
                                    <span style="background: #f1f5f9; color: #475569; padding: 6px 16px; 
                                                border-radius: 25px; font-size: 0.85rem;">
                                         {nb_modules} modules
                                    </span>
                                </div>
                                
                                <div style="margin-top: 15px;">
                                    <p style="margin: 5px 0;"><strong> Email:</strong> {email if email else 'Non renseigné'}</p>
                                    <p style="margin: 5px 0;"><strong> Année d'étude:</strong> {annee_etude}</p>
                                    <p style="margin: 5px 0;"><strong> Spécialité:</strong> {specialite if specialite else 'Non assignée'}</p>
                                    <p style="margin: 5px 0;"><strong>Niveau:</strong> {niveau if niveau else 'Non assigné'}</p>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with col_actions:
                            st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
                            
                            # Bouton Modifier
                            if st.button("✏️ Modifier", 
                                       key=f"edit_etudiant_{id_etudiant}",
                                       use_container_width=True):
                                st.session_state['edit_mode'][f'etudiant_{id_etudiant}'] = True
                                st.rerun()
                            
                            st.markdown('<div style="margin: 10px 0;"></div>', unsafe_allow_html=True)
                            
                            # Bouton Supprimer
                            if st.button("🗑 Supprimer",
                                       key=f"del_etudiant_{id_etudiant}",
                                       type="secondary",
                                       use_container_width=True):
                                st.session_state['delete_mode'][f'etudiant_{id_etudiant}'] = True
                                st.rerun()
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Section modification
                        if st.session_state['edit_mode'].get(f'etudiant_{id_etudiant}', False):
                            st.markdown("---")
                            st.markdown("### ✏ Modifier l'étudiant")
                            
                            with st.form(f"modifier_etudiant_{id_etudiant}"):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    st.markdown('<div class="form-label-etudiant">Nom</div>', unsafe_allow_html=True)
                                    new_nom = st.text_input("", value=nom, 
                                                          key=f"nom_{id_etudiant}",
                                                          label_visibility="collapsed")
                                with col_b:
                                    st.markdown('<div class="form-label-etudiant">Prénom</div>', unsafe_allow_html=True)
                                    new_prenom = st.text_input("", value=prenom, 
                                                             key=f"prenom_{id_etudiant}",
                                                             label_visibility="collapsed")
                                
                                st.markdown('<div class="form-label-etudiant">Email</div>', unsafe_allow_html=True)
                                new_email = st.text_input("", value=email if email else "", 
                                                        key=f"email_{id_etudiant}",
                                                        label_visibility="collapsed")
                                
                                # Charger les spécialités
                                cursor.execute("SELECT id, nom FROM specialites ORDER BY nom")
                                specialites_all = cursor.fetchall()
                                specialite_options = {nom: id for id, nom in specialites_all}
                                
                                current_specialite = specialite if specialite else list(specialite_options.keys())[0] if specialite_options else None
                                
                                if current_specialite and current_specialite in specialite_options:
                                    specialite_index = list(specialite_options.keys()).index(current_specialite)
                                else:
                                    specialite_index = 0
                                
                                st.markdown('<div class="form-label-etudiant">Spécialité</div>', unsafe_allow_html=True)
                                new_specialite = st.selectbox(
                                    "", 
                                    list(specialite_options.keys()),
                                    index=specialite_index if specialite_index < len(specialite_options.keys()) else 0,
                                    key=f"specialite_{id_etudiant}",
                                    label_visibility="collapsed"
                                )
                                new_specialite_id = specialite_options[new_specialite]
                                
                                # Charger les niveaux
                                cursor.execute("SELECT id, nom FROM niveaux ORDER BY nom")
                                niveaux_all = cursor.fetchall()
                                niveau_options = {nom: id for id, nom in niveaux_all}
                                
                                current_niveau = niveau if niveau else list(niveau_options.keys())[0] if niveau_options else None
                                
                                if current_niveau and current_niveau in niveau_options:
                                    niveau_index = list(niveau_options.keys()).index(current_niveau)
                                else:
                                    niveau_index = 0
                                
                                st.markdown('<div class="form-label-etudiant">Niveau</div>', unsafe_allow_html=True)
                                new_niveau = st.selectbox(
                                    "",
                                    list(niveau_options.keys()),
                                    index=niveau_index if niveau_index < len(niveau_options.keys()) else 0,
                                    key=f"niveau_{id_etudiant}",
                                    label_visibility="collapsed"
                                )
                                new_niveau_id = niveau_options[new_niveau]
                                
                                col_annee_edit, col_promo_edit = st.columns(2)
                                with col_annee_edit:
                                    st.markdown('<div class="form-label-etudiant">Année d\'étude</div>', unsafe_allow_html=True)
                                    new_annee_etude = st.number_input("", 
                                                                    value=annee_etude, 
                                                                    min_value=1, 
                                                                    max_value=5,
                                                                    key=f"annee_etude_{id_etudiant}",
                                                                    label_visibility="collapsed")
                                
                                with col_promo_edit:
                                    st.markdown('<div class="form-label-etudiant">Promotion</div>', unsafe_allow_html=True)
                                    new_promo = st.number_input("", 
                                                              value=promo,
                                                              key=f"promo_{id_etudiant}",
                                                              label_visibility="collapsed")
                                
                                st.markdown("---")
                                col_submit_edit, col_cancel_edit = st.columns(2)
                                
                                with col_submit_edit:
                                    if st.form_submit_button("💾 SAUVEGARDER LES MODIFICATIONS",
                                                           type="primary",
                                                           use_container_width=True):
                                        try:
                                            cursor.execute("""
                                                UPDATE etudiants 
                                                SET nom = %s, prenom = %s, email = %s, 
                                                    specialite_id = %s, niveau_courant_id = %s,
                                                    annee_etude = %s, promo = %s
                                                WHERE id = %s
                                            """, (new_nom, new_prenom, new_email if new_email else None, 
                                                  new_specialite_id, new_niveau_id, new_annee_etude, 
                                                  new_promo, id_etudiant))
                                            conn.commit()
                                            st.success(" Étudiant modifié avec succès!")
                                            st.session_state['edit_mode'][f'etudiant_{id_etudiant}'] = False
                                            time_module.sleep(1)
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Erreur: {e}")
                                
                                with col_cancel_edit:
                                    if st.form_submit_button("❌ ANNULER",
                                                           type="secondary",
                                                           use_container_width=True):
                                        st.session_state['edit_mode'][f'etudiant_{id_etudiant}'] = False
                                        st.rerun()
                        
                        # Section suppression
                        if st.session_state['delete_mode'].get(f'etudiant_{id_etudiant}', False):
                            st.markdown("---")
                            st.markdown(f"""
                            <div class="alert-etudiant">
                                <h3 style="color: #dc2626; margin-top: 0;">⚠️ Confirmer la suppression</h3>
                                <p>Êtes-vous sûr de vouloir supprimer l'étudiant <strong>{prenom} {nom}</strong> ?</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            cursor.execute("SELECT COUNT(*) FROM inscriptions WHERE etudiant_id = %s", (id_etudiant,))
                            count_inscriptions = cursor.fetchone()[0]
                            
                            if count_inscriptions > 0:
                                st.error(f"❌ Cet étudiant est inscrit à {count_inscriptions} module(s).")
                                st.info("💡 Solution: Désinscrivez d'abord l'étudiant de ses modules.")
                            
                            col_confirm, col_cancel = st.columns(2)
                            with col_confirm:
                                if st.button(" OUI, SUPPRIMER",
                                           key=f"confirm_del_{id_etudiant}",
                                           type="primary",
                                           use_container_width=True):
                                    if count_inscriptions == 0:
                                        try:
                                            cursor.execute("DELETE FROM etudiants WHERE id = %s", (id_etudiant,))
                                            conn.commit()
                                            st.success(" Étudiant supprimé avec succès!")
                                            st.session_state['delete_mode'][f'etudiant_{id_etudiant}'] = False
                                            time_module.sleep(1)
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"❌ Erreur: {e}")
                                    else:
                                        st.error("❌ Impossible de supprimer. Résolvez d'abord les dépendances.")
                            
                            with col_cancel:
                                if st.button("❌ NON, ANNULER",
                                           key=f"cancel_del_{id_etudiant}",
                                           type="secondary",
                                           use_container_width=True):
                                    st.session_state['delete_mode'][f'etudiant_{id_etudiant}'] = False
                                    st.rerun()
                
                # Option pour afficher en tableau
                st.markdown("---")
                if st.button(" AFFICHER EN TABLEAU", use_container_width=True):
                    df = pd.DataFrame(etudiants_filtres, 
                                    columns=['ID', 'Nom', 'Prénom', 'Email', 'Promotion', 
                                             'Spécialité', 'Niveau', 'Année Étude', 'Modules'])
                    st.dataframe(df, use_container_width=True)
            
            else:
                st.info(" Aucun étudiant enregistré dans la base de données.")
                
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
    
    with tab3:
  
        st.markdown('<div class="section-header">', unsafe_allow_html=True)
        st.markdown("###  Gestion des comptes étudiants")
        st.markdown("Créez des comptes d'accès pour les étudiants")
        st.markdown('</div>', unsafe_allow_html=True)
        
        try:
            cursor = conn.cursor()
            
            # Récupérer tous les étudiants avec statut compte
            cursor.execute("""
                SELECT e.id, e.nom, e.prenom, e.email, e.promo,
                       s.nom as specialite, n.nom as niveau, e.annee_etude,
                       CASE 
                           WHEN u.id IS NULL THEN '❌ Sans compte'
                           ELSE ' Compte existant'
                       END as statut_compte,
                       u.username as username
                FROM etudiants e
                LEFT JOIN specialites s ON e.specialite_id = s.id
                LEFT JOIN niveaux n ON e.niveau_courant_id = n.id
                LEFT JOIN utilisateurs u ON e.utilisateur_id = u.id
                ORDER BY e.nom, e.prenom
            """)
            
            etudiants_comptes = cursor.fetchall()
            
            if not etudiants_comptes:
                st.info("Aucun étudiant trouvé dans la base de données")
                conn.close()
                return
            
            # Diviser en deux colonnes pour les statistiques
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                total_etudiants = len(etudiants_comptes)
                st.metric("Total étudiants", total_etudiants)
            
            with col_stat2:
                sans_compte = len([e for e in etudiants_comptes if e[8] == '❌ Sans compte'])
                st.metric("Sans compte", sans_compte, delta=f"{sans_compte/total_etudiants*100:.1f}%")
            
            with col_stat3:
                avec_compte = len([e for e in etudiants_comptes if e[8] == '✅ Compte existant'])
                st.metric("Avec compte", avec_compte, delta=f"{avec_compte/total_etudiants*100:.1f}%")
            
            # BARRE DE RECHERCHE
            st.markdown("---")
            col_search1, col_search2 = st.columns([3, 1])
            
            with col_search1:
                search_term = st.text_input(
                    " Rechercher un étudiant", 
                    placeholder="Nom, prénom, email, spécialité...",
                    key="search_etudiants_comptes"
                )
            
            with col_search2:
                filter_compte = st.selectbox(
                    "Filtrer par statut",
                    ["Tous", "Sans compte", "Avec compte"],
                    key="filter_compte_etudiants"
                )
            
            # Filtrer les résultats
            etudiants_filtres = etudiants_comptes
            
            if search_term:
                search_lower = search_term.lower()
                etudiants_filtres = [
                    e for e in etudiants_filtres
                    if (search_lower in str(e[1]).lower() or  # nom
                        search_lower in str(e[2]).lower() or  # prénom
                        search_lower in str(e[3]).lower() or  # email
                        search_lower in str(e[5]).lower() or  # spécialité
                        search_lower in str(e[6]).lower())    # niveau
                ]
            
            if filter_compte == "Sans compte":
                etudiants_filtres = [e for e in etudiants_filtres if e[8] == '❌ Sans compte']
            elif filter_compte == "Avec compte":
                etudiants_filtres = [e for e in etudiants_filtres if e[8] == '✅ Compte existant']
            
            # Afficher les résultats
            st.markdown(f"###  Résultats ({len(etudiants_filtres)} étudiants)")
            
            if not etudiants_filtres:
                st.info("Aucun étudiant trouvé avec ces critères")
            else:
                # Créer des onglets pour l'affichage
                tab_affichage1, tab_affichage2 = st.tabs(["Liste détaillée", "Tableau rapide"])
                
                with tab_affichage1:
                    # Afficher d'abord les étudiants sans compte
                    etudiants_sans_compte = [e for e in etudiants_filtres if e[8] == '❌ Sans compte']
                    
                    if etudiants_sans_compte:
                        st.markdown(f"####  Étudiants sans compte ({len(etudiants_sans_compte)})")
                        st.markdown('<div class="warning-box">Ces étudiants ne peuvent pas se connecter au système</div>', unsafe_allow_html=True)
                        
                        for etudiant in etudiants_sans_compte:
                            id_etudiant, nom, prenom, email, promo, specialite, niveau, annee_etude, statut, username = etudiant
                            
                            with st.expander(f"❌ {prenom} {nom} - {specialite} ({niveau})", expanded=True):
                                col_info1, col_info2 = st.columns([2, 1])
                                
                                with col_info1:
                                    st.markdown(f"**ID:** {id_etudiant}")
                                    st.markdown(f"**Nom complet:** {prenom} {nom}")
                                    st.markdown(f"**Email:** {email if email else 'Non renseigné'}")
                                    st.markdown(f"**Promotion:** {promo}")
                                    st.markdown(f"**Spécialité:** {specialite}")
                                    st.markdown(f"**Niveau:** {niveau} (Année {annee_etude})")
                                
                                with col_info2:
                                    # Formulaire de création de compte
                                    with st.form(f"creer_compte_{id_etudiant}"):
                                        username_default = f"{prenom.lower()}.{nom.lower().replace(' ', '_').replace('-', '_')}"
                                        username_default = username_default[:20]  # Limiter la longueur
                                        
                                        username_input = st.text_input(
                                            "Nom d'utilisateur *",
                                            value=username_default,
                                            key=f"username_{id_etudiant}",
                                            help="Sans espaces, minuscules recommandé"
                                        )
                                        
                                        password = st.text_input(
                                            "Mot de passe *",
                                            type="password",
                                            value="etudiant123",
                                            key=f"password_{id_etudiant}",
                                            help="Mot de passe par défaut: etudiant123"
                                        )
                                        
                                        confirm_password = st.text_input(
                                            "Confirmer le mot de passe *",
                                            type="password",
                                            value="etudiant123",
                                            key=f"confirm_{id_etudiant}"
                                        )
                                        
                                        col_btn1, col_btn2 = st.columns(2)
                                        with col_btn1:
                                            if st.form_submit_button(" Créer le compte", use_container_width=True):
                                                if not username_input:
                                                    st.error("Le nom d'utilisateur est obligatoire")
                                                elif not password:
                                                    st.error("Le mot de passe est obligatoire")
                                                elif password != confirm_password:
                                                    st.error("Les mots de passe ne correspondent pas")
                                                else:
                                                    success, message = creer_compte_etudiant(
                                                        conn, id_etudiant, username_input, password
                                                    )
                                                    
                                                    if success:
                                                        st.success(f"{message}")
                                                        time_module.sleep(2)
                                                        st.rerun()
                                                    else:
                                                        st.error(f"❌ {message}")
                                        
                                        with col_btn2:
                                            if st.form_submit_button(" Réinitialiser", use_container_width=True, type="secondary"):
                                                st.rerun()
                    
                    # Afficher les étudiants avec compte
                    etudiants_avec_compte = [e for e in etudiants_filtres if e[8] == ' Compte existant']
                    
                    if etudiants_avec_compte:
                        st.markdown(f"####  Étudiants avec compte ({len(etudiants_avec_compte)})")
                        
                        for etudiant in etudiants_avec_compte:
                            id_etudiant, nom, prenom, email, promo, specialite, niveau, annee_etude, statut, username = etudiant
                            
                            # Récupérer le mot de passe en clair
                            plain_password = get_plain_password(conn, username)
                            
                            with st.expander(f"✅ {prenom} {nom} - {specialite}", expanded=False):
                                col_info1, col_info2 = st.columns([2, 1])
                                
                                with col_info1:   
                                    st.markdown(f"**ID:** {id_etudiant}")
                                    st.markdown(f"**Nom complet:** {prenom} {nom}")
                                    st.markdown(f"**Nom d'utilisateur:** `{username}`")
                                    if plain_password:
                                        st.markdown(f"**Mot de passe:** `{plain_password}`")
                                    else:
                                        st.markdown("**Mot de passe:** `(non disponible)`")
                                    
                                    # Afficher les identifiants dans une zone de code         
                                    if plain_password:
                                        credentials = f"Username: {username}\nPassword: {plain_password}"
                                        st.code(credentials, language="text")
                                    
                                    st.markdown(f"**Email:** {email if email else 'Non renseigné'}")
                                
                                with col_info2:
                                    st.success("✅ Compte actif")
                                    
                                    # Bouton pour copier les identifiants
                                    if plain_password:
                                        credentials_display = f"Username: {username}\nPassword: {plain_password}"
                                        if st.button(" Copier identifiants", key=f"copy_{id_etudiant}", use_container_width=True):
                                            st.code(credentials_display)
                                            st.info("Identifiants copiés! (Coller avec Ctrl+V)")
                                    
                                    # Option pour réinitialiser le mot de passe
                                    if st.button(" Changer mot de passe", key=f"change_pass_{id_etudiant}", use_container_width=True):
                                        st.session_state[f'show_change_pass_{id_etudiant}'] = True
                                    
                                    # Formulaire pour changer le mot de passe
                                    if st.session_state.get(f'show_change_pass_{id_etudiant}', False):
                                        with st.form(f"change_password_{id_etudiant}"):
                                            new_password = st.text_input(
                                                "Nouveau mot de passe *",
                                                type="password",
                                                key=f"new_pass_{id_etudiant}"
                                            )
                                            
                                            confirm_password = st.text_input(
                                                "Confirmer le mot de passe *",
                                                type="password",
                                                key=f"confirm_new_pass_{id_etudiant}"
                                            )
                                            
                                            col_submit, col_cancel = st.columns(2)
                                            with col_submit:
                                                if st.form_submit_button(" Enregistrer", use_container_width=True, type="secondry"):
                                                    if new_password and new_password == confirm_password:
                                                        # Récupérer l'ID utilisateur
                                                        cursor.execute("SELECT id FROM utilisateurs WHERE username = %s", (username,))
                                                        user_id_result = cursor.fetchone()
                                                        if user_id_result:
                                                            user_id = user_id_result[0]
                                                            success, message =changer_mot_de_passe_etudiant(
                conn, id_etudiant, username, new_password  # Utilisez id_etudiant ici
            )
                                                            if success:
                                                                st.success(" Mot de passe changé avec succès!")
                                                                time_module.sleep(2)
                                                                st.rerun()
                                                            else:
                                                                st.error(f"❌ {message}")
                                                        else:
                                                            st.error("Utilisateur non trouvé")
                                                    else:
                                                        st.error("Les mots de passe ne correspondent pas ou sont vides")
                                            
                                            with col_cancel:
                                                if st.form_submit_button("❌ Annuler", use_container_width=True):
                                                    st.session_state[f'show_change_pass_{id_etudiant}'] = False
                                                    st.rerun()
                
                with tab_affichage2:
                    # Créer un tableau simple
                    table_data = []
                    for etudiant in etudiants_filtres:
                        id_etudiant, nom, prenom, email, promo, specialite, niveau, annee_etude, statut, username = etudiant
                        plain_password = get_plain_password(conn, username) if username else None
                        
                        table_data.append({
                            'ID': id_etudiant,
                            'Nom': nom,
                            'Prénom': prenom,
                            'Username': username or 'N/A',
                            'Password': plain_password or 'N/A',
                            'Email': email or 'N/A',
                            'Spécialité': specialite,
                            'Niveau': niveau,
                            'Statut': statut
                        })
                    
                    df_table = pd.DataFrame(table_data)
                    st.dataframe(df_table, use_container_width=True)
                    
                    # Option pour exporter
                    if st.button("📥 Exporter en CSV", use_container_width=True):
                        csv = df_table.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="Télécharger CSV",
                            data=csv,
                            file_name="etudiants_comptes.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
        
        except Exception as e:
            st.error(f" Erreur: {e}")
    
    conn.close()
def page_gestion_modules():
    """Page de gestion des modules"""
    set_page_background('dashboard')
    
    st.markdown("""
    <style>
    /* ============================================
       STYLES SPÉCIFIQUES GESTION MODULES
       ============================================ */
    
    /* Header principal */
    .module-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .module-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" fill-opacity="1" d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,144C672,139,768,181,864,186.7C960,192,1056,160,1152,144C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
        background-size: cover;
        opacity: 0.3;
    }
    
    .module-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #e0f2fe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
    }
    
    .module-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }
    
    /* Cartes module améliorées */
    .module-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .module-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        border-color: #bae6fd;
    }
    
    .module-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #0ea5e9 0%, #3b82f6 100%);
        border-radius: 20px 0 0 20px;
    }
    
    /* Badges spéciaux */
    .credits-badge {
        display: inline-block;
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(14, 165, 233, 0.2);
    }
    
    .code-badge {
        display: inline-block;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(139, 92, 246, 0.2);
    }
    
    .specialite-badge {
        display: inline-block;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.2);
    }
    
    .prof-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(245, 158, 11, 0.2);
    }
    
    /* Boutons améliorés */
    .btn-module-modify {
        background: linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3) !important;
    }
    
    .btn-module-modify:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.4) !important;
    }
    
    .btn-module-delete {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    .btn-module-delete:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
    }
    
    /* Formulaire amélioré */
    .form-container-module {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 35px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .form-label-module {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 8px;
        display: block;
        font-size: 1rem;
    }
    
    /* Statistiques améliorées */
    .stat-card-module {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(240, 249, 255, 0.9) 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    
    .stat-card-module:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value-module {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .stat-label-module {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Onglets améliorés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 15px 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(14, 165, 233, 0.3);
    }
    
    /* Zone de recherche améliorée */
    .search-box-module {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Bouton d'action principal */
    .btn-primary-module {
        background: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 16px 32px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(14, 165, 233, 0.3) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .btn-primary-module:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.4) !important;
        background: linear-gradient(135deg, #0284c7 0%, #1d4ed8 100%) !important;
    }
    
    /* Bouton secondaire */
    .btn-secondary-module {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        color: #64748b !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .btn-secondary-module:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #475569 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Message d'alerte amélioré */
    .alert-module {
        background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
        border-left: 6px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
    }
    
    /* Card info module */
    .info-card-module {
        background: linear-gradient(135deg, rgba(240, 249, 255, 0.9) 0%, rgba(224, 242, 254, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Animation d'entrée */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .module-header {
            padding: 25px 20px;
        }
        
        .module-header h1 {
            font-size: 2.2rem;
        }
        
        .module-card {
            padding: 20px;
        }
        
        .stat-value-module {
            font-size: 2.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="module-header fade-in-up">
        <h1>📚Gestion modules </h1>
        <p>Ajouter, modifier et gérer les modules de formation</p>
        <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
            <i class="fas fa-book" style="margin-right: 5px;">gérer les modules de cours</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    if user_info['role'] not in ['Vice-doyen', 'Admin_examens']:
        st.error("Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité")
        return
    
    conn = get_db()
    if not conn:
        st.error("Impossible de se connecter à la base de données")
        return
    
    # Onglets avec style amélioré
    tab1, tab2 = st.tabs([" Ajouter un module", " Liste des modules"])
    
    with tab1:
        st.markdown("###  Ajouter un nouveau module")
        st.markdown("Remplissez le formulaire pour ajouter un nouveau module à la base de données.")
        
        with st.form("ajout_module", clear_on_submit=True):
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="form-label-module">Code du module *</div>', unsafe_allow_html=True)
                code = st.text_input("", placeholder="Ex: MAT101", label_visibility="collapsed")
                
                st.markdown('<div class="form-label-module">Nom du module *</div>', unsafe_allow_html=True)
                nom = st.text_input("", placeholder="Ex: Mathématiques Appliquées", label_visibility="collapsed")
            
            with col2:
                st.markdown('<div class="form-label-module">Crédits *</div>', unsafe_allow_html=True)
                credits = st.number_input("", min_value=3, max_value=12, value=6, label_visibility="collapsed")
                
                st.markdown('<div class="form-label-module">Volume horaire</div>', unsafe_allow_html=True)
                volume_horaire = st.number_input("", min_value=0, value=30, label_visibility="collapsed")
            
            # Champs supplémentaires
            col3, col4 = st.columns(2)
            with col3:
                st.markdown('<div class="form-label-module">Semestre</div>', unsafe_allow_html=True)
                semestre = st.selectbox("", [1, 2], index=0, label_visibility="collapsed")
                
                st.markdown('<div class="form-label-module">Année d\'étude</div>', unsafe_allow_html=True)
                annee_etude = st.text_input("", placeholder="Ex: L1, M1", label_visibility="collapsed")
            
            with col4:
                try:
                    cursor = conn.cursor()
                    
                    # Sélection de la spécialité (au lieu de la formation)
                    cursor.execute("""
                        SELECT s.id, s.nom, f.nom as formation_nom 
                        FROM specialites s 
                        LEFT JOIN formations f ON s.formation_id = f.id 
                        ORDER BY s.nom
                    """)
                    specialites = cursor.fetchall()
                    
                    if specialites:
                        st.markdown('<div class="form-label-module">Spécialité *</div>', unsafe_allow_html=True)
                        specialite_options = {f"{nom} ({formation_nom})": id for id, nom, formation_nom in specialites}
                        specialite = st.selectbox("", list(specialite_options.keys()), label_visibility="collapsed")
                        specialite_id = specialite_options[specialite]
                    else:
                        st.error(" Aucune spécialité disponible. Créez d'abord une spécialité.")
                        specialite_id = None
                    
                    # Sélection du professeur
                    cursor.execute("SELECT id, nom, prenom FROM professeurs ORDER BY nom")
                    professeurs = cursor.fetchall()
                    
                    if professeurs:
                        st.markdown('<div class="form-label-module">Professeur responsable *</div>', unsafe_allow_html=True)
                        prof_options = {f"{prenom} {nom}": id for id, nom, prenom in professeurs}
                        prof = st.selectbox("", list(prof_options.keys()), label_visibility="collapsed")
                        prof_id = prof_options[prof]
                    else:
                        st.error("❌ Aucun professeur disponible. Créez d'abord un professeur.")
                        prof_id = None
                        
                    # Sélection du pré-requis (optionnel)
                    cursor.execute("SELECT id, code_module, nom FROM modules ORDER BY code_module")
                    modules_existants = cursor.fetchall()
                    
                    if modules_existants:
                        st.markdown('<div class="form-label-module">Pré-requis (optionnel)</div>', unsafe_allow_html=True)
                        prerequis_options = {"Aucun": None}
                        prerequis_options.update({f"{code} - {nom}": id for id, code, nom in modules_existants})
                        
                        prerequis = st.selectbox("", list(prerequis_options.keys()), 
                                               index=0, label_visibility="collapsed")
                        pre_requis_id = prerequis_options[prerequis]
                    
                except Exception as e:
                    st.error(f"❌ Erreur: {e}")
                    specialite_id = None
                    prof_id = None
                    pre_requis_id = None
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.form_submit_button("Ajouter le module", use_container_width=True):
                    if code and nom and specialite_id and prof_id:
                        try:
                            cursor = conn.cursor()
                            cursor.execute(
                                """
                                INSERT INTO modules 
                                (code_module, nom, credits, prof_responsable_id, specialite_id, 
                                 semestre, volume_horaire, annee_etude, pre_requis_id) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                                """,
                                (code, nom, credits, prof_id, specialite_id, 
                                 semestre, volume_horaire, annee_etude if annee_etude else None, 
                                 pre_requis_id)
                            )
                            conn.commit()
                            st.success(f"✅ Module '{nom}' ajouté avec succès")
                            time_module.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Erreur: {e}")
                    else:
                        st.error("⚠️ Les champs marqués d'une * sont obligatoires")
    
    with tab2:
        st.markdown("###  Liste des modules")
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT m.id, m.code_module, m.nom, m.credits, 
                       COALESCE(s.nom, 'Non spécifié') as specialite_nom,
                       COALESCE(f.nom, 'Non spécifié') as formation_nom,
                       p.nom as prof_nom, p.prenom as prof_prenom,
                       m.semestre, m.volume_horaire, m.annee_etude
                FROM modules m
                LEFT JOIN specialites s ON m.specialite_id = s.id
                LEFT JOIN formations f ON s.formation_id = f.id
                LEFT JOIN professeurs p ON m.prof_responsable_id = p.id
                ORDER BY m.code_module
            """)
            
            modules = cursor.fetchall()
            
            if modules:
                # Statistiques
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                total_modules = len(modules)
                total_credits = sum([m[3] for m in modules])
                total_volume = sum([m[9] for m in modules if m[9]])
                
                cursor.execute("SELECT COUNT(DISTINCT s.id) FROM modules m JOIN specialites s ON m.specialite_id = s.id")
                specialites_count_result = cursor.fetchone()
                specialites_count = specialites_count_result[0] if specialites_count_result else 0
                
                with col_stat1:
              
                    st.markdown(f'<div class="stat-value-module">{total_modules}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-module">TOTAL MODULES</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_stat2:
                    
                    st.markdown(f'<div class="stat-value-module">{total_credits}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-module">CRÉDITS TOTAUX</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_stat3:
                    
                    st.markdown(f'<div class="stat-value-module">{total_volume}h</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-module">VOLUME HEURES</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_stat4:
                    
                    st.markdown(f'<div class="stat-value-module">{specialites_count}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-module">SPÉCIALITÉS</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Zone de recherche
              
                search = st.text_input("🔍 Rechercher un module (code, nom, spécialité):", 
                                      placeholder="Entrez un terme de recherche...")
                st.markdown('</div>', unsafe_allow_html=True)
                
                if search:
                    modules_filtres = [
                        m for m in modules 
                        if search.lower() in str(m[1]).lower() or 
                        search.lower() in str(m[2]).lower() or 
                        search.lower() in str(m[4]).lower() or
                        search.lower() in str(m[5]).lower()
                    ]
                else:
                    modules_filtres = modules
                
                for module in modules_filtres:
                    id_module, code, nom_module, credits, specialite_nom, formation_nom, prof_nom, prof_prenom, semestre, volume_horaire, annee_etude = module
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        # Badge code
                        st.markdown(f'<span class="code-badge">{code}</span>', unsafe_allow_html=True)
                        
                        st.markdown(f'<h4 style="margin: 10px 0;">{nom_module}</h4>', unsafe_allow_html=True)
                        
                        # Badges d'information
                        col_badges1, col_badges2, col_badges3, col_badges4 = st.columns(4)
                        with col_badges1:
                            st.markdown(f'<span class="credits-badge">{credits} crédits</span>', unsafe_allow_html=True)
                        
                        with col_badges2:
                            st.markdown(f'<span class="specialite-badge">{specialite_nom}</span>', unsafe_allow_html=True)
                        
                        with col_badges3:
                            st.markdown(f'<span class="prof-badge">{prof_prenom} {prof_nom}</span>', unsafe_allow_html=True)
                        
                        with col_badges4:
                            semestre_color = "#163f82" if semestre == 1 else "#8b5cf6"
                            st.markdown(f'<span style="display: inline-block; background: {semestre_color}; color: white; padding: 6px 16px; border-radius: 25px; font-size: 0.85rem; font-weight: 600; margin: 5px 0; box-shadow: 0 3px 10px rgba(59, 130, 246, 0.2);">S{semestre}</span>', unsafe_allow_html=True)
                        
                        # Infos détaillées
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                            st.markdown('<div class="info-card-module">', unsafe_allow_html=True)
                            st.write(f"**ID:** {id_module}")
                            st.write(f"**Formation:** {formation_nom}")
                            st.write(f"**Professeur:** {prof_prenom} {prof_nom}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col_info2:
                            st.markdown('<div class="info-card-module">', unsafe_allow_html=True)
                            st.write(f"**Année:** {annee_etude if annee_etude else 'Non spécifiée'}")
                            st.write(f"**Volume horaire:** {volume_horaire}h" if volume_horaire else "**Volume horaire:** Non spécifié")
                            
                            cursor.execute("SELECT COUNT(*) FROM inscriptions WHERE module_id = %s", (id_module,))
                            count_inscriptions = cursor.fetchone()[0]
                            st.write(f"**Étudiants inscrits:** {count_inscriptions}")
                            
                            cursor.execute("SELECT COUNT(*) FROM examens WHERE module_id = %s", (id_module,))
                            count_examens = cursor.fetchone()[0]
                            st.write(f"**Examens programmés:** {count_examens}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("✏", key=f"edit_module_{id_module}", 
                                        help="Modifier ce module", 
                                        use_container_width=True):
                                st.session_state['edit_mode'][f'module_{id_module}'] = True
                        
                        with col_btn2:
                            if st.button("🗑", key=f"del_module_{id_module}", 
                                        help="Supprimer ce module", 
                                        type="secondary", use_container_width=True):
                                st.session_state['delete_mode'][f'module_{id_module}'] = True
                    
                    # Formulaire de modification
                    if st.session_state['edit_mode'].get(f'module_{id_module}', False):
                        st.markdown("---")
                        st.write("### ✏ Modifier le module")
                        
                        with st.form(f"modifier_module_{id_module}"):
                            col_m1, col_m2 = st.columns(2)
                            with col_m1:
                                new_code = st.text_input("Code", value=code, key=f"m_code_{id_module}")
                                new_nom = st.text_input("Nom", value=nom_module, key=f"m_nom_{id_module}")
                                new_credits = st.number_input("Crédits", value=credits, 
                                                             min_value=3, max_value=12, key=f"m_credits_{id_module}")
                                new_volume = st.number_input("Volume horaire", value=volume_horaire if volume_horaire else 30,
                                                           min_value=0, key=f"m_volume_{id_module}")
                            
                            with col_m2:
                                new_semestre = st.selectbox("Semestre", [1, 2], 
                                                          index=0 if semestre == 1 else 1,
                                                          key=f"m_semestre_{id_module}")
                                new_annee = st.text_input("Année d'étude", 
                                                        value=annee_etude if annee_etude else "",
                                                        key=f"m_annee_{id_module}")
                                
                                cursor.execute("""
                                    SELECT s.id, s.nom, f.nom as formation_nom 
                                    FROM specialites s 
                                    LEFT JOIN formations f ON s.formation_id = f.id 
                                    ORDER BY s.nom
                                """)
                                specialites_all = cursor.fetchall()
                                specialite_options = {f"{nom} ({formation_nom})": id for id, nom, formation_nom in specialites_all}
                                
                                current_specialite = f"{specialite_nom} ({formation_nom})"
                                if current_specialite in specialite_options:
                                    specialite_index = list(specialite_options.keys()).index(current_specialite)
                                else:
                                    specialite_index = 0
                                
                                new_specialite = st.selectbox(
                                    "Spécialité",
                                    list(specialite_options.keys()),
                                    index=specialite_index,
                                    key=f"m_specialite_{id_module}"
                                )
                                new_specialite_id = specialite_options[new_specialite]
                                
                                cursor.execute("SELECT id, nom, prenom FROM professeurs ORDER BY nom")
                                professeurs_all = cursor.fetchall()
                                prof_options = {f"{prenom} {nom}": id for id, nom, prenom in professeurs_all}
                                
                                current_prof = f"{prof_prenom} {prof_nom}"
                                if current_prof in prof_options:
                                    prof_index = list(prof_options.keys()).index(current_prof)
                                else:
                                    prof_index = 0
                                
                                new_prof = st.selectbox(
                                    "Professeur responsable",
                                    list(prof_options.keys()),
                                    index=prof_index,
                                    key=f"m_prof_{id_module}"
                                )
                                new_prof_id = prof_options[new_prof]
                            
                            # Pré-requis
                            cursor.execute("SELECT id, code_module, nom FROM modules WHERE id != %s ORDER BY code_module", (id_module,))
                            modules_existants = cursor.fetchall()
                            
                            if modules_existants:
                                cursor.execute("SELECT pre_requis_id FROM modules WHERE id = %s", (id_module,))
                                current_prerequis = cursor.fetchone()
                                current_prerequis_id = current_prerequis[0] if current_prerequis else None
                                
                                prerequis_options = {"Aucun": None}
                                prerequis_options.update({f"{code} - {nom}": id for id, code, nom in modules_existants})
                                
                                # Trouver l'index du pré-requis actuel
                                if current_prerequis_id:
                                    for name, mid in prerequis_options.items():
                                        if mid == current_prerequis_id:
                                            current_prerequis_name = name
                                            break
                                    else:
                                        current_prerequis_name = "Aucun"
                                else:
                                    current_prerequis_name = "Aucun"
                                
                                prerequis_list = list(prerequis_options.keys())
                                prerequis_index = prerequis_list.index(current_prerequis_name) if current_prerequis_name in prerequis_list else 0
                                
                                new_prerequis = st.selectbox(
                                    "Pré-requis",
                                    prerequis_list,
                                    index=prerequis_index,
                                    key=f"m_prerequis_{id_module}"
                                )
                                new_pre_requis_id = prerequis_options[new_prerequis]
                            
                            col_btn_a, col_btn_b, _ = st.columns([1, 1, 2])
                            with col_btn_a:
                                if st.form_submit_button("💾 Sauvegarder", use_container_width=True):
                                    try:
                                        cursor.execute("""
                                            UPDATE modules 
                                            SET code_module = %s, nom = %s, credits = %s, 
                                                prof_responsable_id = %s, specialite_id = %s,
                                                semestre = %s, volume_horaire = %s, 
                                                annee_etude = %s, pre_requis_id = %s
                                            WHERE id = %s
                                        """, (new_code, new_nom, new_credits, 
                                              new_prof_id, new_specialite_id,
                                              new_semestre, new_volume,
                                              new_annee if new_annee else None,
                                              new_pre_requis_id, id_module))
                                        conn.commit()
                                        st.success("✅ Module modifié avec succès!")
                                        st.session_state['edit_mode'][f'module_{id_module}'] = False
                                        time_module.sleep(1)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Erreur: {e}")
                            
                            with col_btn_b:
                                if st.form_submit_button("❌ Annuler", use_container_width=True):
                                    st.session_state['edit_mode'][f'module_{id_module}'] = False
                                    st.rerun()
                    
                    # Confirmation suppression
                    if st.session_state['delete_mode'].get(f'module_{id_module}', False):
                        st.markdown("---")
                        st.markdown('<div class="alert-module">', unsafe_allow_html=True)
                        st.warning(f"⚠ Confirmer la suppression du module **'{nom_module}'**?")
                        
                        cursor.execute("SELECT COUNT(*) FROM inscriptions WHERE module_id = %s", (id_module,))
                        count_inscriptions = cursor.fetchone()[0]
                        
                        cursor.execute("SELECT COUNT(*) FROM examens WHERE module_id = %s", (id_module,))
                        count_examens = cursor.fetchone()[0]
                        
                        if count_inscriptions > 0 or count_examens > 0:
                            st.error(f"❌ Attention! Ce module est lié à :")
                            if count_inscriptions > 0:
                                st.error(f"- **{count_inscriptions} étudiant(s)** inscrit(s)")
                            if count_examens > 0:
                                st.error(f"- **{count_examens} examen(s)** programmé(s)")
                            st.info("💡 Solution: Désinscrivez les étudiants et supprimez les examens avant.")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        col_x, col_y, _ = st.columns([1, 1, 2])
                        with col_x:
                            if st.button("✅ Oui, supprimer", key=f"confirm_del_module_{id_module}", 
                                        use_container_width=True, type="primary"):
                                if count_inscriptions == 0 and count_examens == 0:
                                    try:
                                        cursor.execute("DELETE FROM modules WHERE id = %s", (id_module,))
                                        conn.commit()
                                        st.success("✅ Module supprimé avec succès!")
                                        st.session_state['delete_mode'][f'module_{id_module}'] = False
                                        time_module.sleep(1)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Erreur: {e}")
                                else:
                                    st.error("❌ Impossible de supprimer. Résolvez d'abord les dépendances.")
                        
                        with col_y:
                            if st.button("❌ Non, annuler", key=f"cancel_del_module_{id_module}", 
                                        use_container_width=True):
                                st.session_state['delete_mode'][f'module_{id_module}'] = False
                                st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                col_view1, col_view2 = st.columns([1, 1])
                with col_view1:
                    if st.button(" Afficher vue tableau", use_container_width=True):
                        df = pd.DataFrame(modules_filtres, columns=[
                            'ID', 'Code', 'Nom', 'Crédits', 'Spécialité', 'Formation', 
                            'Prof Nom', 'Prof Prénom', 'Semestre', 'Volume Horaire', 'Année'
                        ])
                        st.dataframe(df, use_container_width=True)
                with col_view2:
                    if st.button(" Actualiser la liste", use_container_width=True):
                        st.rerun()
            
            else:
                st.info("ℹ Aucun module enregistré")
                
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
    
    conn.close()
# ============================================
# STYLES CSS SPÉCIFIQUES POUR CETTE PAGE
# ============================================
# ============================================
# STYLES CSS SPÉCIFIQUES POUR CETTE PAGE
# ============================================

st.markdown("""
<style>
/* ============================================
   STYLES SPÉCIFIQUES GESTION ÉTUDIANTS
   ============================================ */

/* Header principal */
.etudiant-header {
    background: linear-gradient(135deg, rgba(21, 94, 117, 0.9) 0%, rgba(29, 78, 216, 0.9) 100%);
    border-radius: 20px;
    padding: 35px;
    margin-bottom: 35px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
}

.etudiant-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" fill-opacity="1" d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,144C672,139,768,181,864,186.7C960,192,1056,160,1152,144C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
    background-size: cover;
    opacity: 0.3;
}

.etudiant-header h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 15px;
    background: linear-gradient(135deg, #ffffff 0%, #dbeafe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}

.etudiant-header p {
    font-size: 1.3rem;
    opacity: 0.9;
    margin-top: 10px;
    position: relative;
    z-index: 1;
}

/* Cartes étudiant améliorées */
.etudiant-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(226, 232, 240, 0.8);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.etudiant-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    border-color: #c7d2fe;
}

.etudiant-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 20px 0 0 20px;
}

/* Badges spéciaux */
.specialite-badge {
    display: inline-block;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(59, 130, 246, 0.2);
}

.niveau-badge {
    display: inline-block;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(16, 185, 129, 0.2);
}

.promo-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(245, 158, 11, 0.2);
}

/* Boutons améliorés */
.btn-etudiant-modify {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
}

.btn-etudiant-modify:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
}

.btn-etudiant-delete {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
}

.btn-etudiant-delete:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
}

/* Formulaire amélioré */
.form-container-etudiant {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 35px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(226, 232, 240, 0.8);
}

.form-label-etudiant {
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 8px;
    display: block;
    font-size: 1rem;
}

/* Statistiques améliorées */
.stat-card-etudiant {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(226, 232, 240, 0.8);
    transition: all 0.3s ease;
}

.stat-card-etudiant:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.stat-value-etudiant {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
}

.stat-label-etudiant {
    font-size: 0.95rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Onglets améliorés */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.1);
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 15px 25px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.15);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
}

/* Zone de recherche améliorée */
.search-box-etudiant {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(226, 232, 240, 0.8);
}

/* Bouton d'action principal */
.btn-primary-etudiant {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 16px 32px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
    width: 100% !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.btn-primary-etudiant:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4) !important;
    background: linear-gradient(135deg, #0da271 0%, #047857 100%) !important;
}

/* Bouton secondaire */
.btn-secondary-etudiant {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    color: #64748b !important;
    font-weight: 600 !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.btn-secondary-etudiant:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    color: #475569 !important;
    transform: translateY(-2px) !important;
}

/* Message d'alerte amélioré */
.alert-etudiant {
    background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
    border-left: 6px solid #ef4444;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
}

/* Card info étudiant */
.info-card-etudiant {
    background: linear-gradient(135deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.9) 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(226, 232, 240, 0.8);
}

/* Animation d'entrée */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
    .etudiant-header {
        padding: 25px 20px;
    }
    
    .etudiant-header h1 {
        font-size: 2.2rem;
    }
    
    .etudiant-card {
        padding: 20px;
    }
    
    .stat-value-etudiant {
        font-size: 2.2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ============================================
# FONCTIONS DE CONNEXION ET UTILITAIRES
# ============================================
def get_all_formations():
    """Récupère toutes les formations avec leurs départements"""
    query = """
    SELECT 
        f.id,
        f.nom,
        d.nom as departement,  -- Ajouter cette ligne
        f.code_formation,
        f.nb_modules,          -- Ajouter cette ligne
        f.created_at::date as date_creation  -- Ajouter cette ligne
    FROM formations f
    JOIN departements d ON f.dept_id = d.id  -- Ajouter le JOIN
    ORDER BY f.nom
    """
    return execute_query(query)

def get_all_departements():
    """Récupère tous les départements"""
    query = "SELECT id, nom FROM departements ORDER BY nom"
    return execute_query(query)

def add_formation(nom, dept_id, code_formation, nb_modules):
    """Ajoute une nouvelle formation"""
    query = """
    INSERT INTO formations (nom, dept_id, code_formation, nb_modules)
    VALUES (%s, %s, %s, %s)
    RETURNING id
    """
    conn = get_db()
    if conn is None:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, (nom, dept_id, code_formation, nb_modules))
            result = cur.fetchone()
            conn.commit()
            return result is not None
    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def update_formation(formation_id, nom, dept_id, code_formation, nb_modules):
    """Met à jour une formation"""
    query = """
    UPDATE formations 
    SET nom = %s, dept_id = %s, code_formation = %s, nb_modules = %s
    WHERE id = %s
    """
    return execute_query(query, (nom, dept_id, code_formation, nb_modules, formation_id), fetch=False)

def delete_formation(formation_id):
    """Supprime une formation"""
    return execute_query("DELETE FROM formations WHERE id = %s", (formation_id,), fetch=False)

def get_formation_by_id(formation_id):
    """Récupère une formation par son ID"""
    query = """
    SELECT 
        f.id,
        f.nom,
        f.dept_id,
        f.code_formation,
        f.nb_modules
    FROM formations f
    WHERE f.id = %s
    """
    return execute_query(query, (formation_id,))

# ==================== PAGE DE GESTION DES FORMATIONS ====================
def page_gestion_formations():
    set_page_background('dashboard')
    """Page de gestion des formations"""
    st.markdown("""
    <div class="etudiant-header fade-in-up">
        <h1>Gestion des Formations</h1>
        <p>Ajouter, modifier et gérer les formations universitaires</p>
        <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
            <i class="fas fa-users" style="margin-right: 5px;"></i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Créer 4 onglets distincts
    tab1, tab2, tab3, tab4 = st.tabs([
        "Liste des Formations", 
        "Ajouter Formation", 
        "Modifier Formation",
        "Supprimer Formation"
    ])
    
    # Onglet 1: Liste des formations
    with tab1:
        st.header("Liste des Formations")
        formations = get_all_formations()
        
        if formations is not None:
            # DEBUG: Afficher les colonnes
            # st.write("DEBUG - Colonnes disponibles:", formations.columns.tolist())
            
            if not formations.empty:
                # Afficher le tableau
                st.dataframe(formations, use_container_width=True, hide_index=True)
                
                # Statistiques SIMPLES
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Formations", len(formations))
                with col2:
                    st.metric("Formations actives", len(formations))
                with col3:
                    # Compter les codes uniques
                    unique_codes = formations['code_formation'].nunique()
                    st.metric("Codes uniques", unique_codes)
                    
            else:
                st.info("Aucune formation enregistrée")
        else:
            st.error("Impossible de charger les formations")
    
    # Onglet 2: Ajouter une formation
    with tab2:
        st.header("Ajouter une Formation")
        
        # Récupérer les données nécessaires
        departements = get_all_departements()
        
        if departements is not None and not departements.empty:
            
            with st.form("form_ajouter_formation"):
                col1, col2 = st.columns(2)
                
                with col1:
                    nom = st.text_input("Nom de la formation*", placeholder="Licence Informatique")
                    
                    # Sélection du département
                    dept_options = departements['nom'].tolist()
                    selected_dept_idx = st.selectbox("Département*", range(len(dept_options)),
                                                    format_func=lambda x: dept_options[x])
                    dept_id = int(departements.iloc[selected_dept_idx]['id'])
                    
                    code_formation = st.text_input("Code formation*", placeholder="INFO-LIC")
                
                with col2:
                    nb_modules = st.number_input("Nombre de modules*", min_value=6, max_value=9, value=7)
                    
                    # Afficher quelques statistiques sur les départements
                    with st.expander("Informations sur les départements disponibles"):
                        st.write(f"**Total de départements:** {len(departements)}")
                        st.write("**Liste des départements:**")
                        for _, dept in departements.iterrows():
                            st.write(f"- {dept['nom']}")
                
                col_sub, col_reset = st.columns(2)
                
                with col_sub:
                    submitted = st.form_submit_button("Ajouter", type="primary", use_container_width=True)
                
                with col_reset:
                    reset = st.form_submit_button("Réinitialiser", use_container_width=True)
                
                if submitted:
                    if nom and code_formation:
                        result = add_formation(nom, dept_id, code_formation, nb_modules)
                        if result:
                            st.success(f"✅ Formation '{nom}' ajoutée avec succès!")
                            st.info("La formation a été enregistrée dans la base de données.")
                            import time
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de l'ajout de la formation")
                            st.info("Vérifiez que le code de formation n'existe pas déjà (doit être unique).")
                    else:
                        if not nom:
                            st.error("❌ Le nom de la formation est obligatoire")
                        if not code_formation:
                            st.error("❌ Le code de la formation est obligatoire")
                
                if reset:
                    st.rerun()
        else:
            st.error("❌ Données manquantes pour créer une formation")
            st.error("Aucun département disponible")
    
    # Onglet 3: Modifier une formation
    with tab3:
        st.header("Modifier une Formation")
        
        formations = get_all_formations()
        departements = get_all_departements()
        
        if formations is not None and not formations.empty and \
           departements is not None and not departements.empty:
            
            # Créer les options de sélection - UTILISER LES COLONNES DISPONIBLES
            selection_options = []
            formation_ids = []
            
            for idx, row in formations.iterrows():
                formation_id = row['id']
                formation_ids.append(formation_id)
                
                # Construire l'option avec les colonnes disponibles
                parts = []
                if 'nom' in formations.columns:
                    parts.append(str(row['nom']))
                if 'code_formation' in formations.columns:
                    parts.append(f"({str(row['code_formation'])})")
                
                option_text = " - ".join(parts)
                selection_options.append(option_text)
            
            selected_idx = st.selectbox(
                "Choisir une formation à modifier",
                range(len(selection_options)),
                format_func=lambda x: selection_options[x],
                key="edit_formation_select_unique"  # CLÉ UNIQUE
            )
            
            if selected_idx is not None:
                formation_id = formation_ids[selected_idx]
                formation_row = formations[formations['id'] == formation_id].iloc[0]
                
                # Récupérer les détails complets de la formation
                formation_details = get_formation_by_id(formation_id)
                
                if formation_details is not None and not formation_details.empty:
                    formation_details = formation_details.iloc[0]
                    
                    with st.form("form_modifier_formation"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            new_nom = st.text_input("Nom*", value=formation_details['nom'], key=f"edit_nom_{formation_id}")
                            
                            # Sélection du département
                            dept_options = departements['nom'].tolist()
                            
                            # Trouver l'index du département actuel
                            current_dept_id = int(formation_details['dept_id'])
                            current_dept = departements[departements['id'] == current_dept_id]
                            if not current_dept.empty:
                                current_dept_name = current_dept.iloc[0]['nom']
                                try:
                                    default_dept_idx = dept_options.index(current_dept_name)
                                except:
                                    default_dept_idx = 0
                            else:
                                default_dept_idx = 0
                            
                            selected_dept_idx = st.selectbox(
                                "Département*",
                                range(len(dept_options)),
                                index=default_dept_idx,
                                format_func=lambda x: dept_options[x],
                                key=f"edit_dept_{formation_id}"
                            )
                            dept_id = int(departements.iloc[selected_dept_idx]['id'])
                            
                            new_code = st.text_input("Code*", value=formation_details['code_formation'], key=f"edit_code_{formation_id}")
                        
                        with col2:
                            new_modules = st.number_input(
                                "Nombre de modules*", 
                                min_value=6, 
                                max_value=9, 
                                value=int(formation_details['nb_modules']),
                                key=f"edit_modules_{formation_id}"
                            )
                            
                            # Afficher les informations actuelles
                            with st.expander("Informations actuelles"):
                                for col in formations.columns:
                                    if col != 'id':
                                        try:
                                            value = formation_row[col]
                                            if not pd.isna(value):
                                                st.write(f"**{col}:** {value}")
                                        except:
                                            pass
                        
                        col_mod, col_cancel = st.columns(2)
                        
                        with col_mod:
                            if st.form_submit_button("Enregistrer", type="primary", use_container_width=True):
                                if new_nom and new_code:
                                    result = update_formation(
                                        formation_id, 
                                        new_nom, 
                                        dept_id, 
                                        new_code, 
                                        new_modules
                                    )
                                    if result:
                                        st.success("✅ Formation modifiée avec succès!")
                                        st.info("Les modifications ont été enregistrées dans la base de données.")
                                        import time
                                        time.sleep(1.5)
                                        st.rerun()
                                    else:
                                        st.error("❌ Erreur lors de la modification de la formation")
                                        st.info("Vérifiez que le nouveau code n'existe pas déjà pour une autre formation.")
                                else:
                                    if not new_nom:
                                        st.error("❌ Le nom est obligatoire")
                                    if not new_code:
                                        st.error("❌ Le code est obligatoire")
                        
                        with col_cancel:
                            if st.form_submit_button("Annuler", use_container_width=True):
                                st.rerun()
                else:
                    st.error("❌ Impossible de charger les détails de la formation")
        else:
            st.info("Aucune formation à modifier")
    
    # Onglet 4: Supprimer une formation
    with tab4:
        st.header("Supprimer une Formation")
        
        formations = get_all_formations()
        
        if formations is not None and not formations.empty:
            # Créer les options de sélection
            selection_options = []
            formation_ids = []
            
            for idx, row in formations.iterrows():
                formation_id = row['id']
                formation_ids.append(formation_id)
                
                # Construire l'option avec les colonnes disponibles
                parts = []
                if 'nom' in formations.columns:
                    parts.append(str(row['nom']))
                if 'code_formation' in formations.columns:
                    parts.append(f"({str(row['code_formation'])})")
                
                option_text = " - ".join(parts)
                selection_options.append(option_text)
            
            selected_idx_del = st.selectbox(
                "Choisir une formation à supprimer",
                range(len(selection_options)),
                format_func=lambda x: selection_options[x],
                key="delete_formation_select_unique"  # CLÉ UNIQUE DIFFÉRENTE
            )
            
            if selected_idx_del is not None:
                formation_id = formation_ids[selected_idx_del]
                formation_row = formations[formations['id'] == formation_id].iloc[0]
                
                st.warning("Action irréversible!")
                
                # Afficher les détails de la formation
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.subheader("Détails de la formation")
                        
                        # Afficher les colonnes disponibles
                        for col in formations.columns:
                            if col != 'id':
                                try:
                                    value = formation_row[col]
                                    if not pd.isna(value):
                                        st.write(f"**{col}:** {value}")
                                except:
                                    pass
                    
                    with col2:
                        st.error("⚠️ Attention!")
                        st.error("Cette action supprimera également toutes les spécialités associées!")
                
                st.divider()
                
                # Confirmation de suppression
                confirm = st.checkbox("Je confirme vouloir supprimer cette formation", key=f"confirm_delete_{formation_id}")
                
                col_sup, col_ann = st.columns(2)
                
                with col_sup:
                    if st.button("Supprimer définitivement", 
                                use_container_width=True, 
                                type="primary",
                                disabled=not confirm,
                                key=f"btn_delete_{formation_id}"):
                        result = delete_formation(formation_id)
                        if result:
                            st.success("✅ Formation supprimée avec succès!")
                            st.info("La formation a été supprimée de la base de données.")
                            import time
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.error("❌ Erreur lors de la suppression de la formation")
                            st.info("Vérifiez qu'aucune spécialité n'est associée à cette formation.")
                
                with col_ann:
                    if st.button("Annuler", 
                                use_container_width=True,
                                key=f"btn_cancel_{formation_id}"):
                        st.info("Suppression annulée")
        else:
            st.info("Aucune formation à supprimer")
def page_gestion_departements():
    # Configuration du background
    set_page_background('dashboard')
    
    # Ajout de styles CSS spécifiques pour cette page
    st.markdown("""
    <style>
    /* ============================================
       STYLES SPÉCIFIQUES GESTION DÉPARTEMENTS
       ============================================ */
    
    /* Header principal */
    .departement-header {
        background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .departement-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" fill-opacity="1" d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,144C672,139,768,181,864,186.7C960,192,1056,160,1152,144C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
        background-size: cover;
        opacity: 0.3;
    }
    
    .departement-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #dbeafe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
    }
    
    .departement-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }
    
    /* Cartes département améliorées */
    .departement-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .departement-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        border-color: #c7d2fe;
    }
    
    .departement-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #4f46e5 0%, #7c3aed 100%);
        border-radius: 20px 0 0 20px;
    }
    
    /* Badges spéciaux */
    .departement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(59, 130, 246, 0.2);
    }
    
    /* Boutons améliorés */
    .btn-departement-modify {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
    }
    
    .btn-departement-modify:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
    }
    
    .btn-departement-delete {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    .btn-departement-delete:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
    }
    
    /* Formulaire amélioré */
    .form-container-departement {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 35px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .form-label-departement {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 8px;
        display: block;
        font-size: 1rem;
    }
    
    /* Statistiques améliorées */
    .stat-card-departement {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    
    .stat-card-departement:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value-departement {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .stat-label-departement {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Onglets améliorés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 15px 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
    }
    
    /* Bouton d'action principal */
    .btn-primary-departement {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 16px 32px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .btn-primary-departement:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4) !important;
        background: linear-gradient(135deg, #0da271 0%, #047857 100%) !important;
    }
    
    /* Bouton secondaire */
    .btn-secondary-departement {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        color: #64748b !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .btn-secondary-departement:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #475569 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Message d'alerte amélioré */
    .alert-departement {
        background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
        border-left: 6px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
    }
    
    /* Card info département */
    .info-card-departement {
        background: linear-gradient(135deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Animation d'entrée */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .departement-header {
            padding: 25px 20px;
        }
        
        .departement-header h1 {
            font-size: 2.2rem;
        }
        
        .departement-card {
            padding: 20px;
        }
        
        .stat-value-departement {
            font-size: 2.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header stylisé
    st.markdown("""
    <div class="departement-header fade-in-up">
        <h1> Gestion des Départements</h1>
        <p>Ajouter, modifier et gérer les départements de l'UMBB</p>
        <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
            <i class="fas fa-building" style="margin-right: 5px;"></i>
            Administration des départements universitaires
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Connexion avec get_db()
    conn = get_db()
    if not conn:
        st.error("Impossible de se connecter à la base de données")
        return
    
    cursor = conn.cursor()
    
    # Créer table si besoin
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS departements (
            id SERIAL PRIMARY KEY,
            nom VARCHAR(100) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    
    # Initialiser session state
    if 'editing' not in st.session_state:
        st.session_state.editing = None
    if 'deleting' not in st.session_state:
        st.session_state.deleting = None
    
    # Onglets
    tab1, tab2 = st.tabs([" Ajouter", " Liste & Gérer"])
    
    with tab1:
        st.subheader("Ajouter un département")
        with st.form("ajout_form", clear_on_submit=True):
            nom = st.text_input("Nom", placeholder="Ex: Informatique")
            
            if st.form_submit_button("Ajouter"):
                if nom:
                    try:
                        cursor.execute("INSERT INTO departements (nom) VALUES (%s)", (nom,))
                        conn.commit()
                        st.success(f"✅ {nom} ajouté")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ {e}")
    
    with tab2:
        st.subheader("Liste des départements")
        
        cursor.execute("SELECT id, nom, created_at FROM departements ORDER BY nom")
        departements = cursor.fetchall()
        
        if not departements:
            st.info("Aucun département")
        else:
            for id_dep, nom_dep, date_crea in departements:
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(f"**{nom_dep}**")
                    st.caption(f"ID: {id_dep} | Créé le: {date_crea.strftime('%d/%m/%Y')}")
                
                with col2:
                    # MODIFIER - Utiliser une fonction callback
                    if st.button("✏", key=f"edit_btn_{id_dep}"):
                        # Stocker l'ID dans session_state
                        st.session_state.editing = id_dep
                        st.rerun()
                
                with col3:
                    # SUPPRIMER - Utiliser une fonction callback
                    if st.button("🗑", key=f"del_btn_{id_dep}"):
                        st.session_state.deleting = id_dep
                        st.rerun()
                
                # MODAL MODIFICATION (si cet ID est en cours d'édition)
                if st.session_state.editing == id_dep:
                    st.markdown("---")
                    st.write(f"Modifier '{nom_dep}' :")
                    
                    # Formulaire de modification
                    with st.form(f"edit_form_{id_dep}"):
                        new_nom = st.text_input("Nouveau nom", value=nom_dep)
                        
                        col_save, col_cancel = st.columns(2)
                        
                        with col_save:
                            if st.form_submit_button("Enregistrer"):
                                if new_nom and new_nom != nom_dep:
                                    try:
                                        cursor.execute("UPDATE departements SET nom = %s WHERE id = %s", (new_nom, id_dep))
                                        conn.commit()
                                        st.success(f"✅ Modifié: {nom_dep} → {new_nom}")
                                        st.session_state.editing = None
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ {e}")
                        
                        with col_cancel:
                            if st.form_submit_button("Annuler"):
                                st.session_state.editing = None
                                st.rerun()
                
                # MODAL SUPPRESSION (si cet ID est en cours de suppression)
                if st.session_state.deleting == id_dep:
                    st.markdown("---")
                    st.warning(f"Supprimer '{nom_dep}' ?")
                    
                    # Formulaire de confirmation
                    with st.form(f"del_form_{id_dep}"):
                        confirmation = st.checkbox("Je confirme la suppression")
                        
                        col_oui, col_non = st.columns(2)
                        
                        with col_oui:
                            if st.form_submit_button("Oui"):
                                if confirmation:
                                    try:
                                        cursor.execute("UPDATE professeurs SET dept_id = NULL WHERE dept_id = %s", (id_dep,))
                                        cursor.execute("DELETE FROM departements WHERE id = %s", (id_dep,))
                                        conn.commit()
                                        st.success(f" {nom_dep} supprimé")
                                        st.session_state.deleting = None
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ {e}")
                        
                        with col_non:
                            if st.form_submit_button("Non"):
                                st.session_state.deleting = None
                                st.rerun()
                
                st.divider()
    
    cursor.close()
    conn.close()






def get_validated_plannings_for_student(conn, specialite_id, niveau_id):
    """Récupère les plannings validés pour un étudiant selon sa spécialité et niveau"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT pa.nom_planning, 
                   COUNT(*) as total_examens,
                   MIN(pa.date_exam) as date_debut,
                   MAX(pa.date_exam) as date_fin,
                   pa.statut
            FROM planning_automatique pa
            JOIN modules m ON pa.module_id = m.id
            WHERE pa.statut = 'validé'
            AND m.specialite_id = %s
            AND m.annee_etude = %s
            GROUP BY pa.nom_planning, pa.statut
            ORDER BY MIN(pa.date_exam) DESC
        """, (str(specialite_id), str(niveau_id)))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Erreur récupération plannings étudiant: {str(e)}")
        return []

def get_validated_plannings_for_professor(conn, specialite=None):
    """Récupère les plannings validés pour un professeur avec filtrage par spécialité"""
    try:
        cursor = conn.cursor()
        
        if specialite and specialite != "Toutes":
            cursor.execute("""
                SELECT DISTINCT pa.nom_planning, 
                       COUNT(*) as total_examens,
                       MIN(pa.date_exam) as date_debut,
                       MAX(pa.date_exam) as date_fin,
                       m.specialite_id,
                       s.nom as specialite_nom,
                       pa.statut
                FROM planning_automatique pa
                JOIN modules m ON pa.module_id = m.id
                LEFT JOIN specialites s ON m.specialite_id = s.id
                WHERE pa.statut = 'validé'
                AND s.nom = %s
                GROUP BY pa.nom_planning, m.specialite_id, s.nom, pa.statut
                ORDER BY MIN(pa.date_exam) DESC
            """, (specialite,))
        else:
            cursor.execute("""
                SELECT DISTINCT pa.nom_planning, 
                       COUNT(*) as total_examens,
                       MIN(pa.date_exam) as date_debut,
                       MAX(pa.date_exam) as date_fin,
                       m.specialite_id,
                       s.nom as specialite_nom,
                       pa.statut
                FROM planning_automatique pa
                JOIN modules m ON pa.module_id = m.id
                LEFT JOIN specialites s ON m.specialite_id = s.id
                WHERE pa.statut = 'validé'
                GROUP BY pa.nom_planning, m.specialite_id, s.nom, pa.statut
                ORDER BY MIN(pa.date_exam) DESC
            """)
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Erreur récupération plannings professeur: {str(e)}")
        return []

def get_planning_details(conn, planning_name):
    """Récupère les détails d'un planning spécifique"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT pa.date_exam, pa.heure_debut, pa.heure_fin,
                   m.code_module, m.nom as module_nom,
                   m.specialite_id, s.nom as specialite_nom,
                   m.annee_etude, m.semestre,
                   l.nom as salle_nom, l.batiment,
                   pa.nb_inscrits, pa.nb_surveillants,
                   pa.statut, pa.created_at
            FROM planning_automatique pa
            LEFT JOIN modules m ON pa.module_id = m.id
            LEFT JOIN specialites s ON m.specialite_id = s.id
            LEFT JOIN lieu_examen l ON pa.salle_id = l.id
            WHERE pa.nom_planning = %s
            ORDER BY pa.date_exam, pa.heure_debut
        """, (planning_name,))
        return cursor.fetchall()
    except Exception as e:
        st.error(f"Erreur récupération détails: {str(e)}")
        return []

def afficher_planning_par_specialite_niveau(planning, conn):
    """Affiche le planning organisé par spécialité et niveau"""
    
    examens_par_specialite_niveau = defaultdict(lambda: defaultdict(list))
    
    for exam in planning:
        specialite = exam['specialite_nom']
        niveau = exam['niveau_nom']
        examens_par_specialite_niveau[specialite][niveau].append(exam)
    
    specialites = sorted(examens_par_specialite_niveau.keys())
    
    if len(specialites) == 0:
        st.info("Aucun examen à afficher")
        return
    
    if len(specialites) == 1:
        specialite = specialites[0]
        afficher_specialite(specialite, examens_par_specialite_niveau[specialite], conn)
    else:
        tabs = st.tabs([f"{spec}" for spec in specialites])
        
        for idx, specialite in enumerate(specialites):
            with tabs[idx]:
                afficher_specialite(specialite, examens_par_specialite_niveau[specialite], conn)

def afficher_specialite(specialite, niveaux_examens, conn):
    """Affiche une spécialité avec ses niveaux"""
    st.markdown(f'<div class="specialite-header"><h3>{specialite}</h3></div>', unsafe_allow_html=True)
    
    total_examens_specialite = sum(len(examens) for examens in niveaux_examens.values())
    st.info(f"**Total des examens pour {specialite}: {total_examens_specialite}**")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_etudiants = sum(e['nb_inscrits'] for niveau_examens in niveaux_examens.values() for e in niveau_examens)
        st.metric("Total étudiants", total_etudiants)
    with col2:
        total_surveillants = sum(e['nb_surveillants'] for niveau_examens in niveaux_examens.values() for e in niveau_examens)
        st.metric("Total surveillants", total_surveillants)
    with col3:
        total_jours = len(set(e['date_exam'] for niveau_examens in niveaux_examens.values() for e in niveau_examens))
        st.metric("Jours utilisés", total_jours)
    with col4:
        st.metric("Niveaux", len(niveaux_examens))
    
    for niveau in sorted(niveaux_examens.keys()):
        examens_niveau = niveaux_examens[niveau]
        
        with st.expander(f"**{niveau}** ({len(examens_niveau)} examens)", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Examens", len(examens_niveau))
            with col2:
                total_etudiants_niveau = sum(e['nb_inscrits'] for e in examens_niveau)
                st.metric("Étudiants", total_etudiants_niveau)
            with col3:
                total_surveillants_niveau = sum(e['nb_surveillants'] for e in examens_niveau)
                st.metric("Surveillants", total_surveillants_niveau)
            with col4:
                jours_uniques_niveau = len(set(e['date_exam'] for e in examens_niveau))
                st.metric("Jours", jours_uniques_niveau)
            
            afficher_tableau_niveau(examens_niveau, conn, niveau)

def afficher_tableau_niveau(examens, conn, niveau):
    """Affiche un tableau pour un niveau spécifique"""
    table_data = []
    
    for exam in sorted(examens, key=lambda x: (x['date_exam'], x['heure_debut'])):
        surveillants_noms = []
        try:
            cursor = conn.cursor()
            for prof_id in exam['surveillants_ids']:
                cursor.execute("SELECT nom, prenom FROM professeurs WHERE id = %s", (prof_id,))
                prof = cursor.fetchone()
                if prof:
                    surveillants_noms.append(f"{prof[1]} {prof[0]}")
                else:
                    surveillants_noms.append(f"Prof {prof_id}")
        except:
            surveillants_noms = [f"Prof {pid}" for pid in exam['surveillants_ids']]
        
        date_str = exam['date_exam'].strftime('%d/%m/%Y')
        jour_str = exam['date_exam'].strftime('%A')
        heure_str = f"{exam['heure_debut'].strftime('%H:%M')} - {exam['heure_fin'].strftime('%H:%M')}"
        
        prof_principal_nom = ""
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT nom, prenom FROM professeurs WHERE id = %s", (exam['prof_principal_id'],))
            prof = cursor.fetchone()
            if prof:
                prof_principal_nom = f"{prof[1]} {prof[0]}"
        except:
            prof_principal_nom = f"Prof {exam['prof_principal_id']}"
        
        table_data.append({
            'Date': date_str,
            'Jour': jour_str,
            'Heure': heure_str,
            'Module': f"{exam['module_code']} - {exam['module_nom']}",
            'Salle': exam['salle_nom'],
            'Bâtiment': exam['batiment'],
            'Capacité': exam['salle_capacite'],
            'Étudiants': exam['nb_inscrits'],
            'Surveillants': ", ".join(surveillants_noms[:3]),
            'Nb. Sur.': exam['nb_surveillants'],
            'Prof. Principal': prof_principal_nom,
            'Durée': f"{exam['duree_minutes']} min",
            'Semestre': exam.get('semestre', 'N/A'),
            'Statut Validation': exam.get('statut  ', 'en_attente')
        })
    
    if table_data:
        df = pd.DataFrame(table_data)
        
        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "Date": st.column_config.TextColumn("Date", width="small"),
                "Jour": st.column_config.TextColumn("Jour", width="small"),
                "Heure": st.column_config.TextColumn("Heure", width="small"),
                "Module": st.column_config.TextColumn("Module", width="large"),
                "Salle": st.column_config.TextColumn("Salle", width="medium"),
                "Bâtiment": st.column_config.TextColumn("Bâtiment", width="small"),
                "Capacité": st.column_config.NumberColumn("Capacité", width="small"),
                "Étudiants": st.column_config.NumberColumn("Étudiants", width="small"),
                "Surveillants": st.column_config.TextColumn("Surveillants", width="medium"),
                "Nb. Sur.": st.column_config.NumberColumn("Nb. Sur.", width="small"),
                "Prof. Principal": st.column_config.TextColumn("Prof. Principal", width="medium"),
                "Durée": st.column_config.TextColumn("Durée", width="small"),
                "Semestre": st.column_config.NumberColumn("Semestre", width="small"),
                "Statut Validation": st.column_config.TextColumn("Validation", width="small")
            },
            hide_index=True
        )
    else:
        st.info("Aucun examen pour ce niveau")

# =============================================
# PAGE GESTION DES ÉTUDIANTS
# =============================================
def page_gestion_professeurs():
    """Page de gestion des professeurs"""
    set_page_background('dashboard')
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown(f'<h1>Gestion des Professeurs</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Ajouter, modifier et gérer les professeurs</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    if user_info['role'] not in ['Vice-doyen', 'Admin_examens']:
        st.error("Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité")
        return
    
    # Initialiser les états de session
    if 'edit_mode' not in st.session_state:
        st.session_state['edit_mode'] = {}
    if 'delete_mode' not in st.session_state:
        st.session_state['delete_mode'] = {}
    
    conn = get_db()
    if not conn:
        st.error("Impossible de se connecter à la base de données")
        return
    
    def get_specialites(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, code_specialite, nom 
                FROM specialites 
                ORDER BY nom
            """)
            specialites = cursor.fetchall()
            return specialites
        except Exception as e:
            st.error(f"Erreur lors du chargement des spécialités: {e}")
            return []
    
    tab1, tab2, tab3 = st.tabs(["Ajouter un professeur", "Liste des professeurs", "📱 Gestion des comptes"])
    
    with tab1:
        st.markdown("### Ajouter un nouveau professeur")
        specialites_list = get_specialites(conn)
        
        # Préparer les options pour le selectbox
        specialite_options_dict = {"": "Sélectionner une spécialité..."}
        if specialites_list:
            for s in specialites_list:
                specialite_options_dict[str(s[0])] = f"{s[1]} - {s[2]}"
        
        with st.form("ajout_professeur"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom *")
            with col2:
                prenom = st.text_input("Prénom *")
            
            email = st.text_input("Email")
            
            # Utiliser un selectbox avec conversion en string
            specialite = st.selectbox(
                "Spécialité",
                options=list(specialite_options_dict.keys()),
                format_func=lambda x: specialite_options_dict.get(x, "Sélectionner...")
            )
            
            col3, col4 = st.columns(2)
            with col3:
                est_surveillant = st.checkbox("Est surveillant", value=True)
            with col4:
                heures_travail = st.number_input("Heures travail semaine *", 
                                                min_value=10, max_value=60, value=20, step=1)
            
            if st.form_submit_button("Ajouter le professeur"):
                if nom and prenom:
                    try:
                        cursor = conn.cursor()
                        
                        # Convertir en integer si ce n'est pas vide
                        specialite_id = None
                        if specialite:
                            try:
                                specialite_id = int(specialite)
                            except ValueError:
                                specialite_id = None
                        
                        cursor.execute(
                            "INSERT INTO professeurs (nom, prenom, email, specialite, est_surveillant, heures_travail_semaine) VALUES (%s, %s, %s, %s, %s, %s)",
                            (nom, prenom, email if email else None, specialite_id, est_surveillant, heures_travail)
                        )
                        conn.commit()
                        st.success(f"Professeur {prenom} {nom} ajouté avec succès")
                        time_module.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur: {e}")
                else:
                    st.error("Les champs marqués d'un * sont obligatoires")
    
    with tab2:
        st.markdown("### Liste des professeurs")
        
        try:
            cursor = conn.cursor()
            # CORRECTION: Ajouter un cast pour comparer les types correctement
            cursor.execute("""
                SELECT p.id, p.nom, p.prenom, p.email, 
                       COALESCE(s.nom, p.specialite::text) as specialite,
                       p.est_surveillant, p.heures_travail_semaine, p.utilisateur_id,
                       s.code_specialite as code_specialite,
                       s.id as specialite_id
                FROM professeurs p
                LEFT JOIN specialites s ON p.specialite::text = s.id::text
                ORDER BY p.nom, p.prenom
            """)
            
            professeurs = cursor.fetchall()
            
            if professeurs:
                search = st.text_input("Rechercher un professeur (nom, prénom, spécialité):")
                
                if search:
                    professeurs_filtres = [
                        p for p in professeurs 
                        if search.lower() in str(p[1]).lower() or 
                        search.lower() in str(p[2]).lower() or 
                        search.lower() in str(p[4]).lower()
                    ]
                else:
                    professeurs_filtres = professeurs
                
                specialites_list = get_specialites(conn)
                
                # Préparer les options pour l'édition
                specialite_options_edit = {"": "Aucune spécialité"}
                if specialites_list:
                    for s in specialites_list:
                        specialite_options_edit[str(s[0])] = f"{s[1]} - {s[2]}"
                
                for professeur in professeurs_filtres:
                    id_prof, nom, prenom, email, specialite, est_surveillant, heures, user_id, code_specialite, specialite_id = professeur
                    
                    specialite_display = "Pas de spécialité"
                    if specialite:
                        if code_specialite:
                            specialite_display = f"{code_specialite} - {specialite}"
                        else:
                            specialite_display = specialite
                    
                    with st.expander(f"{prenom} {nom} - {specialite_display}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**ID:** {id_prof}")
                            st.write(f"**Email:** {email if email else 'Non renseigné'}")
                            st.write(f"**Spécialité:** {specialite_display}")
                            st.write(f"**Surveillant:** {'✅ Oui' if est_surveillant else '❌ Non'}")
                            st.write(f"**Heures travail:** {heures}h/semaine")
                            st.write(f"**Compte utilisateur:** {'✅ Créé' if user_id else '❌ Non créé'}")
                            
                            cursor.execute("SELECT COUNT(*) FROM modules WHERE prof_responsable_id = %s", (id_prof,))
                            count_modules = cursor.fetchone()[0]
                            st.write(f"**Modules responsables:** {count_modules}")
                            
                        with col2:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("Modifier", key=f"edit_prof_{id_prof}"):
                                    st.session_state['edit_mode'][f'prof_{id_prof}'] = True
                            with col_b:
                                if st.button("Supprimer", key=f"del_prof_{id_prof}", type="secondary"):
                                    st.session_state['delete_mode'][f'prof_{id_prof}'] = True
                        
                        if st.session_state['edit_mode'].get(f'prof_{id_prof}', False):
                            st.markdown("---")
                            st.write("### Modifier le professeur")
                            
                            # Convertir specialite_id en string pour le selectbox
                            current_specialite_id = str(specialite_id) if specialite_id else ""
                            
                            with st.form(f"modifier_professeur_{id_prof}"):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    new_nom = st.text_input("Nom", value=nom, key=f"p_nom_{id_prof}")
                                with col_b:
                                    new_prenom = st.text_input("Prénom", value=prenom, key=f"p_prenom_{id_prof}")
                                
                                new_email = st.text_input("Email", value=email if email else "", key=f"p_email_{id_prof}")
                                
                                # Trouver l'index de la spécialité actuelle
                                specialite_keys = list(specialite_options_edit.keys())
                                index = 0
                                if current_specialite_id in specialite_keys:
                                    index = specialite_keys.index(current_specialite_id)
                                
                                new_specialite = st.selectbox(
                                    "Spécialité",
                                    options=specialite_keys,
                                    index=index,
                                    format_func=lambda x: specialite_options_edit.get(x, "Sélectionner..."),
                                    key=f"p_specialite_{id_prof}"
                                )
                                
                                col_c, col_d = st.columns(2)
                                with col_c:
                                    new_surveillant = st.checkbox("Surveillant", value=est_surveillant, key=f"p_surv_{id_prof}")
                                with col_d:
                                    new_heures = st.number_input("Heures travail (h/semaine)", 
                                                                value=heures,
                                                                min_value=10, max_value=60, key=f"p_heures_{id_prof}")
                                
                                col_e, col_f = st.columns(2)
                                with col_e:
                                    if st.form_submit_button("Sauvegarder"):
                                        try:
                                            # Convertir new_specialite en integer (peut être vide)
                                            specialite_val = None
                                            if new_specialite:
                                                try:
                                                    specialite_val = int(new_specialite)
                                                except ValueError:
                                                    specialite_val = None
                                            
                                            cursor.execute("""
                                                UPDATE professeurs 
                                                SET nom = %s, prenom = %s, email = %s, 
                                                    specialite = %s, est_surveillant = %s, 
                                                    heures_travail_semaine = %s
                                                WHERE id = %s
                                            """, (new_nom, new_prenom, new_email if new_email else None,
                                                  specialite_val, new_surveillant, new_heures, id_prof))
                                            conn.commit()
                                            st.success("Professeur modifié avec succès!")
                                            st.session_state['edit_mode'][f'prof_{id_prof}'] = False
                                            time_module.sleep(1)
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Erreur: {e}")
                                
                                with col_f:
                                    if st.form_submit_button("Annuler"):
                                        st.session_state['edit_mode'][f'prof_{id_prof}'] = False
                                        st.rerun()
                        
                        if st.session_state['delete_mode'].get(f'prof_{id_prof}', False):
                            st.markdown("---")
                            st.warning(f"Confirmer la suppression du professeur {prenom} {nom}?")
                            
                            cursor.execute("SELECT COUNT(*) FROM modules WHERE prof_responsable_id = %s", (id_prof,))
                            count_modules = cursor.fetchone()[0]
                            
                            if count_modules > 0:
                                st.error(f"Attention! Ce professeur est responsable de {count_modules} module(s)")
                                st.info("Solution: Modifiez d'abord les modules avant de supprimer le professeur.")
                            
                            col_x, col_y = st.columns(2)
                            with col_x:
                                if st.button("Oui, supprimer", key=f"confirm_del_prof_{id_prof}"):
                                    if count_modules == 0:
                                        try:
                                            cursor.execute("DELETE FROM professeurs WHERE id = %s", (id_prof,))
                                            conn.commit()
                                            st.success("Professeur supprimé avec succès!")
                                            st.session_state['delete_mode'][f'prof_{id_prof}'] = False
                                            time_module.sleep(1)
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Erreur: {e}")
                                    else:
                                        st.error("Impossible de supprimer. Résolvez d'abord les dépendances.")
                            
                            with col_y:
                                if st.button("Non, annuler", key=f"cancel_del_prof_{id_prof}"):
                                    st.session_state['delete_mode'][f'prof_{id_prof}'] = False
                                    st.rerun()
                
                st.markdown("---")
                if st.button("Afficher vue tableau"):
                    df = pd.DataFrame(professeurs_filtres, columns=[
                        'ID', 'Nom', 'Prénom', 'Email', 'Spécialité', 'Surveillant', 
                        'Heures/semaine', 'User ID', 'Code Spécialité', 'Spécialité ID'
                    ])
                    st.dataframe(df, use_container_width=True)
            
            else:
                st.info("Aucun professeur enregistré")
                
        except Exception as e:
            st.error(f"Erreur: {e}")
    
    with tab3:
        st.markdown('<div class="section-header">', unsafe_allow_html=True)
        st.markdown("### 📱 Gestion des comptes professeurs")
        st.markdown("Créez des comptes d'accès pour les professeurs")
        st.markdown('</div>', unsafe_allow_html=True)
        
        try:
            cursor = conn.cursor()
            
            # CORRECTION: Ajouter le cast dans la jointure
            cursor.execute("""
                SELECT p.id, p.nom, p.prenom, p.email, 
                       COALESCE(s.nom, p.specialite::text) as specialite,
                       p.est_surveillant, p.heures_travail_semaine,
                       CASE 
                           WHEN u.id IS NULL THEN '❌ Sans compte'
                           ELSE '✅ Compte existant'
                       END as statut_compte,
                       u.username as username
                FROM professeurs p
                LEFT JOIN specialites s ON p.specialite::text = s.id::text
                LEFT JOIN utilisateurs u ON p.utilisateur_id = u.id
                ORDER BY p.nom, p.prenom
            """)
            
            professeurs_comptes = cursor.fetchall()
            
            if not professeurs_comptes:
                st.info("Aucun professeur trouvé dans la base de données")
                conn.close()
                return
            
            # Statistiques
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                total_professeurs = len(professeurs_comptes)
                st.metric("Total professeurs", total_professeurs)
            
            with col_stat2:
                sans_compte = len([p for p in professeurs_comptes if p[7] == '❌ Sans compte'])
                st.metric("Sans compte", sans_compte, delta=f"{sans_compte/total_professeurs*100:.1f}%")
            
            with col_stat3:
                avec_compte = len([p for p in professeurs_comptes if p[7] == '✅ Compte existant'])
                st.metric("Avec compte", avec_compte, delta=f"{avec_compte/total_professeurs*100:.1f}%")
            
            # Barre de recherche
            st.markdown("---")
            col_search1, col_search2 = st.columns([3, 1])
            
            with col_search1:
                search_term = st.text_input(
                    "🔍 Rechercher un professeur", 
                    placeholder="Nom, prénom, spécialité...",
                    key="search_professeurs_comptes"
                )
            
            with col_search2:
                filter_compte = st.selectbox(
                    "Filtrer par statut",
                    ["Tous", "Sans compte", "Avec compte"],
                    key="filter_compte_professeurs"
                )
            
            # Filtrer les résultats
            professeurs_filtres = professeurs_comptes
            
            if search_term:
                search_lower = search_term.lower()
                professeurs_filtres = [
                    p for p in professeurs_filtres
                    if (search_lower in str(p[1]).lower() or  # nom
                        search_lower in str(p[2]).lower() or  # prénom
                        search_lower in str(p[3]).lower() or  # email
                        search_lower in str(p[4]).lower())    # spécialité
                ]
            
            if filter_compte == "Sans compte":
                professeurs_filtres = [p for p in professeurs_filtres if p[7] == '❌ Sans compte']
            elif filter_compte == "Avec compte":
                professeurs_filtres = [p for p in professeurs_filtres if p[7] == '✅ Compte existant']
            
            # Afficher les résultats
            st.markdown(f"### Résultats ({len(professeurs_filtres)} professeurs)")
            
            if not professeurs_filtres:
                st.info("Aucun professeur trouvé avec ces critères")
            else:
                # Onglets d'affichage
                tab_affichage1, tab_affichage2 = st.tabs(["Liste détaillée", "Tableau rapide"])
                
                with tab_affichage1:
                    # Afficher d'abord les professeurs sans compte
                    profs_sans_compte = [p for p in professeurs_filtres if p[7] == '❌ Sans compte']
                    
                    if profs_sans_compte:
                        st.markdown(f"#### Professeurs sans compte ({len(profs_sans_compte)})")
                        st.markdown('<div class="warning-box">Ces professeurs ne peuvent pas se connecter au système</div>', unsafe_allow_html=True)
                        
                        for prof in profs_sans_compte:
                            id_prof, nom, prenom, email, specialite, est_surveillant, heures, statut, username = prof
                            
                            with st.expander(f"❌ {prenom} {nom} - {specialite if specialite else 'Sans spécialité'}", expanded=True):
                                col_info1, col_info2 = st.columns([2, 1])
                                
                                with col_info1:
                                    st.markdown(f"**ID:** {id_prof}")
                                    st.markdown(f"**Nom complet:** {prenom} {nom}")
                                    st.markdown(f"**Email:** {email if email else 'Non renseigné'}")
                                    st.markdown(f"**Spécialité:** {specialite}")
                                    st.markdown(f"**Surveillant:** {'✅ Oui' if est_surveillant else '❌ Non'}")
                                    st.markdown(f"**Heures travail:** {heures}h/semaine")
                                
                                with col_info2:
                                    # Formulaire de création de compte
                                    with st.form(f"creer_compte_prof_{id_prof}"):
                                        username_default = f"{prenom.lower()}.{nom.lower().replace(' ', '_').replace('-', '_')}"
                                        username_default = username_default[:20]
                                        
                                        username_input = st.text_input(
                                            "Nom d'utilisateur *",
                                            value=username_default,
                                            key=f"username_prof_{id_prof}"
                                        )
                                        
                                        password = st.text_input(
                                            "Mot de passe *",
                                            type="password",
                                            value="professeur123",
                                            key=f"password_prof_{id_prof}"
                                        )
                                        
                                        confirm_password = st.text_input(
                                            "Confirmer le mot de passe *",
                                            type="password",
                                            value="professeur123",
                                            key=f"confirm_prof_{id_prof}"
                                        )
                                        
                                        col_btn1, col_btn2 = st.columns(2)
                                        with col_btn1:
                                            if st.form_submit_button("📝 Créer le compte", use_container_width=True):
                                                if not username_input:
                                                    st.error("Le nom d'utilisateur est obligatoire")
                                                elif not password:
                                                    st.error("Le mot de passe est obligatoire")
                                                elif password != confirm_password:
                                                    st.error("Les mots de passe ne correspondent pas")
                                                else:
                                                    success, message = creer_compte_professeur(
                                                        conn, id_prof, username_input, password
                                                    )
                                                    
                                                    if success:
                                                        st.success(f"✅ {message}")
                                                        time_module.sleep(2)
                                                        st.rerun()
                                                    else:
                                                        st.error(f"❌ {message}")
                                        
                                        with col_btn2:
                                            if st.form_submit_button("🔄 Réinitialiser", use_container_width=True, type="secondary"):
                                                st.rerun()
                    
                    # Afficher les professeurs avec compte
                    profs_avec_compte = [p for p in professeurs_filtres if p[7] == '✅ Compte existant']
                    
                    if profs_avec_compte:
                        st.markdown(f"#### ✅ Professeurs avec compte ({len(profs_avec_compte)})")
                        
                        for prof in profs_avec_compte:
                            id_prof, nom, prenom, email, specialite, est_surveillant, heures, statut, username = prof
                            
                            plain_password = get_plain_password(conn, username)
                            
                            with st.expander(f"✅ {prenom} {nom} - {specialite if specialite else 'Sans spécialité'}", expanded=False):
                                col_info1, col_info2 = st.columns([2, 1])
                                
                                with col_info1:   
                                    st.markdown(f"**ID:** {id_prof}")
                                    st.markdown(f"**Nom complet:** {prenom} {nom}")
                                    st.markdown(f"**Nom d'utilisateur:** `{username}`")
                                    if plain_password:
                                        st.markdown(f"**Mot de passe:** `{plain_password}`")
                                    else:
                                        st.markdown("**Mot de passe:** `(non disponible)`")
                                    
                                    if plain_password:
                                        credentials = f"Username: {username}\nPassword: {plain_password}"
                                        st.code(credentials, language="text")
                                    
                                    st.markdown(f"**Email:** {email if email else 'Non renseigné'}")
                                    st.markdown(f"**Spécialité:** {specialite}")
                                    st.markdown(f"**Surveillant:** {'✅ Oui' if est_surveillant else '❌ Non'}")
                                
                                with col_info2:
                                    st.success("✅ Compte actif")
                                    
                                    if plain_password:
                                        credentials_display = f"Username: {username}\nPassword: {plain_password}"
                                        if st.button("📋 Copier identifiants", key=f"copy_prof_{id_prof}", use_container_width=True):
                                            st.code(credentials_display)
                                            st.info("Identifiants copiés! (Coller avec Ctrl+V)")
                                    
                                    if st.button("🔄 Changer mot de passe", key=f"change_pass_prof_{id_prof}", use_container_width=True):
                                        st.session_state[f'show_change_pass_prof_{id_prof}'] = True
                                    
                                    if st.session_state.get(f'show_change_pass_prof_{id_prof}', False):
                                        with st.form(f"change_password_prof_{id_prof}"):
                                            new_password = st.text_input(
                                                "Nouveau mot de passe *",
                                                type="password",
                                                key=f"new_pass_prof_{id_prof}"
                                            )
                                            
                                            confirm_password = st.text_input(
                                                "Confirmer le mot de passe *",
                                                type="password",
                                                key=f"confirm_new_pass_prof_{id_prof}"
                                            )
                                            
                                            col_submit, col_cancel = st.columns(2)
                                            with col_submit:
                                                if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                                                    if new_password and new_password == confirm_password:
                                                        cursor.execute("SELECT id FROM utilisateurs WHERE username = %s", (username,))
                                                        user_id_result = cursor.fetchone()
                                                        if user_id_result:
                                                            success, message = changer_mot_de_passe_professeur(conn, id_prof, username, new_password)
                                                            if success:
                                                                st.success("✅ Mot de passe changé avec succès!")
                                                                time_module.sleep(2)
                                                                st.rerun()
                                                            else:
                                                                st.error(f"❌ {message}")
                                                        else:
                                                            st.error("Utilisateur non trouvé")
                                                    else:
                                                        st.error("Les mots de passe ne correspondent pas ou sont vides")
                                            
                                            with col_cancel:
                                                if st.form_submit_button("❌ Annuler", use_container_width=True):
                                                    st.session_state[f'show_change_pass_prof_{id_prof}'] = False
                                                    st.rerun()
                
                with tab_affichage2:
                    table_data = []
                    for prof in professeurs_filtres:
                        id_prof, nom, prenom, email, specialite, est_surveillant, heures, statut, username = prof
                        plain_password = get_plain_password(conn, username) if username else None
                        
                        table_data.append({
                            'ID': id_prof,
                            'Nom': nom,
                            'Prénom': prenom,
                            'Username': username or 'N/A',
                            'Password': plain_password or 'N/A',
                            'Email': email or 'N/A',
                            'Spécialité': specialite,
                            'Surveillant': 'Oui' if est_surveillant else 'Non',
                            'Heures': heures,
                            'Statut': statut
                        })
                    
                    df_table = pd.DataFrame(table_data)
                    st.dataframe(df_table, use_container_width=True)
                    
                    if st.button("📥 Exporter en CSV", use_container_width=True):
                        csv = df_table.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="Télécharger CSV",
                            data=csv,
                            file_name="professeurs_comptes.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
        
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
    
    conn.close()
# =============================================
# PAGE ADMIN - TOUS LES PLANNINGS

def page_gestion_professeurs():
    """Page de gestion des professeurs"""
    set_page_background('dashboard')
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown(f'<h1>Gestion des Professeurs</h1>', unsafe_allow_html=True)
    st.markdown(f'<p>Ajouter, modifier et gérer les professeurs</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    if user_info['role'] not in ['Vice-doyen', 'Admin_examens']:
        st.error("Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité")
        return
    
    conn = get_db()
    if not conn:
        st.error("Impossible de se connecter à la base de données")
        return
    
    tab1, tab2, tab3 = st.tabs(["Ajouter un professeur", "Liste des professeurs", "📱 Gestion des comptes"])
    def get_specialites(conn):
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, code_specialite, nom 
                FROM specialites 
                ORDER BY nom
            """)
            specialites = cursor.fetchall()
            return specialites
        except Exception as e:
            st.error(f"Erreur lors du chargement des spécialités: {e}")
            return []
    with tab1:
        st.markdown("### Ajouter un nouveau professeur")
        specialites_list = get_specialites(conn)
        specialite_options = []
        if specialites_list:
            specialite_options = [("", "Sélectionner une spécialité...")]
            specialite_options.extend([(s[0], f"{s[1]} - {s[2]}") for s in specialites_list])
        else:
            specialite_options = [("", "Aucune spécialité disponible")]
        with st.form("ajout_professeur"):
            col1, col2 = st.columns(2)
            with col1:
                nom = st.text_input("Nom *")
            with col2:
                prenom = st.text_input("Prénom *")
            
            email = st.text_input("Email")
            specialite = st.selectbox(
                "Spécialité",
                options=[opt[0] for opt in specialite_options],
                format_func=lambda x: dict(specialite_options).get(x, "Sélectionner une spécialité...")
            ) 
            
            col3, col4 = st.columns(2)
            with col3:
                est_surveillant = st.checkbox("Est surveillant", value=True)
            with col4:
                heures_travail = st.number_input("Heures travail semaine *", 
                                                min_value=10, max_value=60, value=20, step=1)
            
            if st.form_submit_button("Ajouter le professeur"):
                if nom and prenom:
                    try:
                        cursor = conn.cursor()
                        specialite_id = None
                        if  specialite:
                            # Chercher la spécialité dans la liste
                            for spec in specialites_list:
                                if spec[0] == specialite:
                                    specialite_id = spec[0]
                                    break
                        
                        cursor.execute(
                            "INSERT INTO professeurs (nom, prenom, email, specialite, est_surveillant, heures_travail_semaine) VALUES (%s, %s, %s, %s, %s, %s)",
                            (nom, prenom, email if email else None, specialite_id, est_surveillant, heures_travail)
                        )
                        conn.commit()
                        st.success(f"Professeur {prenom} {nom} ajouté avec succès")
                        time_module.sleep(1)
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erreur: {e}")
                else:
                    st.error("Les champs marqués d'un * sont obligatoires")
    
    with tab2:
        st.markdown("### Liste des professeurs")
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
    SELECT p.id, p.nom, p.prenom, p.email, 
           p.specialite as specialite_nom,  -- Changer ici
           p.est_surveillant, p.heures_travail_semaine, p.utilisateur_id
    FROM professeurs p
    ORDER BY p.nom, p.prenom
""")
            professeurs = cursor.fetchall()
            
            if professeurs:
                search = st.text_input("Rechercher un professeur (nom, prénom, spécialité):")
                
                if search:
                    professeurs_filtres = [
                        p for p in professeurs 
                        if search.lower() in str(p[1]).lower() or 
                        search.lower() in str(p[2]).lower() or 
                        search.lower() in str(p[4]).lower()
                    ]
                else:
                    professeurs_filtres = professeurs
                    specialites_list = get_specialites(conn)
                specialite_options_edit = []
                if specialites_list:
                    specialite_options_edit = [("", "Aucune spécialité")]
                    specialite_options_edit.extend([(s[0], f"{s[1]} - {s[2]}") for s in specialites_list])
                
                for professeur in professeurs_filtres:
                    id_prof, nom, prenom, email, specialite_nom, est_surveillant, heures_travail, user_id = professeur
                    specialite_display = "Pas de spécialité"
                    if  specialite_nom:
                        specialite_display = specialite_nom
                    with st.expander(f"{prenom} {nom} - {specialite_display}"):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**ID:** {id_prof}")
                            st.write(f"**Email:** {email if email else 'Non renseigné'}")
                            st.write(f"**Spécialité:** {specialite_display}")
                            st.write(f"**Surveillant:** {'✅ Oui' if est_surveillant else '❌ Non'}")
                            st.write(f"**Heures travail:** {heures_travail}h/semaine")
                            st.write(f"**Compte utilisateur:** {'✅ Créé' if user_id else '❌ Non créé'}")
                            
                            cursor.execute("SELECT COUNT(*) FROM modules WHERE prof_responsable_id = %s", (id_prof,))
                            count_modules = cursor.fetchone()[0]
                            st.write(f"**Modules responsables:** {count_modules}")
                            
                        with col2:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                if st.button("Modifier", key=f"edit_prof_{id_prof}"):
                                    st.session_state['edit_mode'][f'prof_{id_prof}'] = True
                            with col_b:
                                if st.button("Supprimer", key=f"del_prof_{id_prof}", type="secondary"):
                                    st.session_state['delete_mode'][f'prof_{id_prof}'] = True
                        
                        if st.session_state['edit_mode'].get(f'prof_{id_prof}', False):
                            st.markdown("---")
                            st.write("### Modifier le professeur")
                            cursor.execute("SELECT specialite FROM professeurs WHERE id = %s", (id_prof,))
                            current_specialite = cursor.fetchone()
                            current_specialite_id = current_specialite[0] if current_specialite else ""
                            with st.form(f"modifier_professeur_{id_prof}"):
                                col_a, col_b = st.columns(2)
                                with col_a:
                                    new_nom = st.text_input("Nom", value=nom, key=f"p_nom_{id_prof}")
                                with col_b:
                                    new_prenom = st.text_input("Prénom", value=prenom, key=f"p_prenom_{id_prof}")
                                
                                new_email = st.text_input("Email", value=email if email else "", key=f"p_email_{id_prof}")
                                if specialite_options_edit:
                                    new_specialite = st.selectbox(
                                    "Spécialité",
                                    options=[opt[0] for opt in specialite_options_edit],
                                    index=[opt[0] for opt in specialite_options_edit].index(current_specialite_id) if current_specialite_id in [opt[0] for opt in specialite_options_edit] else 0,
                                    format_func=lambda x: dict(specialite_options_edit).get(x, "Sélectionner une spécialité..."),
                                    key=f"p_specialite_{id_prof}"
                                )
                                else:
                                # Si c'est juste un texte
                                    new_specialite = st.text_input("Spécialité", 
                                                             value=specialite_nom if specialite_nom else "",
                                                             key=f"p_specialite_{id_prof}")
                                col_c, col_d = st.columns(2)
                                with col_c:
                                    new_surveillant = st.checkbox("Surveillant", value=est_surveillant, key=f"p_surv_{id_prof}")
                                with col_d:
                                    new_heures = st.number_input("Heures travail (h/semaine)", 
                                                                 value=int(heures_travail) if heures_travail else 20,
                                                            min_value=10, max_value=60, key=f"p_heures_{id_prof}")
                                col_e, col_f = st.columns(2)
                                with col_e:
                                    if st.form_submit_button("Sauvegarder"):
                                        try:
                                            cursor.execute("""
                                                UPDATE professeurs 
                                                SET nom = %s, prenom = %s, email = %s, 
                                                    specialite = %s, est_surveillant = %s, 
                                                    heures_travail_semaine = %s
                                                WHERE id = %s
                                            """, (new_nom, new_prenom, new_email if new_email else None,
                                                  new_specialite, new_surveillant, new_heures, id_prof))
                                            conn.commit()
                                            st.success("Professeur modifié avec succès!")
                                            st.session_state['edit_mode'][f'prof_{id_prof}'] = False
                                            time_module.sleep(1)
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Erreur: {e}")
                                
                                with col_f:
                                    if st.form_submit_button("Annuler"):
                                        st.session_state['edit_mode'][f'prof_{id_prof}'] = False
                                        st.rerun()
                        
                        if st.session_state['delete_mode'].get(f'prof_{id_prof}', False):
                            st.markdown("---")
                            st.warning(f"Confirmer la suppression du professeur {prenom} {nom}?")
                            
                            cursor.execute("SELECT COUNT(*) FROM modules WHERE prof_responsable_id = %s", (id_prof,))
                            count_modules = cursor.fetchone()[0]
                            
                            if count_modules > 0:
                                st.error(f"Attention! Ce professeur est responsable de {count_modules} module(s)")
                                st.info("Solution: Modifiez d'abord les modules avant de supprimer le professeur.")
                            
                            col_x, col_y = st.columns(2)
                            with col_x:
                                if st.button("Oui, supprimer", key=f"confirm_del_prof_{id_prof}"):
                                    if count_modules == 0:
                                        try:
                                            cursor.execute("DELETE FROM professeurs WHERE id = %s", (id_prof,))
                                            conn.commit()
                                            st.success("Professeur supprimé avec succès!")
                                            st.session_state['delete_mode'][f'prof_{id_prof}'] = False
                                            time_module.sleep(1)
                                            st.rerun()
                                        except Exception as e:
                                            st.error(f"Erreur: {e}")
                                    else:
                                        st.error("Impossible de supprimer. Résolvez d'abord les dépendances.")
                            
                            with col_y:
                                if st.button("Non, annuler", key=f"cancel_del_prof_{id_prof}"):
                                    st.session_state['delete_mode'][f'prof_{id_prof}'] = False
                                    st.rerun()
                
                st.markdown("---")
                if st.button("Afficher vue tableau"):
                    df = pd.DataFrame(professeurs_filtres, columns=['ID', 'Nom', 'Prénom', 'Email', 'Spécialité', 'Surveillant', 'Heures/semaine', 'User ID'])
                    st.dataframe(df, use_container_width=True)
            
            else:
                st.info("Aucun professeur enregistré")
                
        except Exception as e:
            st.error(f"Erreur: {e}")
    
    with tab3:
        st.markdown('<div class="section-header">', unsafe_allow_html=True)
        st.markdown("### 📱 Gestion des comptes professeurs")
        st.markdown("Créez des comptes d'accès pour les professeurs")
        st.markdown('</div>', unsafe_allow_html=True)
        
        try:
            cursor = conn.cursor()
            
            # Récupérer tous les professeurs avec statut compte
            cursor.execute("""
                SELECT p.id, p.nom, p.prenom, p.email, p.specialite,
                       p.est_surveillant, p.heures_travail_semaine,
                       CASE 
                           WHEN u.id IS NULL THEN '❌ Sans compte'
                           ELSE '✅ Compte existant'
                       END as statut_compte,
                       u.username as username
                FROM professeurs p
                LEFT JOIN utilisateurs u ON p.utilisateur_id = u.id
                ORDER BY p.nom, p.prenom
            """)
            
            professeurs_comptes = cursor.fetchall()
            
            if not professeurs_comptes:
                st.info("Aucun professeur trouvé dans la base de données")
                conn.close()
                return
            
            # Statistiques
            col_stat1, col_stat2, col_stat3 = st.columns(3)
            
            with col_stat1:
                total_professeurs = len(professeurs_comptes)
                st.metric("Total professeurs", total_professeurs)
            
            with col_stat2:
                sans_compte = len([p for p in professeurs_comptes if p[7] == '❌ Sans compte'])
                st.metric("Sans compte", sans_compte, delta=f"{sans_compte/total_professeurs*100:.1f}%")
            
            with col_stat3:
                avec_compte = len([p for p in professeurs_comptes if p[7] == '✅ Compte existant'])
                st.metric("Avec compte", avec_compte, delta=f"{avec_compte/total_professeurs*100:.1f}%")
            
            # Barre de recherche
            st.markdown("---")
            col_search1, col_search2 = st.columns([3, 1])
            
            with col_search1:
                search_term = st.text_input(
                    "🔍 Rechercher un professeur", 
                    placeholder="Nom, prénom, spécialité...",
                    key="search_professeurs_comptes"
                )
            
            with col_search2:
                filter_compte = st.selectbox(
                    "Filtrer par statut",
                    ["Tous", "Sans compte", "Avec compte"],
                    key="filter_compte_professeurs"
                )
            
            # Filtrer les résultats
            professeurs_filtres = professeurs_comptes
            
            if search_term:
                search_lower = search_term.lower()
                professeurs_filtres = [
                    p for p in professeurs_filtres
                    if (search_lower in str(p[1]).lower() or  # nom
                        search_lower in str(p[2]).lower() or  # prénom
                        search_lower in str(p[3]).lower() or  # email
                        search_lower in str(p[4]).lower())    # spécialité
                ]
            
            if filter_compte == "Sans compte":
                professeurs_filtres = [p for p in professeurs_filtres if p[7] == '❌ Sans compte']
            elif filter_compte == "Avec compte":
                professeurs_filtres = [p for p in professeurs_filtres if p[7] == '✅ Compte existant']
            
            # Afficher les résultats
            st.markdown(f"###  Résultats ({len(professeurs_filtres)} professeurs)")
            
            if not professeurs_filtres:
                st.info("Aucun professeur trouvé avec ces critères")
            else:
                # Onglets d'affichage
                tab_affichage1, tab_affichage2 = st.tabs(["Liste détaillée", "Tableau rapide"])
                
                with tab_affichage1:
                    # Afficher d'abord les professeurs sans compte
                    profs_sans_compte = [p for p in professeurs_filtres if p[7] == '❌ Sans compte']
                    
                    if profs_sans_compte:
                        st.markdown(f"####  Professeurs sans compte ({len(profs_sans_compte)})")
                        st.markdown('<div class="warning-box">Ces professeurs ne peuvent pas se connecter au système</div>', unsafe_allow_html=True)
                        
                        for prof in profs_sans_compte:
                            id_prof, nom, prenom, email, specialite, est_surveillant, heures, statut, username = prof
                            
                            with st.expander(f"❌ {prenom} {nom} - {specialite if specialite else 'Sans spécialité'}", expanded=True):
                                col_info1, col_info2 = st.columns([2, 1])
                                
                                with col_info1:
                                    st.markdown(f"**ID:** {id_prof}")
                                    st.markdown(f"**Nom complet:** {prenom} {nom}")
                                    st.markdown(f"**Email:** {email if email else 'Non renseigné'}")
                                    st.markdown(f"**Spécialité:** {specialite}")
                                    st.markdown(f"**Surveillant:** {'✅ Oui' if est_surveillant else '❌ Non'}")
                                    st.markdown(f"**Heures travail:** {heures}h/semaine")
                                
                                with col_info2:
                                    # Formulaire de création de compte
                                    with st.form(f"creer_compte_prof_{id_prof}"):
                                        username_default = f"{prenom.lower()}.{nom.lower().replace(' ', '_').replace('-', '_')}"
                                        username_default = username_default[:20]  # Limiter la longueur
                                        
                                        username_input = st.text_input(
                                            "Nom d'utilisateur *",
                                            value=username_default,
                                            key=f"username_prof_{id_prof}",
                                            help="Sans espaces, minuscules recommandé"
                                        )
                                        
                                        password = st.text_input(
                                            "Mot de passe *",
                                            type="password",
                                            value="professeur123",
                                            key=f"password_prof_{id_prof}",
                                            help="Mot de passe par défaut: professeur123"
                                        )
                                        
                                        confirm_password = st.text_input(
                                            "Confirmer le mot de passe *",
                                            type="password",
                                            value="professeur123",
                                            key=f"confirm_prof_{id_prof}"
                                        )
                                        
                                        col_btn1, col_btn2 = st.columns(2)
                                        with col_btn1:
                                            if st.form_submit_button("📝 Créer le compte", use_container_width=True):
                                                if not username_input:
                                                    st.error("Le nom d'utilisateur est obligatoire")
                                                elif not password:
                                                    st.error("Le mot de passe est obligatoire")
                                                elif password != confirm_password:
                                                    st.error("Les mots de passe ne correspondent pas")
                                                else:
                                                    success, message = creer_compte_professeur(
                                                        conn, id_prof, username_input, password
                                                    )
                                                    
                                                    if success:
                                                        st.success(f"✅ {message}")
                                                        time_module.sleep(2)
                                                        st.rerun()
                                                    else:
                                                        st.error(f"❌ {message}")
                                        
                                        with col_btn2:
                                            if st.form_submit_button("🔄 Réinitialiser", use_container_width=True, type="secondary"):
                                                st.rerun()
                    
                    # Afficher les professeurs avec compte
                    profs_avec_compte = [p for p in professeurs_filtres if p[7] == '✅ Compte existant']
                    
                    if profs_avec_compte:
                        st.markdown(f"#### ✅ Professeurs avec compte ({len(profs_avec_compte)})")
                        
                        for prof in profs_avec_compte:
                            id_prof, nom, prenom, email, specialite, est_surveillant, heures, statut, username = prof
                            
                            # Récupérer le mot de passe en clair
                            plain_password = get_plain_password(conn, username)
                            
                            with st.expander(f"✅ {prenom} {nom} - {specialite if specialite else 'Sans spécialité'}", expanded=False):
                                col_info1, col_info2 = st.columns([2, 1])
                                
                                with col_info1:   
                                    st.markdown(f"**ID:** {id_prof}")
                                    st.markdown(f"**Nom complet:** {prenom} {nom}")
                                    st.markdown(f"**Nom d'utilisateur:** `{username}`")
                                    if plain_password:
                                        st.markdown(f"**Mot de passe:** `{plain_password}`")
                                    else:
                                        st.markdown("**Mot de passe:** `(non disponible)`")
                                    
                                    # Afficher les identifiants dans une zone de code         
                                    if plain_password:
                                        credentials = f"Username: {username}\nPassword: {plain_password}"
                                        st.code(credentials, language="text")
                                    
                                    st.markdown(f"**Email:** {email if email else 'Non renseigné'}")
                                    st.markdown(f"**Spécialité:** {specialite}")
                                    st.markdown(f"**Surveillant:** {'✅ Oui' if est_surveillant else '❌ Non'}")
                                
                                with col_info2:
                                    st.success("✅ Compte actif")
                                    
                                    # Bouton pour copier les identifiants
                                    if plain_password:
                                        credentials_display = f"Username: {username}\nPassword: {plain_password}"
                                        if st.button("📋 Copier identifiants", key=f"copy_prof_{id_prof}", use_container_width=True):
                                            st.code(credentials_display)
                                            st.info("Identifiants copiés! (Coller avec Ctrl+V)")
                                    
                                    # Option pour réinitialiser le mot de passe
                                    if st.button("🔄 Changer mot de passe", key=f"change_pass_prof_{id_prof}", use_container_width=True):
                                        st.session_state[f'show_change_pass_prof_{id_prof}'] = True
                                    
                                    # Formulaire pour changer le mot de passe
                                    if st.session_state.get(f'show_change_pass_prof_{id_prof}', False):
                                        with st.form(f"change_password_prof_{id_prof}"):
                                            new_password = st.text_input(
                                                "Nouveau mot de passe *",
                                                type="password",
                                                key=f"new_pass_prof_{id_prof}"
                                            )
                                            
                                            confirm_password = st.text_input(
                                                "Confirmer le mot de passe *",
                                                type="password",
                                                key=f"confirm_new_pass_prof_{id_prof}"
                                            )
                                            
                                            col_submit, col_cancel = st.columns(2)
                                            with col_submit:
                                                if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                                                    if new_password and new_password == confirm_password:
                                                        # Récupérer l'ID utilisateur
                                                        cursor.execute("SELECT id FROM utilisateurs WHERE username = %s", (username,))
                                                        user_id_result = cursor.fetchone()
                                                        if user_id_result:
                                                            user_id = user_id_result[0]
                                                            success, message =changer_mot_de_passe_professeur(conn, id_prof, username, new_password)
                                                            if success:
                                                                st.success("✅ Mot de passe changé avec succès!")
                                                                time_module.sleep(2)
                                                                st.rerun()
                                                            else:
                                                                st.error(f"❌ {message}")
                                                        else:
                                                            st.error("Utilisateur non trouvé")
                                                    else:
                                                        st.error("Les mots de passe ne correspondent pas ou sont vides")
                                            
                                            with col_cancel:
                                                if st.form_submit_button("❌ Annuler", use_container_width=True):
                                                    st.session_state[f'show_change_pass_prof_{id_prof}'] = False
                                                    st.rerun()
                
                with tab_affichage2:
                    # Créer un tableau simple
                    table_data = []
                    for prof in professeurs_filtres:
                        id_prof, nom, prenom, email, specialite, est_surveillant, heures, statut, username = prof
                        plain_password = get_plain_password(conn, username) if username else None
                        
                        table_data.append({
                            'ID': id_prof,
                            'Nom': nom,
                            'Prénom': prenom,
                            'Username': username or 'N/A',
                            'Password': plain_password or 'N/A',
                            'Email': email or 'N/A',
                            'Spécialité': specialite,
                            'Surveillant': 'Oui' if est_surveillant else 'Non',
                            'Heures': heures,
                            'Statut': statut
                        })
                    
                    df_table = pd.DataFrame(table_data)
                    st.dataframe(df_table, use_container_width=True)
                    
                    # Option pour exporter
                    if st.button("📥 Exporter en CSV", use_container_width=True):
                        csv = df_table.to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            label="Télécharger CSV",
                            data=csv,
                            file_name="professeurs_comptes.csv",
                            mime="text/csv",
                            use_container_width=True
                        )
        
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
    
    conn.close()



# =============================================
# PAGE GESTION DES SALLES
# =============================================
# =============================================
# FONCTIONS DE GESTION DES MOTS DE PASSE
# =============================================

def reset_password(conn, user_id, new_password):
    """Réinitialise le mot de passe d'un utilisateur"""
    try:
        cursor = conn.cursor()
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        # Mettre à jour le mot de passe dans utilisateurs
        cursor.execute("""
            UPDATE utilisateurs 
            SET password_hash = %s 
            WHERE id = %s
        """, (password_hash, user_id))
        
        # Enregistrer le mot de passe en clair dans password_log
        cursor.execute("""
            SELECT username FROM utilisateurs WHERE id = %s
        """, (user_id,))
        username_result = cursor.fetchone()
        
        if username_result:
            username = username_result[0]
            cursor.execute("""
                INSERT INTO password_log (username, plain_password)
                VALUES (%s, %s)
            """, (username, new_password))
        
        conn.commit()
        return True, "Mot de passe réinitialisé avec succès"
    except Exception as e:
        conn.rollback()
        return False, f"Erreur lors de la réinitialisation: {str(e)}"


def page_gestion_salles():
    """Page de gestion des salles"""
    set_page_background('dashboard')
    
    st.markdown("""
    <style>
    /* ============================================
       STYLES SPÉCIFIQUES GESTION SALLES
       ============================================ */
    
    /* Header principal */
    .salle-header {
        background:linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 35px;
        margin-bottom: 35px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        text-align: center;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .salle-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" fill-opacity="1" d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,144C672,139,768,181,864,186.7C960,192,1056,160,1152,144C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
        background-size: cover;
        opacity: 0.3;
    }
    
    .salle-header h1 {
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 15px;
        background: linear-gradient(135deg, #ffffff 0%, #f3e8ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        position: relative;
        z-index: 1;
    }
    
    .salle-header p {
        font-size: 1.3rem;
        opacity: 0.9;
        margin-top: 10px;
        position: relative;
        z-index: 1;
    }
    
    /* Cartes salle améliorées */
    .salle-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .salle-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
        border-color: #e9d5ff;
    }
    
    .salle-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 6px;
        height: 100%;
        background: linear-gradient(180deg, #8b5cf6 0%, #a855f7 100%);
        border-radius: 20px 0 0 20px;
    }
    
    /* Badges spéciaux */
    .type-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    }
    
    .type-salle {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
    }
    
    .type-amphi {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    .type-labo {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .capacite-badge {
        display: inline-block;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
        box-shadow: 0 3px 10px rgba(139, 92, 246, 0.2);
    }
    
    .dispo-badge {
        display: inline-block;
        padding: 6px 16px;
        border-radius: 25px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 5px 0;
    }
    
    .dispo-oui {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.2);
    }
    
    .dispo-non {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        box-shadow: 0 3px 10px rgba(239, 68, 68, 0.2);
    }
    
    /* Boutons améliorés */
    .btn-salle-modify {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3) !important;
    }
    
    .btn-salle-modify:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.4) !important;
    }
    
    .btn-salle-delete {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        border-radius: 10px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
    }
    
    .btn-salle-delete:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
    }
    
    /* Formulaire amélioré */
    .form-container-salle {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 35px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    .form-label-salle {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 8px;
        display: block;
        font-size: 1rem;
    }
    
    /* Statistiques améliorées */
    .stat-card-salle {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(250, 245, 255, 0.9) 100%);
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
        transition: all 0.3s ease;
    }
    
    .stat-card-salle:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .stat-value-salle {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 10px;
    }
    
    .stat-label-salle {
        font-size: 0.95rem;
        color: #64748b;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Onglets améliorés */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.1);
        padding: 10px;
        border-radius: 15px;
        margin-bottom: 25px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        padding: 15px 25px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255, 255, 255, 0.15);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
        color: white !important;
        box-shadow: 0 4px 15px rgba(139, 92, 246, 0.3);
    }
    
    /* Zone de recherche améliorée */
    .search-box-salle {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Bouton d'action principal */
    .btn-primary-salle {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%) !important;
        border: none !important;
        color: white !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        padding: 16px 32px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.3) !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    .btn-primary-salle:hover {
        transform: translateY(-3px) !important;
        box-shadow: 0 10px 25px rgba(139, 92, 246, 0.4) !important;
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%) !important;
    }
    
    /* Bouton secondaire */
    .btn-secondary-salle {
        background: rgba(255, 255, 255, 0.1) !important;
        border: 2px solid rgba(255, 255, 255, 0.2) !important;
        color: #64748b !important;
        font-weight: 600 !important;
        padding: 14px 28px !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .btn-secondary-salle:hover {
        background: rgba(255, 255, 255, 0.15) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        color: #475569 !important;
        transform: translateY(-2px) !important;
    }
    
    /* Message d'alerte amélioré */
    .alert-salle {
        background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
        border-left: 6px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
    }
    
    /* Card info salle */
    .info-card-salle {
        background: linear-gradient(135deg, rgba(250, 245, 255, 0.9) 0%, rgba(245, 243, 255, 0.9) 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid rgba(226, 232, 240, 0.8);
    }
    
    /* Animation d'entrée */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .salle-header {
            padding: 25px 20px;
        }
        
        .salle-header h1 {
            font-size: 2.2rem;
        }
        
        .salle-card {
            padding: 20px;
        }
        
        .stat-value-salle {
            font-size: 2.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="salle-header fade-in-up">
        <h1>🏫 Gestion des Salles</h1>
        <p>Ajouter, modifier et gérer les salles d'examen</p>
        <div style="margin-top: 20px; font-size: 0.9rem; opacity: 0.8;">
            <i class="fas fa-building" style="margin-right: 5px;">gérer les salles d'examen</i>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    user_info = st.session_state['user_info']
    
    if user_info['role'] not in ['Vice-doyen', 'Admin_examens']:
        st.error("Vous n'avez pas les permissions nécessaires pour accéder à cette fonctionnalité")
        return
    
    conn = get_db()
    if not conn:
        st.error("Impossible de se connecter à la base de données")
        return
    
    # Onglets avec style amélioré
    tab1, tab2 = st.tabs([" Ajouter une salle", " Liste des salles"])
    
    with tab1:
        st.markdown("###  Ajouter une nouvelle salle")
        st.markdown("Remplissez le formulaire pour ajouter une nouvelle salle à la base de données.")
        
        with st.form("ajout_salle", clear_on_submit=True):
            
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('<div class="form-label-salle">Nom de la salle *</div>', unsafe_allow_html=True)
                nom = st.text_input("", placeholder="Ex: Amphi A", label_visibility="collapsed")
                
                st.markdown('<div class="form-label-salle">Type *</div>', unsafe_allow_html=True)
                type_salle = st.selectbox("", ["salle", "amphi", "labo"], label_visibility="collapsed")
            
            with col2:
                st.markdown('<div class="form-label-salle">Capacité *</div>', unsafe_allow_html=True)
                capacite = st.number_input("", min_value=1, value=30, label_visibility="collapsed")
                
                st.markdown('<div class="form-label-salle">Bâtiment</div>', unsafe_allow_html=True)
                batiment = st.text_input("", placeholder="Ex: Bâtiment Informatique", label_visibility="collapsed")
            
            st.markdown('<div class="form-label-salle">Disponible pour les examens</div>', unsafe_allow_html=True)
            disponible = st.checkbox("", value=True, label_visibility="collapsed")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.form_submit_button("Ajouter la salle", use_container_width=True):
                    if nom:
                        try:
                            cursor = conn.cursor()
                            cursor.execute(
                                "INSERT INTO lieu_examen (nom, capacite, type, batiment, disponible_examen) VALUES (%s, %s, %s, %s, %s)",
                                (nom, capacite, type_salle, batiment if batiment else None, disponible)
                            )
                            conn.commit()
                            st.success(f" Salle '{nom}' ajoutée avec succès")
                            time_module.sleep(1)
                            st.rerun()
                        except Exception as e:
                            st.error(f" Erreur: {e}")
                    else:
                        st.error("⚠ Le nom est obligatoire")
    
    with tab2:
        st.markdown("###  Liste des salles")
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, nom, capacite, type, batiment, disponible_examen
                FROM lieu_examen
                ORDER BY nom
            """)
            
            salles = cursor.fetchall()
            
            if salles:
                # Statistiques
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                total_salles = len(salles)
                amphi_count = len([s for s in salles if s[3] == 'amphi'])
                salle_count = len([s for s in salles if s[3] == 'salle'])
                labo_count = len([s for s in salles if s[3] == 'labo'])
                
                with col_stat1:
                    st.markdown(f'<div class="stat-value-salle">{total_salles}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-salle">TOTAL SALLES</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_stat2:
                 
                    st.markdown(f'<div class="stat-value-salle">{amphi_count}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-salle">AMPHIS</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_stat3:
                   
                    st.markdown(f'<div class="stat-value-salle">{salle_count}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-salle">SALLES</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                with col_stat4:
                    
                    st.markdown(f'<div class="stat-value-salle">{labo_count}</div>', unsafe_allow_html=True)
                    st.markdown('<div class="stat-label-salle">LABOS</div>', unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Zone de recherche
                
                search = st.text_input(" Rechercher une salle (nom, type, bâtiment):", 
                                      placeholder="Entrez un terme de recherche...")
                st.markdown('</div>', unsafe_allow_html=True)
                
                if search:
                    salles_filtres = [
                        s for s in salles 
                        if search.lower() in str(s[1]).lower() or 
                        search.lower() in str(s[3]).lower() or 
                        search.lower() in str(s[4]).lower()
                    ]
                else:
                    salles_filtres = salles
                
                for salle in salles_filtres:
                    id_salle, nom_salle, capacite, type_salle, batiment, disponible = salle
                    
                    st.markdown(f'<div class="salle-card fade-in-up">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        # Badge type
                        type_class = f"type-{type_salle}" if type_salle in ['salle', 'amphi', 'labo'] else "type-salle"
                        st.markdown(f'<span class="type-badge {type_class}">{type_salle.upper()}</span>', 
                                   unsafe_allow_html=True)
                        
                        st.markdown(f'<h4 style="margin: 10px 0;">{nom_salle}</h4>', unsafe_allow_html=True)
                        
                        st.markdown(f'<span class="capacite-badge">{capacite} places</span>', 
                                   unsafe_allow_html=True)
                        
                        col_info1, col_info2 = st.columns(2)
                        with col_info1:
                          
                            st.write(f"**ID:** {id_salle}")
                            st.write(f"**Bâtiment:** {batiment if batiment else 'Non spécifié'}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col_info2:
                            
                            # Badge disponibilité
                            dispo_class = "dispo-oui" if disponible else "dispo-non"
                            dispo_text = "DISPONIBLE" if disponible else "INDISPONIBLE"
                            st.markdown(f'<span class="dispo-badge {dispo_class}">{dispo_text}</span>', 
                                       unsafe_allow_html=True)
                            
                            cursor.execute("SELECT COUNT(*) FROM examens WHERE salle_id = %s", (id_salle,))
                            count_examens = cursor.fetchone()[0]
                            st.write(f"**Examens:** {count_examens}")
                            st.markdown('</div>', unsafe_allow_html=True)
                    
                    with col2:
                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("✏", key=f"edit_salle_{id_salle}", 
                                        help="Modifier cette salle", 
                                        use_container_width=True):
                                st.session_state['edit_mode'][f'salle_{id_salle}'] = True
                        
                        with col_btn2:
                            if st.button("🗑", key=f"del_salle_{id_salle}", 
                                        help="Supprimer cette salle", 
                                        type="secondary", use_container_width=True):
                                st.session_state['delete_mode'][f'salle_{id_salle}'] = True
                    
                    # Formulaire de modification
                    if st.session_state['edit_mode'].get(f'salle_{id_salle}', False):
                        st.markdown("---")
                        st.write("### ✏ Modifier la salle")
                        
                        with st.form(f"modifier_salle_{id_salle}"):
                            col_m1, col_m2 = st.columns(2)
                            with col_m1:
                                new_nom = st.text_input("Nom", value=nom_salle, key=f"s_nom_{id_salle}")
                                new_capacite = st.number_input("Capacité", value=capacite, 
                                                              min_value=1, key=f"s_capacite_{id_salle}")
                            
                            with col_m2:
                                new_type = st.selectbox("Type", ["salle", "amphi", "labo"], 
                                                       index=["salle", "amphi", "labo"].index(type_salle) 
                                                       if type_salle in ["salle", "amphi", "labo"] else 0,
                                                       key=f"s_type_{id_salle}")
                                new_batiment = st.text_input("Bâtiment", value=batiment if batiment else "", 
                                                            key=f"s_batiment_{id_salle}")
                                new_disponible = st.checkbox("Disponible pour examens", 
                                                            value=bool(disponible),
                                                            key=f"s_dispo_{id_salle}")
                            
                            col_btn_a, col_btn_b, _ = st.columns([1, 1, 2])
                            with col_btn_a:
                                if st.form_submit_button(" Sauvegarder", use_container_width=True):
                                    try:
                                        cursor.execute("""
                                            UPDATE lieu_examen 
                                            SET nom = %s, capacite = %s, type = %s, 
                                                batiment = %s, disponible_examen = %s
                                            WHERE id = %s
                                        """, (new_nom, new_capacite, new_type, 
                                              new_batiment if new_batiment else None, 
                                              new_disponible, id_salle))
                                        conn.commit()
                                        st.success("✅ Salle modifiée avec succès!")
                                        st.session_state['edit_mode'][f'salle_{id_salle}'] = False
                                        time_module.sleep(1)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Erreur: {e}")
                            
                            with col_btn_b:
                                if st.form_submit_button("❌ Annuler", use_container_width=True):
                                    st.session_state['edit_mode'][f'salle_{id_salle}'] = False
                                    st.rerun()
                    
                    # Confirmation suppression
                    if st.session_state['delete_mode'].get(f'salle_{id_salle}', False):
                        st.markdown("---")
                        st.warning(f"⚠ Confirmer la suppression de la salle **'{nom_salle}'**?")
                        
                        cursor.execute("SELECT COUNT(*) FROM examens WHERE salle_id = %s", (id_salle,))
                        count_examens = cursor.fetchone()[0]
                        
                        if count_examens > 0:
                            st.error(f"❌ Cette salle est utilisée dans **{count_examens} examen(s)**.")
                            st.info(" Solution: Supprimez d'abord les examens utilisant cette salle.")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        col_x, col_y, _ = st.columns([1, 1, 2])
                        with col_x:
                            if st.button("✅ Oui, supprimer", key=f"confirm_del_salle_{id_salle}", 
                                        use_container_width=True, type="primary"):
                                if count_examens == 0:
                                    try:
                                        cursor.execute("DELETE FROM lieu_examen WHERE id = %s", (id_salle,))
                                        conn.commit()
                                        st.success(" Salle supprimée avec succès!")
                                        st.session_state['delete_mode'][f'salle_{id_salle}'] = False
                                        time_module.sleep(1)
                                        st.rerun()
                                    except Exception as e:
                                        st.error(f"❌ Erreur: {e}")
                                else:
                                    st.error("❌ Impossible de supprimer. Résolvez d'abord les dépendances.")
                        
                        with col_y:
                            if st.button("❌ Non, annuler", key=f"cancel_del_salle_{id_salle}", 
                                        use_container_width=True):
                                st.session_state['delete_mode'][f'salle_{id_salle}'] = False
                                st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                col_view1, col_view2 = st.columns([1, 1])
                with col_view1:
                    if st.button(" Afficher vue tableau", use_container_width=True):
                        df = pd.DataFrame(salles_filtres, columns=['ID', 'Nom', 'Capacité', 'Type', 'Bâtiment', 'Disponible'])
                        st.dataframe(df, use_container_width=True)
                with col_view2:
                    if st.button(" Actualiser la liste", use_container_width=True):
                        st.rerun()
            
            else:
                st.info("ℹ Aucune salle enregistrée")
                
        except Exception as e:
            st.error(f"❌ Erreur: {e}")
    
    conn.close()


# ============================================
# STYLES CSS SPÉCIFIQUES POUR CETTE PAGE
# ============================================

st.markdown("""
<style>
/* ============================================
   STYLES SPÉCIFIQUES GESTION ÉTUDIANTS
   ============================================ */

/* Header principal */
.etudiant-header {
    background: linear-gradient(135deg, rgba(21, 94, 117, 0.9) 0%, rgba(29, 78, 216, 0.9) 100%);
    border-radius: 20px;
    padding: 35px;
    margin-bottom: 35px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    text-align: center;
    color: white;
    position: relative;
    overflow: hidden;
}

.etudiant-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.05)" fill-opacity="1" d="M0,160L48,176C96,192,192,224,288,213.3C384,203,480,149,576,144C672,139,768,181,864,186.7C960,192,1056,160,1152,144C1248,128,1344,128,1392,128L1440,128L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>');
    background-size: cover;
    opacity: 0.3;
}

.etudiant-header h1 {
    font-size: 2.8rem;
    font-weight: 800;
    margin-bottom: 15px;
    background: linear-gradient(135deg, #ffffff 0%, #dbeafe 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    position: relative;
    z-index: 1;
}

.etudiant-header p {
    font-size: 1.3rem;
    opacity: 0.9;
    margin-top: 10px;
    position: relative;
    z-index: 1;
}

/* Cartes étudiant améliorées */
.etudiant-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 25px;
    margin: 15px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(226, 232, 240, 0.8);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.etudiant-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    border-color: #c7d2fe;
}

.etudiant-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 6px;
    height: 100%;
    background: linear-gradient(180deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 20px 0 0 20px;
}

/* Badges spéciaux */
.specialite-badge {
    display: inline-block;
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(59, 130, 246, 0.2);
}

.niveau-badge {
    display: inline-block;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(16, 185, 129, 0.2);
}

.promo-badge {
    display: inline-block;
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    padding: 6px 16px;
    border-radius: 25px;
    font-size: 0.85rem;
    font-weight: 600;
    margin: 5px 0;
    box-shadow: 0 3px 10px rgba(245, 158, 11, 0.2);
}

/* Boutons améliorés */
.btn-etudiant-modify {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
}

.btn-etudiant-modify:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
}

.btn-etudiant-delete {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3) !important;
}

.btn-etudiant-delete:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4) !important;
}

/* Formulaire amélioré */
.form-container-etudiant {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 20px;
    padding: 35px;
    margin: 20px 0;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    border: 1px solid rgba(226, 232, 240, 0.8);
}

.form-label-etudiant {
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 8px;
    display: block;
    font-size: 1rem;
}

/* Statistiques améliorées */
.stat-card-etudiant {
    background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(248, 250, 252, 0.9) 100%);
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(226, 232, 240, 0.8);
    transition: all 0.3s ease;
}

.stat-card-etudiant:hover {
    transform: translateY(-3px);
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.stat-value-etudiant {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
}

.stat-label-etudiant {
    font-size: 0.95rem;
    color: #64748b;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Onglets améliorés */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(255, 255, 255, 0.1);
    padding: 10px;
    border-radius: 15px;
    margin-bottom: 25px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px;
    padding: 15px 25px;
    font-weight: 600;
    font-size: 1rem;
    transition: all 0.3s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(255, 255, 255, 0.15);
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3);
}

/* Zone de recherche améliorée */
.search-box-etudiant {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 25px;
    margin: 20px 0;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
    border: 1px solid rgba(226, 232, 240, 0.8);
}

/* Bouton d'action principal */
.btn-primary-etudiant {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.1rem !important;
    padding: 16px 32px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 6px 20px rgba(16, 185, 129, 0.3) !important;
    width: 100% !important
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.btn-primary-etudiant:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4) !important;
    background: linear-gradient(135deg, #0da271 0%, #047857 100%) !important;
}

/* Bouton secondaire */
.btn-secondary-etudiant {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 2px solid rgba(255, 255, 255, 0.2) !important;
    color: #64748b !important;
    font-weight: 600 !important;
    padding: 14px 28px !important;
    border-radius: 12px !important;
    transition: all 0.3s ease !important;
    width: 100% !important;
}

.btn-secondary-etudiant:hover {
    background: rgba(255, 255, 255, 0.15) !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
    color: #475569 !important;
    transform: translateY(-2px) !important;
}

/* Message d'alerte amélioré */
.alert-etudiant {
    background: linear-gradient(135deg, rgba(254, 226, 226, 0.9) 0%, rgba(254, 202, 202, 0.9) 100%);
    border-left: 6px solid #ef4444;
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.1);
}

/* Card info étudiant */
.info-card-etudiant {
    background: linear-gradient(135deg, rgba(248, 250, 252, 0.9) 0%, rgba(241, 245, 249, 0.9) 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border: 1px solid rgba(226, 232, 240, 0.8);
}

/* Animation d'entrée */
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}

/* Responsive */
@media (max-width: 768px) {
    .etudiant-header {
        padding: 25px 20px;
    }
    
    .etudiant-header h1 {
        font-size: 2.2rem;
    }
    
    .etudiant-card {
        padding: 20px;
    }
    
    .stat-value-etudiant {
        font-size: 2.2rem;
    }
}
</style>
""", unsafe_allow_html=True)

# ==================== FONCTIONS POUR LES SPÉCIALITÉS ====================

def get_all_specialites():
    """Récupère toutes les spécialités avec leurs détails"""
    query = """
    SELECT 
        s.id,
        s.nom as specialite,
        f.nom as formation,
        n.nom as niveau,
        s.code_specialite,
        COALESCE(CONCAT(p.nom, ' ', p.prenom), 'Non spécifié') as responsable,
        s.capacite_max,
        s.description
    FROM specialites s
    JOIN formations f ON s.formation_id = f.id
    JOIN niveaux n ON s.niveau_id = n.id
    LEFT JOIN professeurs p ON s.responsable_id = p.id
    ORDER BY s.id
    """
    return execute_query(query)

def get_all_formations():
    """Récupère toutes les formations"""
    query = "SELECT id, nom, code_formation FROM formations ORDER BY nom"
    return execute_query(query)

def get_all_niveaux():
    """Récupère tous les niveaux"""
    query = "SELECT id, nom, code FROM niveaux ORDER BY ordre"
    return execute_query(query)

def get_all_professeurs():
    """Récupère tous les professeurs avec leurs départements"""
    query = """
    SELECT 
        p.id,
        p.nom,
        p.prenom,
        p.specialite,
        d.nom as departement
    FROM professeurs p
    JOIN departements d ON p.dept_id = d.id
    ORDER BY p.nom, p.prenom
    """
    return execute_query(query)

def add_specialite(nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max):
    """Ajoute une nouvelle spécialité"""
    query = """
    INSERT INTO specialites 
        (nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    if responsable_id is None:
        responsable_id = None
    
    conn = get_db()
    if conn is None:
        return False
    
    try:
        with conn.cursor() as cur:
            cur.execute(query, (nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max))
            result = cur.fetchone()
            conn.commit()
            return result is not None
    except Exception as e:
        st.error(f"❌ Erreur lors de l'ajout: {e}")
        conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def update_specialite(specialite_id, nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max):
    """Met à jour une spécialité"""
    query = """
    UPDATE specialites 
    SET nom = %s, 
        formation_id = %s, 
        niveau_id = %s, 
        code_specialite = %s, 
        description = %s, 
        responsable_id = %s, 

        capacite_max = %s
    WHERE id = %s
    """
    return execute_query(query, (nom, formation_id, niveau_id, code_specialite, description, responsable_id, capacite_max, specialite_id), fetch=False)

def delete_specialite(specialite_id):
    """Supprime une spécialité"""
    return execute_query("DELETE FROM specialites WHERE id = %s", (specialite_id,), fetch=False)

def get_specialite_by_id(specialite_id):
    """Récupère une spécialité par son ID"""
    query = """
    SELECT 
        s.id,
        s.nom,
        s.formation_id,
        s.niveau_id,
        s.code_specialite,
        s.description,
        s.responsable_id,
        s.capacite_max
    FROM specialites s
    WHERE s.id = %s
    """
    return execute_query(query, (specialite_id,))

# ==================== PAGE DE GESTION DES SPÉCIALITÉS ====================



# =============================================
# ROUTAGE DES PAGES
# =============================================

# Afficher la barre latérale
afficher_sidebar()

# Router vers la page appropriée
menu = st.session_state.get('menu', 'dashboard')

if menu == 'dashboard':
    page_dashboard()
elif menu == 'generation_planning':
    page_generation_planning()

elif menu == 'validation_edt':
    page_validation_edt()
elif menu == 'detail_planning_validation':
    page_detail_planning_validation()
elif menu == 'detail_planning_valide':
    page_detail_planning_valide()
elif menu == 'gestion_etudiants':
  page_gestion_etudiants()
elif menu == 'gestion_professeurs':
    page_gestion_professeurs()
elif menu == 'gestion_modules':
    page_gestion_modules()
elif menu == 'gestion_salles':
      page_gestion_salles()
elif menu == 'professeur_plannings':
    page_professeur_plannings()
elif menu == 'gestion_departements':  
    page_gestion_departements() 
elif menu == 'gestion_specialites':
    page_gestion_specialites()
elif menu == 'gestion_formations':
    page_gestion_formations()       
elif menu == 'etudiant_plannings':
    page_etudiant_plannings()

else:
    page_dashboard()