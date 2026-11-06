-- Supprimer tous les utilisateurs existants
DELETE FROM utilisateurs;

-- Insérer des utilisateurs avec leurs hash SHA256
INSERT INTO utilisateurs (username, password_hash, email, role_id, departement_id) VALUES
-- admin / admin123
('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Admin_examens'), NULL),

-- admin2 / admin123 (même mot de passe)
('admin2', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin2@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Admin_examens'), NULL),

-- etudiant1 / etudiant123
('etudiant1', 'e4e5c8b8e9d2e2e8f8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8', 'etu00001@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Etudiant'), 1),

-- prof1 / prof123
('prof1', 'ccf5e6c8e9d2e2e8f8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8a8b8c8d8e8f8', 'prof1@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Professeur'), 1),

-- chef_info / chef123
('chef_info', 'd8e9f0a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8', 'chef.info@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Chef_departement'), 1);

-- Vérifier
SELECT username, email, role_id FROM utilisateurs ORDER BY username;


-- Insérer le Vice-doyen
INSERT INTO utilisateurs (username, password_hash, email, role_id, est_actif) VALUES
('vicedoyen', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'vicedoyen@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Vice-doyen'), true);

-- Insérer le Doyen admin123
INSERT INTO utilisateurs (username, password_hash, email, role_id, est_actif) VALUES
('doyen', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'doyen@umbb.dz', 
 (SELECT id FROM roles WHERE nom = 'Doyen'), true);

-- Insérer aussi l'admin si pas encore fait
INSERT INTO utilisateurs (username, password_hash, email, role_id, est_actif) 
SELECT 'admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'admin@umbb.dz', 
       id, true
FROM roles WHERE nom = 'Admin_examens'
AND NOT EXISTS (SELECT 1 FROM utilisateurs WHERE username = 'admin');



-- Hash SHA256 pour 'admin123' = 240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9

-- Créer quelques étudiants de test
INSERT INTO etudiants (nom, prenom, email, promo, specialite_id, niveau_courant_id, annee_etude) VALUES
('Dupont', 'Jean', 'jean.dupont@etudiant.umbb.dz', 2024, 1, 1, 1),
('Martin', 'Marie', 'marie.martin@etudiant.umbb.dz', 2024, 1, 1, 1),
('Bernard', 'Pierre', 'pierre.bernard@etudiant.umbb.dz', 2024, 2, 2, 2),
('Petit', 'Sophie', 'sophie.petit@etudiant.umbb.dz', 2024, 2, 2, 2);

-- Créer quelques professeurs de test
INSERT INTO professeurs (nom, prenom, email, specialite, quota_surveillance_journalier, heures_travail_semaine) VALUES
('Durand', 'Paul', 'paul.durand@umbb.dz', 'Informatique', 4, 20),
('Moreau', 'Catherine', 'catherine.moreau@umbb.dz', 'Mathématiques', 4, 20),
('Leroy', 'Thomas', 'thomas.leroy@umbb.dz', 'Physique', 4, 20);

-- Créer les comptes utilisateurs (mot de passe: admin123)
INSERT INTO utilisateurs (username, password_hash, role_id, email, est_actif) VALUES
('jean.dupont', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 4, 'jean.dupont@umbb.dz', true),
('marie.martin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 4, 'marie.martin@umbb.dz', true),
('pierre.bernard', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 4, 'pierre.bernard@umbb.dz', true),
('sophie.petit', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 4, 'sophie.petit@umbb.dz', true),
('paul.durand', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 3, 'paul.durand@umbb.dz', true),
('catherine.moreau', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 3, 'catherine.moreau@umbb.dz', true),
('thomas.leroy', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 3, 'thomas.leroy@umbb.dz', true);

-- Lier les comptes aux étudiants et professeurs
UPDATE etudiants SET utilisateur_id = (SELECT id FROM utilisateurs WHERE username = 'jean.dupont') WHERE email = 'jean.dupont@etudiant.umbb.dz';
UPDATE etudiants SET utilisateur_id = (SELECT id FROM utilisateurs WHERE username = 'marie.martin') WHERE email = 'marie.martin@etudiant.umbb.dz';
UPDATE etudiants SET utilisateur_id = (SELECT id FROM utilisateurs WHERE username = 'pierre.bernard') WHERE email = 'pierre.bernard@etudiant.umbb.dz';
UPDATE etudiants SET utilisateur_id = (SELECT id FROM utilisateurs WHERE username = 'sophie.petit') WHERE email = 'sophie.petit@etudiant.umbb.dz';

UPDATE professeurs SET utilisateur_id = (SELECT id FROM utilisateurs WHERE username = 'paul.durand') WHERE email = 'paul.durand@umbb.dz';
UPDATE professeurs SET utilisateur_id = (SELECT id FROM utilisateurs WHERE username = 'catherine.moreau') WHERE email = 'catherine.moreau@umbb.dz';
UPDATE professeurs SET utilisateur_id = (SELECT id FROM utilisateurs WHERE username = 'thomas.leroy') WHERE email = 'thomas.leroy@umbb.dz';



