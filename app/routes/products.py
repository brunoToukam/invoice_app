from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import db, Produit

products_bp = Blueprint('products', __name__)


@products_bp.route('/products', methods=['POST'])
def add_product():
    data = request.json
    existing_product = Produit.query.filter(
        Produit.id_produit == data['id_produit'],
        Produit.date_fin is None  # Current active version
    ).first()

    if existing_product:
        # Set end date of the existing version
        existing_product.date_fin = datetime.today().date()

    # Insert the new version
    new_product = Produit(
        id_produit=data['id_produit'],
        nom_produit=data['nom_produit'],
        tva_id=data['tva_id'],
        prix_ht=data['prix_ht'],
        date_debut=datetime.today().date(),
        date_fin=None  # Newest version is active
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({"message": "Product version added successfully!"}), 201


@products_bp.route('/products', methods=['GET'])
def get_all_products():
    products = Produit.query.all()  # Retrieve all products
    if not products:
        return jsonify({"message": "No products found"}), 404

    products_list = []
    for product in products:
        products_list.append({
            "id_produit": product.id_produit,
            "nom_produit": product.nom_produit,
            "prix_ht": product.prix_ht,
            "tva_id": product.tva_id,
            "date_debut": product.date_debut.strftime("%Y-%m-%d"),
            "date_fin": product.date_fin.strftime("%Y-%m-%d") if product.date_fin else None
        })

    return jsonify(products_list), 200


@products_bp.route('/products/<id_produit>', methods=['GET'])
def get_product(id_produit):
    product = Produit.query.filter_by(id_produit=id_produit).order_by(Produit.date_debut.desc()).first()
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify({
        "id_produit": product.id_produit,
        "nom_produit": product.nom_produit,
        "prix_ht": product.prix_ht,
        "tva_id": product.tva_id,
        "date_debut": product.date_debut,
        "date_fin": product.date_fin
    })
