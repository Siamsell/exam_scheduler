-- =============================================
-- INDEXES OPTIMISÉS POUR SQL SERVER
-- =============================================

-- Index de base pour les requêtes fréquentes
CREATE INDEX idx_inscriptions_module ON inscriptions(module_id);
CREATE INDEX idx_inscriptions_etudiant ON inscriptions(etudiant_id);
CREATE INDEX idx_exam_date ON examens(date_exam);
CREATE INDEX idx_exam_module ON examens(module_id);
CREATE INDEX idx_exam_prof ON examens(prof_surveillant_id);
CREATE INDEX idx_exam_salle ON examens(salle_id);
CREATE INDEX idx_exam_statut ON examens(statut);
GO

-- Index composites pour les jointures complexes
CREATE INDEX idx_inscriptions_composite 
ON inscriptions(etudiant_id, module_id) 
INCLUDE (annee_academique);
GO

CREATE INDEX idx_examens_composite 
ON examens(date_exam, heure_debut) 
INCLUDE (salle_id, module_id, prof_surveillant_id);
GO

CREATE INDEX idx_modules_composite 
ON modules(formation_id, prof_responsable_id) 
INCLUDE (nom, credits);
GO

-- Index filtrés pour les requêtes spécifiques
CREATE INDEX idx_examens_actifs 
ON examens(id) 
WHERE statut IN ('planifié', 'confirmé');
GO

CREATE INDEX idx_salles_disponibles 
ON lieu_examen(id) 
WHERE disponible_examen = 1;
GO

-- Index pour les recherches textuelles
CREATE INDEX idx_modules_nom ON modules(nom);
CREATE INDEX idx_etudiants_nom ON etudiants(nom);
CREATE INDEX idx_professeurs_nom ON professeurs(nom);
GO

-- Index pour les agrégations
CREATE INDEX idx_examens_agregation 
ON examens(statut, date_exam) 
INCLUDE (module_id, salle_id, nombre_inscrits);
GO

CREATE INDEX idx_inscriptions_agregation 
ON inscriptions(module_id, annee_academique) 
INCLUDE (etudiant_id);
GO

-- Index pour les contraintes d'unicité
CREATE INDEX idx_unique_salle_horaire 
ON examens(salle_id, date_exam, heure_debut);
GO

-- Index pour les dates (optimisation des requêtes temporelles)
CREATE INDEX idx_examens_date_range 
ON examens(date_exam) 
INCLUDE (heure_debut, heure_fin, statut);
GO

-- Statistiques pour l'optimiseur de requêtes
UPDATE STATISTICS examens WITH FULLSCAN;
UPDATE STATISTICS inscriptions WITH FULLSCAN;
UPDATE STATISTICS modules WITH FULLSCAN;
UPDATE STATISTICS etudiants WITH FULLSCAN;
GO

-- Vérification des index créés
PRINT '=========================================';
PRINT '📊 INDEXES CRÉÉS AVEC SUCCÈS';
PRINT '=========================================';
PRINT 'Total d''index créés:';
PRINT '- 8 index de base';
PRINT '- 3 index composites';
PRINT '- 2 index filtrés';
PRINT '- 3 index de recherche textuelle';
PRINT '- 2 index d''agrégation';
PRINT '=========================================';