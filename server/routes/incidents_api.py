'''
incidents_api.py
Ce module définit les routes API Flask pour la gestion des incidents :
ajout, modification, suppression et récupération des incidents dans la base SQLite
pour l'application Canmore Incident Management.
'''

import requests
from flask import Blueprint, request, jsonify
import sqlite3
import os

# Chemin du fichier de base de données SQLite des incidents
# Assure que le répertoire data/ existe
DATA_DIR = os.path.join(os.path.dirname(__file__), '../data')
os.makedirs(DATA_DIR, exist_ok=True)

DB_PATH = os.path.join(DATA_DIR, 'incidents.db')

# Création d'un blueprint pour l'API incidents
incidents_api = Blueprint('incidents_api', __name__)

def get_db_connection():
    '''
    Ouvre une connexion à la base de données SQLite et configure le retour sous forme de dictionnaire.
    '''
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    '''
    Initialise la base de données : crée la table incidents si besoin et ajoute la colonne status si absente.
    '''
    conn = get_db_connection()
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
    try:
        conn.execute("ALTER TABLE incidents ADD COLUMN status TEXT DEFAULT 'unsolved'")
    except Exception:
        pass  # Ignore si déjà présente
    conn.commit()
    conn.close()

# Initialisation de la base de données au démarrage du module
init_db()

@incidents_api.route('/api/incidents/<int:incident_id>', methods=['DELETE'])
def delete_incident(incident_id):
    '''
    Supprime un incident de la base de données à partir de son ID.
    '''
    conn = get_db_connection()
    conn.execute('DELETE FROM incidents WHERE id = ?', (incident_id,))
    conn.commit()
    conn.close()
    # Notifie le serveur websocket pour la mise à jour en temps réel
    try:
        requests.post('http://localhost:8001/broadcast', json={"message": "incident_deleted"}, timeout=1)
    except Exception:
        pass
    return jsonify({'message': 'Incident supprimé avec succès'}), 200

@incidents_api.route('/api/incidents/<int:incident_id>', methods=['PATCH'])
def update_incident_status(incident_id):
    '''
    Met à jour le statut (résolu/non résolu) d'un incident existant.
    '''
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
    # Notifie le serveur websocket pour la mise à jour en temps réel
    try:
        requests.post('http://localhost:8001/broadcast', json={"message": "incident_updated"}, timeout=1)
    except Exception:
        pass
    return jsonify({'message': "Statut de l'incident mis à jour avec succès"}), 200

@incidents_api.route('/api/incidents', methods=['POST'])
def add_incident():
    '''
    Ajoute un nouvel incident à la base de données.
    '''
    data = request.get_json()
    required_fields = ['type', 'description', 'latitude', 'longitude', 'timestamp']
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
    # Notifie le serveur websocket pour la mise à jour en temps réel
    try:
        requests.post('http://localhost:8001/broadcast', json={"message": "incident_added"}, timeout=1)
    except Exception:
        pass
    return jsonify({'message': 'Incident ajouté avec succès'}), 201

@incidents_api.route('/api/incidents', methods=['GET'])
def get_incidents():
    '''
    Retourne la liste de tous les incidents enregistrés dans la base de données.
    '''
    conn = get_db_connection()
    incidents = conn.execute('SELECT * FROM incidents').fetchall()
    conn.close()
    incidents_list = [dict(row) for row in incidents]
    return jsonify(incidents_list)
