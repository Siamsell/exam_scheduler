-- 1. Désactiver les contraintes temporairement
ALTER TABLE formations DISABLE TRIGGER ALL;
ALTER TABLE modules DISABLE TRIGGER ALL;
ALTER TABLE inscriptions DISABLE TRIGGER ALL;
ALTER TABLE examens DISABLE TRIGGER ALL;

-- 2. Vider toutes les tables (exécuter cette partie seule)
TRUNCATE TABLE examens_historique CASCADE;
TRUNCATE TABLE connexions_log CASCADE;
TRUNCATE TABLE inscriptions CASCADE;
TRUNCATE TABLE examens CASCADE;
TRUNCATE TABLE modules CASCADE;
TRUNCATE TABLE etudiants CASCADE;
TRUNCATE TABLE formations CASCADE;
TRUNCATE TABLE professeurs CASCADE;
TRUNCATE TABLE utilisateurs CASCADE;
TRUNCATE TABLE roles CASCADE;
TRUNCATE TABLE lieu_examen CASCADE;
TRUNCATE TABLE departements CASCADE;

-- 3. Réinitialiser les séquences (exécuter cette partie seule)
ALTER SEQUENCE IF EXISTS departements_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS formations_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS etudiants_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS modules_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS examens_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS professeurs_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS utilisateurs_id_seq RESTART WITH 1;
ALTER SEQUENCE IF EXISTS roles_id_seq RESTART WITH 1;


-- 4. Insérer les 7 départements (exécuter cette partie seule)
INSERT INTO departements (nom) VALUES 
('Informatique'),
('Mathématiques'),
('Physique'),
('Chimie'),
('Biologie'),
('Sciences de l''Ingénieur'),
('Langues et Littérature');

-- Vérifier
SELECT '✅ Départements créés' as message, COUNT(*) as nombre FROM departements;
SELECT id, nom FROM departements ORDER BY id;


-- 5. Insérer les rôles (exécuter cette partie seule)
INSERT INTO roles (nom, description, niveau_acces) VALUES
('Admin_examens', 'Administrateur des examens', 4),
('Chef_departement', 'Chef de département', 3),
('Professeur', 'Enseignant', 2),
('Etudiant', 'Étudiant', 1);

-- Vérifier
SELECT '✅ Rôles créés' as message, COUNT(*) as nombre FROM roles;


-- 6. Insérer les salles d'examen (exécuter cette partie seule)
INSERT INTO lieu_examen (code_salle, nom, capacite, type, batiment) VALUES
('AMPHI-A', 'Amphithéâtre A', 300, 'amphi', 'Bâtiment Principal'),
('SAL-101', 'Salle 101', 50, 'salle', 'Bâtiment B'),
('SAL-102', 'Salle 102', 50, 'salle', 'Bâtiment B'),
('SAL-103', 'Salle 103', 30, 'salle', 'Bâtiment B'),
('LAB-INFO', 'Laboratoire Informatique', 40, 'labo', 'Bâtiment C');

-- Vérifier
SELECT '✅ Salles créées' as message, COUNT(*) as nombre FROM lieu_examen;




-- 7. Insérer les professeurs (exécuter cette partie seule)
INSERT INTO professeurs (nom, prenom, dept_id, specialite) VALUES
-- Informatique (dept_id = 1)
('Dupont', 'Jean', 1, 'Informatique'),
('Martin', 'Marie', 1, 'Programmation'),
('Bernard', 'Paul', 1, 'Réseaux'),
('Thomas', 'Luc', 1, 'Base de données'),
-- Mathématiques (dept_id = 2)
('Petit', 'Sophie', 2, 'Mathématiques'),
('Robert', 'Alain', 2, 'Statistiques'),
('Richard', 'Pierre', 2, 'Algèbre'),
-- Physique (dept_id = 3)
('Durand', 'Claire', 3, 'Physique'),
('Dubois', 'Marc', 3, 'Mécanique'),
-- Chimie (dept_id = 4)
('Moreau', 'Isabelle', 4, 'Chimie'),
('Laurent', 'David', 4, 'Biochimie'),
-- Biologie (dept_id = 5)
('Simon', 'Julie', 5, 'Biologie'),
('Michel', 'Anne', 5, 'Génétique'),
-- Sciences Ingénieur (dept_id = 6)
('Lefebvre', 'Philippe', 6, 'Génie Civil'),
('Girard', 'Nathalie', 6, 'Génie Mécanique'),
-- Langues (dept_id = 7)
('Roux', 'Catherine', 7, 'Littérature'),
('Vincent', 'François', 7, 'Linguistique');

