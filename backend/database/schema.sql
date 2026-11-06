-- =============================================
-- SCHEMA POSTGRESQL - VERSION CORRIGÉE
-- =============================================

-- Suppression en ordre inverse des dépendances
DROP TABLE IF EXISTS examens_historique CASCADE;
DROP TABLE IF EXISTS connexions_log CASCADE;
DROP TABLE IF EXISTS utilisateurs CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS inscriptions CASCADE;
DROP TABLE IF EXISTS examens CASCADE;
DROP TABLE IF EXISTS lieu_examen CASCADE;
DROP TABLE IF EXISTS modules CASCADE;
DROP TABLE IF EXISTS professeurs CASCADE;
DROP TABLE IF EXISTS etudiants CASCADE;
DROP TABLE IF EXISTS formations CASCADE;
DROP TABLE IF EXISTS departements CASCADE;

-- =============================================
-- TABLES DE BASE (CRÉATION D'ABORD)
-- =============================================

-- 1. DÉPARTEMENTS (DOIT ÊTRE LA PREMIÈRE)
CREATE TABLE departements (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. FORMATIONS
CREATE TABLE formations (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(200) NOT NULL,
    dept_id INT NOT NULL REFERENCES departements(id) ON DELETE CASCADE,
    nb_modules INT CHECK (nb_modules BETWEEN 6 AND 9),
    code_formation VARCHAR(20) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. RÔLES (avant utilisateurs)
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    niveau_acces INTEGER DEFAULT 1,
    permissions JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. UTILISATEURS (après roles et departements)
CREATE TABLE utilisateurs (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE,
    role_id INTEGER NOT NULL REFERENCES roles(id),
    departement_id INTEGER REFERENCES departements(id),
    est_actif BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- 5. PROFESSEURS
CREATE TABLE professeurs (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    dept_id INT REFERENCES departements(id),
    specialite VARCHAR(200),
    quota_surveillance_journalier INT DEFAULT 3,
    heures_travail_semaine INT DEFAULT 20,
    est_surveillant BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. ÉTUDIANTS
CREATE TABLE etudiants (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE,
    formation_id INT REFERENCES formations(id),
    promo INT CHECK (promo BETWEEN 2020 AND 2030),
    annee_etude INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. MODULES
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    code_module VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(200) NOT NULL,
    credits INT DEFAULT 6 CHECK (credits BETWEEN 3 AND 12),
    formation_id INT NOT NULL REFERENCES formations(id) ON DELETE CASCADE,
    prof_responsable_id INT NOT NULL REFERENCES professeurs(id) ON DELETE CASCADE,
    pre_requis_id INT REFERENCES modules(id),
    semestre INT CHECK (semestre IN (1, 2)),
    volume_horaire INT DEFAULT 30,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. LIEUX D'EXAMEN
CREATE TABLE lieu_examen (
    id SERIAL PRIMARY KEY,
    code_salle VARCHAR(20) UNIQUE NOT NULL,
    nom VARCHAR(100) NOT NULL,
    capacite INT CHECK (capacite > 0),
    type VARCHAR(30) CHECK (type IN ('amphi', 'salle', 'labo', 'salle_spéciale')),
    batiment VARCHAR(50),
    etage INT,
    equipement_special TEXT[],
    disponible_examen BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. INSCRIPTIONS
CREATE TABLE inscriptions (
    etudiant_id INT NOT NULL REFERENCES etudiants(id) ON DELETE CASCADE,
    module_id INT NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    annee_academique INT NOT NULL,
    note DECIMAL(4,2) CHECK (note BETWEEN 0 AND 20),
    date_inscription DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (etudiant_id, module_id, annee_academique)
);

-- 10. EXAMENS (SANS COLONNE GÉNÉRÉE - ON UTILISERA UN TRIGGER)
CREATE TABLE examens (
    id SERIAL PRIMARY KEY,
    module_id INT NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    prof_surveillant_id INT NOT NULL REFERENCES professeurs(id) ON DELETE CASCADE,
    salle_id INT NOT NULL REFERENCES lieu_examen(id) ON DELETE CASCADE,
    date_exam DATE NOT NULL,
    heure_debut TIME NOT NULL CHECK (heure_debut BETWEEN '08:00:00' AND '19:00:00'),
    duree_minutes INT NOT NULL CHECK (duree_minutes BETWEEN 60 AND 240),
    heure_fin TIME, -- Sera calculée par trigger
    session VARCHAR(20) DEFAULT 'Principale',
    statut VARCHAR(20) DEFAULT 'planifié' CHECK (statut IN ('planifié', 'confirmé', 'annulé')),
    statut_validation VARCHAR(20) DEFAULT 'en_attente' CHECK (statut_validation IN ('en_attente', 'validé_dept', 'validé_final', 'refusé')),
    nombre_inscrits INT DEFAULT 0,
    created_by INTEGER REFERENCES utilisateurs(id),
    validated_by INTEGER REFERENCES utilisateurs(id),
    validation_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- Contrainte d'unicité salle + date + heure
    UNIQUE(salle_id, date_exam, heure_debut)
);

-- =============================================
-- TABLES DE LOG ET HISTORIQUE
-- =============================================

-- Table de suivi des connexions
CREATE TABLE connexions_log (
    id SERIAL PRIMARY KEY,
    utilisateur_id INTEGER REFERENCES utilisateurs(id),
    date_connexion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ip_adresse VARCHAR(45),
    succes BOOLEAN
);

-- Table historique des examens
CREATE TABLE examens_historique (
    id SERIAL PRIMARY KEY,
    examen_id INTEGER REFERENCES examens(id) ON DELETE CASCADE,
    action VARCHAR(50),
    ancienne_valeur JSONB,
    nouvelle_valeur JSONB,
    modifie_par INTEGER REFERENCES utilisateurs(id),
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =============================================
-- DONNÉES DE BASE
-- =============================================

-- Rôles du système (d'abord)
INSERT INTO roles (nom, description, niveau_acces, permissions) VALUES
('Vice-doyen', 'Accès stratégique global avec validation finale', 5, '{"dashboard": ["global", "stats", "kpi"], "departements": ["all"], "formations": ["all"], "etudiants": ["all"], "professeurs": ["all"], "modules": ["all"], "salles": ["all"], "examens": ["all", "validate", "generate"], "planning": ["all", "conflicts", "optimize"], "reports": ["all", "export"]}'),
('Doyen', 'Validation finale des emplois du temps', 5, '{"dashboard": ["global", "stats"], "formations": ["all"], "examens": ["all", "validate"], "planning": ["all", "conflicts"], "reports": ["all"]}'),
('Admin_examens', 'Génération automatique et gestion des examens', 4, '{"dashboard": ["admin", "stats", "conflicts"], "etudiants": ["all"], "professeurs": ["all"], "modules": ["all"], "salles": ["all"], "examens": ["all", "generate", "detect_conflicts", "optimize"], "planning": ["all", "generate", "optimize"], "reports": ["all", "export"]}'),
('Chef_departement', 'Gestion du département avec validation locale', 3, '{"dashboard": ["dept", "stats"], "etudiants": ["dept_only"], "professeurs": ["dept_only"], "modules": ["dept_only"], "examens": ["dept_only", "validate_dept"], "planning": ["dept_only", "conflicts"], "reports": ["dept_only"]}'),
('Professeur', 'Consultation planning et modules enseignés', 2, '{"dashboard": ["prof", "my_modules"], "planning": ["my_exams", "my_surveillances"], "modules": ["my_modules"], "profile": ["my_info"]}'),
('Etudiant', 'Consultation planning personnel', 1, '{"dashboard": ["student", "my_exams"], "planning": ["my_schedule"], "modules": ["my_modules"], "profile": ["my_info"]}')
ON CONFLICT (nom) DO NOTHING;

-- Départements
INSERT INTO departements (nom) VALUES
('Informatique'),
('Mathématiques'),
('Physique'),
('Chimie'),
('Biologie'),
('Sciences de l''Ingénieur'),
('Langues et Littérature')
ON CONFLICT (nom) DO NOTHING;

-- Salles
INSERT INTO lieu_examen (code_salle, nom, capacite, type, batiment) VALUES
('AMPHI-A', 'Amphithéâtre Principal', 300, 'amphi', 'Bâtiment A'),
('AMPHI-B', 'Amphithéâtre Secondaire', 200, 'amphi', 'Bâtiment A'),
('SAL-101', 'Salle 101', 50, 'salle', 'Bâtiment B'),
('SAL-102', 'Salle 102', 50, 'salle', 'Bâtiment B'),
('SAL-103', 'Salle 103', 30, 'salle', 'Bâtiment B'),
('LAB-INF1', 'Laboratoire Informatique 1', 40, 'labo', 'Bâtiment C'),
('LAB-INF2', 'Laboratoire Informatique 2', 40, 'labo', 'Bâtiment C'),
('SAL-SPEC', 'Salle Spéciale', 20, 'salle_spéciale', 'Bâtiment D')
ON CONFLICT (code_salle) DO NOTHING;

-- Professeurs
INSERT INTO professeurs (nom, prenom, dept_id, specialite) VALUES
('Dupont', 'Jean', 1, 'Informatique Théorique'),
('Martin', 'Marie', 1, 'Base de Données'),
('Bernard', 'Pierre', 2, 'Analyse Mathématique'),
('Petit', 'Sophie', 3, 'Physique Quantique'),
('Rousseau', 'Alain', 4, 'Chimie Organique'),
('Lemoine', 'Isabelle', 5, 'Biologie Cellulaire')
ON CONFLICT (email) DO NOTHING;

-- =============================================
-- UTILISATEURS PAR DÉFAUT (APRÈS RÔLES ET DÉPARTEMENTS)
-- =============================================

INSERT INTO utilisateurs (username, password_hash, email, role_id, departement_id) VALUES
('admin', '$5$rounds=535000$j8HZlBpEeZ5Ku0VP$HkF7F4L7d1Q5q7Y4X3n2m1K9j8H7G6F5E4D3C2B1A', 'admin@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Admin_examens'), NULL),
('vicedoyen', '$5$rounds=535000$j8HZlBpEeZ5Ku0VP$HkF7F4L7d1Q5q7Y4X3n2m1K9j8H7G6F5E4D3C2B1A', 'vicedoyen@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Vice-doyen'), NULL),
('doyen', '$5$rounds=535000$j8HZlBpEeZ5Ku0VP$HkF7F4L7d1Q5q7Y4X3n2m1K9j8H7G6F5E4D3C2B1A', 'doyen@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Doyen'), NULL),
('chef_info', '$5$rounds=535000$j8HZlBpEeZ5Ku0VP$HkF7F4L7d1Q5q7Y4X3n2m1K9j8H7G6F5E4D3C2B1A', 'chef.info@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Chef_departement'), 1),
('chef_math', '$5$rounds=535000$j8HZlBpEeZ5Ku0VP$HkF7F4L7d1Q5q7Y4X3n2m1K9j8H7G6F5E4D3C2B1A', 'chef.math@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Chef_departement'), 2)
ON CONFLICT (username) DO NOTHING;

-- =============================================
-- FONCTIONS ET TRIGGERS
-- =============================================

-- Fonction pour calculer l'heure de fin
CREATE OR REPLACE FUNCTION calculer_heure_fin()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcule l'heure de fin en ajoutant la durée
    NEW.heure_fin := NEW.heure_debut + (NEW.duree_minutes * INTERVAL '1 minute');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour calculer heure_fin automatiquement
CREATE TRIGGER trg_calculer_heure_fin
    BEFORE INSERT OR UPDATE OF heure_debut, duree_minutes ON examens
    FOR EACH ROW
    EXECUTE FUNCTION calculer_heure_fin();

-- Fonction pour updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour examens
CREATE TRIGGER trg_update_examens_updated_at
    BEFORE UPDATE ON examens
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Fonction pour mettre à jour nombre_inscrits
CREATE OR REPLACE FUNCTION update_nombre_inscrits()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' OR TG_OP = 'DELETE' THEN
        UPDATE examens e
        SET nombre_inscrits = (
            SELECT COUNT(DISTINCT i.etudiant_id)
            FROM inscriptions i
            WHERE i.module_id = e.module_id
        )
        WHERE e.module_id IN (
            SELECT COALESCE(NEW.module_id, OLD.module_id)
        );
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour inscriptions
CREATE TRIGGER trg_update_nombre_inscrits
    AFTER INSERT OR DELETE ON inscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_nombre_inscrits();

-- Fonction pour loguer les connexions
CREATE OR REPLACE FUNCTION log_connexion()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO connexions_log (utilisateur_id, ip_adresse, succes)
    VALUES (NEW.id, inet_client_addr(), TRUE);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour les connexions (optionnel)
-- CREATE TRIGGER trg_log_connexion
--     AFTER INSERT ON utilisateurs
--     FOR EACH ROW
--     EXECUTE FUNCTION log_connexion();

-- Fonction pour vérifier les permissions
CREATE OR REPLACE FUNCTION a_permission(
    user_role TEXT,
    permission_key TEXT,
    permission_value TEXT DEFAULT NULL
) RETURNS BOOLEAN AS $$
DECLARE
    user_permissions JSONB;
BEGIN
    SELECT permissions INTO user_permissions
    FROM roles WHERE nom = user_role;
    
    IF user_permissions IS NULL THEN
        RETURN FALSE;
    END IF;
    
    IF permission_value IS NULL THEN
        RETURN user_permissions ? permission_key;
    ELSE
        RETURN user_permissions->permission_key ? permission_value;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- =============================================
-- INDEXES POUR PERFORMANCE
-- =============================================

CREATE INDEX idx_inscriptions_module ON inscriptions(module_id);
CREATE INDEX idx_inscriptions_etudiant ON inscriptions(etudiant_id);
CREATE INDEX idx_exam_date ON examens(date_exam);
CREATE INDEX idx_exam_salle ON examens(salle_id);
CREATE INDEX idx_exam_module ON examens(module_id);
CREATE INDEX idx_exam_prof ON examens(prof_surveillant_id);
CREATE INDEX idx_exam_statut ON examens(statut);
CREATE INDEX idx_examens_composite ON examens(date_exam, heure_debut);
CREATE INDEX idx_salles_disponibles ON lieu_examen(id) WHERE disponible_examen = TRUE;
CREATE INDEX idx_exam_actifs ON examens(id) WHERE statut IN ('planifié', 'confirmé');

-- =============================================
-- VUES
-- =============================================

-- Vue statistiques globales
CREATE OR REPLACE VIEW vue_statistiques_globales AS
SELECT 
    (SELECT COUNT(*) FROM etudiants) as total_etudiants,
    (SELECT COUNT(*) FROM professeurs) as total_professeurs,
    (SELECT COUNT(*) FROM examens WHERE statut = 'planifié') as examens_planifies,
    (SELECT COUNT(DISTINCT date_exam) FROM examens) as jours_examens,
    (SELECT COUNT(*) FROM lieu_examen WHERE disponible_examen = TRUE) as salles_disponibles,
    (SELECT ROUND(COALESCE(AVG(nombre_inscrits), 0), 2) FROM examens) as moyenne_inscrits_par_examen;

-- Vue conflits étudiants
CREATE OR REPLACE VIEW vue_conflits_etudiants AS
SELECT 
    i.etudiant_id,
    e.nom || ' ' || e.prenom as etudiant,
    COUNT(DISTINCT ex.id) as nb_examens_jour,
    ex.date_exam,
    STRING_AGG(DISTINCT m.nom, ', ' ORDER BY m.nom) as modules
FROM inscriptions i
JOIN examens ex ON ex.module_id = i.module_id
JOIN etudiants e ON e.id = i.etudiant_id
JOIN modules m ON m.id = ex.module_id
WHERE ex.statut IN ('planifié', 'confirmé')
GROUP BY i.etudiant_id, e.nom, e.prenom, ex.date_exam
HAVING COUNT(DISTINCT ex.id) > 1;

-- Vue examens complets
CREATE OR REPLACE VIEW vue_examens_complets AS
SELECT 
    ex.id,
    ex.date_exam,
    ex.heure_debut,
    ex.heure_fin,
    ex.duree_minutes,
    m.nom AS module,
    m.code_module,
    f.nom AS formation,
    d.nom AS departement,
    p.nom || ' ' || COALESCE(p.prenom, '') AS professeur,
    l.nom AS salle,
    l.capacite,
    l.batiment,
    ex.nombre_inscrits,
    ex.statut,
    ex.statut_validation,
    u1.username as cree_par,
    u2.username as valide_par
FROM examens ex
JOIN modules m ON m.id = ex.module_id
JOIN formations f ON f.id = m.formation_id
JOIN departements d ON d.id = f.dept_id
JOIN professeurs p ON p.id = ex.prof_surveillant_id
JOIN lieu_examen l ON l.id = ex.salle_id
LEFT JOIN utilisateurs u1 ON ex.created_by = u1.id
LEFT JOIN utilisateurs u2 ON ex.validated_by = u2.id;

-- Vue examens à valider
CREATE OR REPLACE VIEW vue_examens_a_valider AS
SELECT 
    e.id,
    m.nom as module,
    f.nom as formation,
    d.nom as departement,
    e.date_exam,
    e.heure_debut,
    e.heure_fin,
    e.statut_validation,
    e.created_by,
    u.username as createur
FROM examens e
JOIN modules m ON e.module_id = m.id
JOIN formations f ON m.formation_id = f.id
JOIN departements d ON f.dept_id = d.id
LEFT JOIN utilisateurs u ON e.created_by = u.id
WHERE e.statut_validation = 'en_attente';

-- Vue dashboard par rôle
CREATE OR REPLACE VIEW vue_dashboard_par_role AS
SELECT 
    r.nom as role,
    COUNT(u.id) as nb_utilisateurs,
    r.niveau_acces
FROM roles r
LEFT JOIN utilisateurs u ON r.id = u.role_id
GROUP BY r.nom, r.niveau_acces;

-- =============================================
-- MESSAGE DE SUCCÈS
-- =============================================
-- 1. Ajouter la colonne utilisateur_id à la table etudiants
ALTER TABLE etudiants 
ADD COLUMN utilisateur_id INTEGER;

-- 2. Ajouter la contrainte de clé étrangère
ALTER TABLE etudiants 
ADD CONSTRAINT fk_etudiants_utilisateurs 
FOREIGN KEY (utilisateur_id) 
REFERENCES utilisateurs(id) 
ON DELETE CASCADE;

-- 3. Faire la même chose pour professeurs
ALTER TABLE professeurs 
ADD COLUMN utilisateur_id INTEGER;

ALTER TABLE professeurs 
ADD CONSTRAINT fk_professeurs_utilisateurs 
FOREIGN KEY (utilisateur_id) 
REFERENCES utilisateurs(id) 
ON DELETE CASCADE;
DO $$
BEGIN
    RAISE NOTICE '✅ Schéma créé avec succès !';
    RAISE NOTICE '📊 Tables créées: 12 tables';
    RAISE NOTICE '👥 Rôles insérés: 6 rôles';
    RAISE NOTICE '🏢 Départements: 7 départements';
    RAISE NOTICE '🏛️ Salles: 8 salles';
    RAISE NOTICE '👨‍🏫 Professeurs: 6 professeurs';
    RAISE NOTICE '👤 Utilisateurs: 5 utilisateurs par défaut';
    RAISE NOTICE '⚙️ Triggers créés: 3 triggers';
    RAISE NOTICE '👁️ Vues créées: 5 vues';
END $$;