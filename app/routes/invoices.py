from flask import Blueprint, request, jsonify
from app.models import db, Facture, FactureDetail, Produit, TVA
from datetime import datetime

invoices_bp = Blueprint('invoices', __name__)


@invoices_bp.route('/factures', methods=['POST'])
def create_facture():
    data = request.json
    facture = Facture(id_facture=data['id_facture'], id_client=data['id_client'],
                      date_facture=datetime.strptime(data['date_facture'], "%Y-%m-%d"),
                      date_echeance=datetime.strptime(data['date_echeance'], "%Y-%m-%d"))

    db.session.add(facture)

    # Add Facture Details
    for item in data['details']:
        produit = Produit.query.filter_by(id_produit=item['id_produit']).order_by(Produit.date_debut.desc()).first()
        if not produit:
            return jsonify({"error": "Produit not found"}), 404

        tva = TVA.query.get(produit.tva_id)
        total_ht = produit.prix_ht * item['quantite']

        detail = FactureDetail(id_facture=facture.id_facture, id_produit=produit.id_produit,
                               nom_produit=produit.nom_produit, tva_appliquee=tva.taux,
                               prix_unitaire_ht=produit.prix_ht, quantite=item['quantite'], total_ht=total_ht)
        db.session.add(detail)

    db.session.commit()
    return jsonify({"message": "Facture created successfully!"}), 201