-- Ajouter 33 autres professeurs
INSERT INTO professeurs (nom, prenom, dept_id, specialite)
SELECT 
    CASE (i % 8)
        WHEN 0 THEN 'Mercier'
        WHEN 1 THEN 'Faure'
        WHEN 2 THEN 'Blanc'
        WHEN 3 THEN 'Perrin'
        WHEN 4 THEN 'Robin'
        WHEN 5 THEN 'Clement'
        WHEN 6 THEN 'Morin'
        WHEN 7 THEN 'Gauthier'
    END,
    CASE (i % 5)
        WHEN 0 THEN 'Alexandre'
        WHEN 1 THEN 'Benoît'
        WHEN 2 THEN 'Camille'
        WHEN 3 THEN 'Élodie'
        WHEN 4 THEN 'Gabriel'
    END,
    ((i % 7) + 1),
    'Professeur ' || i
FROM generate_series(1, 33) i;

-- Vérifier
SELECT '✅ Professeurs créés' as message, COUNT(*) as nombre FROM professeurs;
SELECT dept_id, COUNT(*) as nb_professeurs FROM professeurs GROUP BY dept_id ORDER BY dept_id;


-- 8. Créer 30 formations par département (exécuter cette partie seule)
DO $$
DECLARE
    dept_id_val INTEGER;
    i INTEGER;
    j INTEGER := 1;
BEGIN
    -- Pour chaque département (1 à 7)
    FOR dept_id_val IN 1..7 LOOP
        -- Créer 30 formations par département
        FOR i IN 1..30 LOOP
            INSERT INTO formations (nom, dept_id, nb_modules, code_formation) VALUES (
                CASE (i % 3)
                    WHEN 0 THEN 'Licence '
                    WHEN 1 THEN 'Master '
                    WHEN 2 THEN 'Doctorat '
                END ||
                CASE dept_id_val
                    WHEN 1 THEN 'Informatique '
                    WHEN 2 THEN 'Mathématiques '
                    WHEN 3 THEN 'Physique '
                    WHEN 4 THEN 'Chimie '
                    WHEN 5 THEN 'Biologie '
                    WHEN 6 THEN 'Sciences de l''Ingénieur '
                    WHEN 7 THEN 'Langues et Littérature '
                END ||
                CASE (i % 5)
                    WHEN 0 THEN 'Fondamentale'
                    WHEN 1 THEN 'Appliquée'
                    WHEN 2 THEN 'Avancée'
                    WHEN 3 THEN 'Spécialisée'
                    WHEN 4 THEN 'Professionnelle'
                END,
                dept_id_val,
                6 + (i % 4), -- 6 à 9 modules
                'FORM-' || LPAD(dept_id_val::text, 2, '0') || '-' || LPAD(j::text, 3, '0')
            );
            j := j + 1;
        END LOOP;
    END LOOP;
END $$;

-- Vérifier
SELECT '✅ Formations créées' as message, COUNT(*) as nombre FROM formations;
SELECT dept_id, COUNT(*) as nb_formations FROM formations GROUP BY dept_id ORDER BY dept_id;





