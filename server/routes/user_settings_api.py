'''
user_settings_api.py
Ce module définit les routes API Flask pour la gestion et la récupération
des préférences utilisateur (mode sombre, musique, etc.)
dans l'application Canmore Incident Management.
'''

from flask import Blueprint, request, jsonify
from config.user_settings import update_user_settings, get_user_settings

# Création d'un blueprint pour l'API des paramètres utilisateur
user_settings_api = Blueprint('user_settings_api', __name__)

@user_settings_api.route('/save_user_settings', methods=['POST'])
def save_settings():
    '''
    Enregistre ou met à jour les préférences utilisateur reçues en JSON.
    '''
    data = request.get_json()
    update_user_settings(data)
    return jsonify({'status': 'ok'})

@user_settings_api.route('/get_user_settings', methods=['GET'])
def get_settings():
    '''
    Retourne les préférences utilisateur enregistrées.
    '''
    settings = get_user_settings()
    return jsonify(settings)
