-- Schéma de base de données pour un système de facturation simple

-- Table pour stocker les informations sur les clients
CREATE TABLE Clients (
    ClientID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Nom VARCHAR(255) NOT NULL,
    Adresse VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Telephone VARCHAR(50)
);

-- Table pour stocker les produits ou services
CREATE TABLE Produits (
    ProduitID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    Nom VARCHAR(255) NOT NULL,
    Description TEXT,
    PrixUnitaire NUMERIC(10, 2) NOT NULL CHECK (PrixUnitaire >= 0) -- Ajout d'une contrainte de vérification
);

-- Table pour les factures
CREATE TABLE Factures (
    FactureID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    ClientID INT NOT NULL,
    DateFacture DATE NOT NULL DEFAULT CURRENT_DATE,
    DateEcheance DATE,
    Statut VARCHAR(50) DEFAULT 'Non payée', -- Ex: 'Payée', 'Annulée'
    FOREIGN KEY (ClientID) REFERENCES Clients(ClientID)
);

-- Table de liaison pour les lignes de facture (détails de la facture)
-- C'est une table de jonction entre Factures et Produits
CREATE TABLE LignesFacture (
    LigneFactureID INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    FactureID INT NOT NULL,
    ProduitID INT NOT NULL,
    Quantite INT NOT NULL CHECK (Quantite > 0),
    PrixTotal NUMERIC(10, 2) NOT NULL, -- Calculé : Quantite * PrixUnitaire du produit au moment de la facturation
    FOREIGN KEY (FactureID) REFERENCES Factures(FactureID),
    FOREIGN KEY (ProduitID) REFERENCES Produits(ProduitID)
);

-- Création d'index pour améliorer les performances des requêtes
CREATE INDEX idx_factures_clientid ON Factures(ClientID);
CREATE INDEX idx_lignesfacture_factureid ON LignesFacture(FactureID);
CREATE INDEX idx_lignesfacture_produitid ON LignesFacture(ProduitID);