-- 9. Créer les modules pour chaque formation (exécuter cette partie seule)
DO $$
DECLARE
    formation_record RECORD;
    module_index INTEGER;
    prof_id_val INTEGER;
BEGIN
    FOR formation_record IN SELECT id, dept_id, nb_modules FROM formations ORDER BY id LOOP
        -- Créer nb_modules modules pour cette formation
        FOR module_index IN 1..formation_record.nb_modules LOOP
            -- Trouver un professeur du même département
            SELECT id INTO prof_id_val 
            FROM professeurs 
            WHERE dept_id = formation_record.dept_id 
            ORDER BY RANDOM() 
            LIMIT 1;
            
            IF prof_id_val IS NULL THEN
                prof_id_val := 1; -- Fallback
            END IF;
            
            INSERT INTO modules (code_module, nom, credits, formation_id, prof_responsable_id, semestre, volume_horaire)
            VALUES (
                'MOD-' || LPAD(formation_record.id::text, 3, '0') || '-' || LPAD(module_index::text, 2, '0'),
                'Module ' || module_index || ' - Formation ' || formation_record.id,
                CASE (module_index % 3)
                    WHEN 0 THEN 6
                    WHEN 1 THEN 9
                    WHEN 2 THEN 12
                END,
                formation_record.id,
                prof_id_val,
                CASE WHEN module_index <= formation_record.nb_modules/2 THEN 1 ELSE 2 END,
                CASE (module_index % 3)
                    WHEN 0 THEN 30
                    WHEN 1 THEN 45
                    WHEN 2 THEN 60
                END
            );
        END LOOP;
    END LOOP;
END $$;

-- Vérifier
SELECT '✅ Modules créés' as message, COUNT(*) as nombre FROM modules;
SELECT formation_id, COUNT(*) as nb_modules FROM modules GROUP BY formation_id
	ORDER BY formation_id LIMIT 10;



-- 10. Créer 13,000 étudiants (exécuter cette partie seule)
INSERT INTO etudiants (nom, prenom, email, formation_id, promo, annee_etude)
SELECT 
    -- Noms algériens
    CASE (i % 25)
        WHEN 0 THEN 'Benali'
        WHEN 1 THEN 'Bouzid'
        WHEN 2 THEN 'Chaoui'
        WHEN 3 THEN 'Haddad'
        WHEN 4 THEN 'Hamidi'
        WHEN 5 THEN 'Kaci'
        WHEN 6 THEN 'Mansouri'
        WHEN 7 THEN 'Nasri'
        WHEN 8 THEN 'Saadi'
        WHEN 9 THEN 'Taleb'
        WHEN 10 THEN 'Zeroual'
        WHEN 11 THEN 'Ait'
        WHEN 12 THEN 'Cherif'
        WHEN 13 THEN 'Fares'
        WHEN 14 THEN 'Gharbi'
        WHEN 15 THEN 'Lounis'
        WHEN 16 THEN 'Ouali'
        WHEN 17 THEN 'Rabah'
        WHEN 18 THEN 'Slimani'
        WHEN 19 THEN 'Touati'
        WHEN 20 THEN 'Yahiaoui'
        WHEN 21 THEN 'Ziane'
        WHEN 22 THEN 'Belkacem'
        WHEN 23 THEN 'Dahmane'
        WHEN 24 THEN 'Mammeri'
    END,
    -- Prénoms
    CASE (i % 20)
        WHEN 0 THEN 'Mohamed'
        WHEN 1 THEN 'Ahmed'
        WHEN 2 THEN 'Karim'
        WHEN 3 THEN 'Rachid'
        WHEN 4 THEN 'Youssef'
        WHEN 5 THEN 'Samir'
        WHEN 6 THEN 'Farid'
        WHEN 7 THEN 'Bilal'
        WHEN 8 THEN 'Leila'
        WHEN 9 THEN 'Fatima'
        WHEN 10 THEN 'Nadia'
        WHEN 11 THEN 'Sofia'
        WHEN 12 THEN 'Aicha'
        WHEN 13 THEN 'Salima'
        WHEN 14 THEN 'Nour'
        WHEN 15 THEN 'Yasmina'
        WHEN 16 THEN 'Ines'
        WHEN 17 THEN 'Ryma'
        WHEN 18 THEN 'Samira'
        WHEN 19 THEN 'Zahra'
    END,
    -- Email
    'etu' || LPAD(i::text, 5, '0') || '@umbb.dz',
    -- Formation (réparti sur 210 formations)
    ((i % 210) + 1),
    -- Promo (2022-2024)
    (2022 + (i % 3)),
    -- Année d'étude (1-3)
    ((i % 3) + 1)
