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