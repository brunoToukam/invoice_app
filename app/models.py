from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# 1. CLIENT TABLE
class Client(db.Model):
    __tablename__ = 'clients'
    id_client = db.Column(db.String, primary_key=True)
    nom_client = db.Column(db.String, nullable=False)
    adresse = db.Column(db.String, nullable=False)


# 2. FACTURE TABLE
class Facture(db.Model):
    __tablename__ = 'factures'
    id_facture = db.Column(db.String, primary_key=True)
    id_client = db.Column(db.String, db.ForeignKey('clients.id_client'), nullable=False)
    date_facture = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    date_echeance = db.Column(db.Date, nullable=False)

    client = db.relationship('Client', backref='factures')


# 3. TVA TABLE (SCD Type 2)
class TVA(db.Model):
    __tablename__ = 'tva'
    id_tva = db.Column(db.Integer, nullable=False)  # Part of composite key
    date_debut = db.Column(db.Date, nullable=False)  # Part of composite key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment ID
    taux = db.Column(db.Float, nullable=False)
    date_fin = db.Column(db.Date, nullable=True)  # Null means active


# 4. CATALOGUE_PRODUITS TABLE (SCD Type 2)
class Produit(db.Model):
    __tablename__ = 'catalogue_produits'
    id_produit = db.Column(db.String, nullable=False)  # Part of composite key
    date_debut = db.Column(db.Date, nullable=False)  # Part of composite key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Auto-increment ID
    nom_produit = db.Column(db.String, nullable=False)
    tva_id = db.Column(db.Integer, db.ForeignKey('tva.id_tva'), nullable=False)
    prix_ht = db.Column(db.Float, nullable=False)
    date_fin = db.Column(db.Date, nullable=True)

    tva = db.relationship('TVA', backref='produits')


# 5. FACTURE_DETAIL TABLE
class FactureDetail(db.Model):
    __tablename__ = 'facture_details'
    id_facture = db.Column(db.String, db.ForeignKey('factures.id_facture'), primary_key=True)
    id_produit = db.Column(db.String, db.ForeignKey('catalogue_produits.id_produit'), primary_key=True)
    nom_produit = db.Column(db.String, nullable=False)
    tva_appliquee = db.Column(db.Float, nullable=False)
    prix_unitaire_ht = db.Column(db.Float, nullable=False)
    quantite = db.Column(db.Integer, nullable=False)
    total_ht = db.Column(db.Float, nullable=False)

    facture = db.relationship('Facture', backref='details')
    produit = db.relationship('Produit', backref='details')
