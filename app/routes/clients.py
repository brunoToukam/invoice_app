from flask import Blueprint, request, jsonify
from app.models import db, Client

clients_bp = Blueprint('clients', __name__)


@clients_bp.route('/clients', methods=['POST'])
def add_client():
    data = request.json
    client = Client(id_client=data['id_client'], nom_client=data['nom_client'], adresse=data['adresse'])
    db.session.add(client)
    db.session.commit()
    return jsonify({"message": "Client added successfully!"}), 201


@clients_bp.route('/clients/<id_client>', methods=['GET'])
def get_client(id_client):
    client = Client.query.get(id_client)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify({"id_client": client.id_client, "nom_client": client.nom_client, "adresse": client.adresse})
