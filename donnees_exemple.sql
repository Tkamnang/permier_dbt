-- Script pour insérer des données d'exemple dans la base de données de facturation

-- Insertion des clients
INSERT INTO Clients (Nom, Adresse, Email, Telephone) VALUES
('Jean Dupont', '123 Rue de la République, 75001 Paris', 'jean.dupont@email.com', '0123456789'),
('Marie Curie', '45 Avenue des Sciences, 91190 Gif-sur-Yvette', 'marie.curie@email.com', '0987654321'),
('Victor Hugo', '6 Place des Vosges, 75004 Paris', 'victor.hugo@email.com', '0612345678');

-- Insertion des produits
INSERT INTO Produits (Nom, Description, PrixUnitaire) VALUES
('Développement Web', 'Création d''un site web vitrine (5 pages)', 1500.00),
('Hébergement Web', 'Abonnement annuel pour l''hébergement du site', 120.00),
('Maintenance de site', 'Forfait mensuel de maintenance technique', 80.00),
('Rédaction de contenu', 'Rédaction de 3 articles de blog optimisés SEO', 300.00),
('Logo Design', 'Création d''un logo personnalisé', 450.00);

-- Insertion des factures
-- Facture 1 pour Jean Dupont
INSERT INTO Factures (ClientID, DateFacture, DateEcheance, Statut) VALUES
(1, '2023-10-01', '2023-10-31', 'Payée');

-- Facture 2 pour Marie Curie
INSERT INTO Factures (ClientID, DateFacture, DateEcheance, Statut) VALUES
(2, '2023-10-15', '2023-11-15', 'Non payée');

-- Facture 3 pour Jean Dupont (une autre)
INSERT INTO Factures (ClientID, DateFacture, DateEcheance, Statut) VALUES
(1, '2023-11-05', '2023-12-05', 'Non payée');

-- Insertion des lignes de facture

-- Lignes pour la Facture 1 (ID: 1)
INSERT INTO LignesFacture (FactureID, ProduitID, Quantite, PrixTotal) VALUES
(1, 1, 1, 1500.00), -- 1x Développement Web
(1, 2, 1, 120.00);  -- 1x Hébergement Web

-- Lignes pour la Facture 2 (ID: 2)
INSERT INTO LignesFacture (FactureID, ProduitID, Quantite, PrixTotal) VALUES
(2, 5, 1, 450.00), -- 1x Logo Design
(2, 4, 2, 600.00);  -- 2x Rédaction de contenu

-- Lignes pour la Facture 3 (ID: 3)
INSERT INTO LignesFacture (FactureID, ProduitID, Quantite, PrixTotal) VALUES
(3, 3, 3, 240.00); -- 3x Maintenance de site

-- Pour voir les résultats, vous pouvez utiliser des requêtes SELECT.
-- Par exemple, pour voir le détail d'une facture :
/*
SELECT
    f.FactureID,
    f.DateFacture,
    c.Nom AS NomClient,
    p.Nom AS Produit,
    lf.Quantite,
    lf.PrixTotal
FROM Factures f
JOIN Clients c ON f.ClientID = c.ClientID
JOIN LignesFacture lf ON f.FactureID = lf.FactureID
JOIN Produits p ON lf.ProduitID = p.ProduitID
WHERE f.FactureID = 2;
*/
