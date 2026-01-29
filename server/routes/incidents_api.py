import requests

"""
=========================
 Titre : API Flask - Gestion des incidents
 Explication : Fournit les routes API pour ajouter, modifier, supprimer et lister les incidents dans la base de données SQLite pour l'application Canmore Incident Management.
=========================
"""

from flask import Blueprint, request, jsonify

import sqlite3
import os



# =========================
# Chemin du fichier de base de données
# Explication: Définit le chemin vers la base de données SQLite des incidents
DB_PATH = os.path.join(os.path.dirname(__file__), '../data/incidents.db')


# =========================
# Définition du Blueprint
# Explication: Création d'un blueprint pour l'API incidents
incidents_api = Blueprint('incidents_api', __name__)


# =========================
# Connexion à la base de données
# Explication: Fonction utilitaire pour obtenir une connexion à la base de données SQLite
def get_db_connection():
	conn = sqlite3.connect(DB_PATH)
	conn.row_factory = sqlite3.Row
	return conn


# =========================
# Initialisation de la base de données
# Explication: Crée la table incidents si elle n'existe pas et ajoute la colonne status si besoin
def init_db():
	conn = get_db_connection()
	# Crée la table incidents avec toutes les colonnes nécessaires
	conn.execute('''
		CREATE TABLE IF NOT EXISTS incidents (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			type TEXT NOT NULL,
			description TEXT,
			latitude REAL NOT NULL,
			longitude REAL NOT NULL,
			timestamp TEXT NOT NULL,
			status TEXT DEFAULT 'unsolved'
		)
	''')
	# Ajoute la colonne status si elle n'existe pas déjà (pour les anciennes bases)
	try:
		conn.execute("ALTER TABLE incidents ADD COLUMN status TEXT DEFAULT 'unsolved'")
	except Exception:
		pass  # Ignore si déjà présente
	conn.commit()
	conn.close()

# =========================
# Initialisation au démarrage
# Explication: Lance l'initialisation de la base de données au démarrage du module
init_db()

# =========================
# Route DELETE : Supprimer un incident
# Explication: Supprime un incident de la base de données à partir de son ID
@incidents_api.route('/api/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
	conn = get_db_connection()
	conn.execute('DELETE FROM incidents WHERE id = ?', (incident_id,))
	conn.commit()
	conn.close()
	# Notify websocket server for live update
	try:
		requests.post('http://localhost:8001/broadcast', json={"message": "incident_deleted"}, timeout=1)
	except Exception:
		pass
	return jsonify({'message': 'Incident supprimé avec succès'}), 200


# =========================
# Route PATCH : Mettre à jour le statut d'un incident
# Explication: Met à jour le statut (résolu/non résolu) d'un incident existant
@incidents_api.route('/api/incidents/<int:incident_id>', methods=['PATCH'])
def update_incident_status(incident_id):
	import sys
	print(f"PATCH /api/incidents/{incident_id} appelé", file=sys.stderr)
	data = request.get_json()
	print(f"Données reçues : {data}", file=sys.stderr)
	if 'status' not in data:
		print("Champ status manquant", file=sys.stderr)
		return jsonify({'error': 'Champ status manquant'}), 400
	conn = get_db_connection()
	conn.execute('UPDATE incidents SET status = ? WHERE id = ?', (data['status'], incident_id))
	conn.commit()
	conn.close()
	print("Statut de l'incident mis à jour avec succès", file=sys.stderr)
	# Notify websocket server for live update
	try:
		requests.post('http://localhost:8001/broadcast', json={"message": "incident_updated"}, timeout=1)
	except Exception:
		pass
	return jsonify({'message': "Statut de l'incident mis à jour avec succès"}), 200


# =========================
# Route POST : Ajouter un nouvel incident
# Explication: Ajoute un nouvel incident à la base de données
@incidents_api.route('/api/incidents', methods=['POST'])
def add_incident():
	data = request.get_json()
	required_fields = ['type', 'description', 'latitude', 'longitude', 'timestamp']
	# Vérifie que tous les champs obligatoires sont présents
	if not all(field in data for field in required_fields):
		return jsonify({'error': 'Champs manquants'}), 400
	status = data.get('status', 'unsolved')
	conn = get_db_connection()
	conn.execute(
		'INSERT INTO incidents (type, description, latitude, longitude, timestamp, status) VALUES (?, ?, ?, ?, ?, ?)',
		(data['type'], data['description'], data['latitude'], data['longitude'], data['timestamp'], status)
	)
	conn.commit()
	conn.close()
	# Notify websocket server for live update
	try:
		requests.post('http://localhost:8001/broadcast', json={"message": "incident_added"}, timeout=1)
	except Exception:
		pass
	return jsonify({'message': 'Incident ajouté avec succès'}), 201


# =========================
# Route GET : Récupérer tous les incidents
# Explication: Retourne la liste de tous les incidents enregistrés dans la base de données
@incidents_api.route('/api/incidents', methods=['GET'])
def get_incidents():
	conn = get_db_connection()
	incidents = conn.execute('SELECT * FROM incidents').fetchall()
	conn.close()
	incidents_list = [dict(row) for row in incidents]
	return jsonify(incidents_list)