FROM generate_series(1, 13000) i;

-- Vérifier
SELECT '✅ Étudiants créés' as message, COUNT(*) as nombre FROM etudiants;
SELECT formation_id, COUNT(*) as nb_etudiants FROM etudiants GROUP BY formation_id ORDER BY nb_etudiants DESC LIMIT 10;





-- 11. Créer les inscriptions aux modules (exécuter cette partie seule)
INSERT INTO inscriptions (etudiant_id, module_id, annee_academique, note)
SELECT 
    e.id,
    m.id,
    2024,
    CASE 
        WHEN RANDOM() > 0.4 THEN (8 + (RANDOM() * 12))::DECIMAL(4,2) -- Notes entre 8 et 20
        ELSE NULL -- Certains n'ont pas encore de note
    END
FROM etudiants e
JOIN modules m ON m.formation_id = e.formation_id
WHERE RANDOM() < 0.6 -- 60% de chance d'être inscrit à un module
LIMIT 50000; -- Limiter à 50,000 inscriptions

-- Vérifier
SELECT '✅ Inscriptions créées' as message, COUNT(*) as nombre FROM inscriptions;
SELECT AVG(note) as moyenne_notes FROM inscriptions WHERE note IS NOT NULL;




-- 13. Créer des utilisateurs (exécuter cette partie seule)
INSERT INTO utilisateurs (username, password_hash, email, role_id, departement_id) VALUES
('admin', '$2a$10$hashedpassword', 'admin@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Admin_examens'), NULL),
('chef_info', '$2a$10$hashedpassword', 'chef.info@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Chef_departement'), 1),
('prof_dupont', '$2a$10$hashedpassword', 'prof.dupont@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Professeur'), 1),
('etudiant1', '$2a$10$hashedpassword', 'etu00001@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Etudiant'), 1);

-- Vérifier
SELECT '✅ Utilisateurs créés' as message, COUNT(*) as nombre FROM utilisateurs;

-- 14. Réactiver toutes les contraintes (exécuter cette partie seule)
ALTER TABLE formations ENABLE TRIGGER ALL;
ALTER TABLE modules ENABLE TRIGGER ALL;
ALTER TABLE inscriptions ENABLE TRIGGER ALL;
ALTER TABLE examens ENABLE TRIGGER ALL



CREATE TABLE planning_automatique (
    id SERIAL PRIMARY KEY,
    nom_planning VARCHAR(200) NOT NULL,
    module_id INTEGER REFERENCES modules(id),
    specialite_id INTEGER REFERENCES specialites(id),
    date_exam DATE NOT NULL,
    heure_debut TIME NOT NULL,
    heure_fin TIME NOT NULL,
    salle_id INTEGER REFERENCES lieu_examen(id),
    surveillants_ids INTEGER[] NOT NULL,
    nb_surveillants INTEGER NOT NULL,
    nb_inscrits INTEGER NOT NULL,
    statut VARCHAR(50) DEFAULT 'en_attente',
    created_by INTEGER REFERENCES utilisateurs(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validated_by INTEGER REFERENCES utilisateurs(id),
    validated_at TIMESTAMP,
    notes TEXT
);