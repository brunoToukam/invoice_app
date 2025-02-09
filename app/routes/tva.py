from flask import Blueprint, request, jsonify
from datetime import datetime
from app.models import db, TVA

tva_bp = Blueprint('tva', __name__)


@tva_bp.route('/tva', methods=['POST'])
def add_tva():
    data = request.json
    existing_tva = TVA.query.filter(
        TVA.date_fin is None  # Current active TVA
    ).first()

    if existing_tva:
        existing_tva.date_fin = datetime.today().date()  # Closing previous record

    # Insert the new version
    new_tva = TVA(
        taux=data['taux'],
        date_debut=datetime.today().date(),
        date_fin=None  # Active rate
    )

    db.session.add(new_tva)
    db.session.commit()

    return jsonify({"message": "New TVA rate added successfully!"}), 201


@tva_bp.route('/tva/latest', methods=['GET'])
def get_latest_tva():
    latest_tva = TVA.query.order_by(TVA.date_debut.desc()).first()
    if not latest_tva:
        return jsonify({"error": "No TVA found"}), 404
    return jsonify({
        "id_tva": latest_tva.id_tva,
        "taux": latest_tva.taux,
        "date_debut": latest_tva.date_debut,
        "date_fin": latest_tva.date_fin
    })
