"""
main.py
Ce script initialise et lance l'application Flask Canmore Incident Management.
Il configure les blueprints (routes), les APIs, et démarre le serveur en mode développement.
"""

# Importation des modules nécessaires pour Flask et les routes de l'application
from flask import Flask, session, redirect, request, url_for
from server.routes.home_route import home_bp  # Page d'accueil
from server.routes.map_route import map_bp    # Page de la carte
from server.routes.report_route import report_bp  # Page de rapport
from server.routes.incident_types import incident_types_bp  # Types d'incidents
from server.routes.incidents_api import incidents_api  # API incidents
from server.routes.user_settings_api import user_settings_api  # API paramètres utilisateur
from flask_socketio import SocketIO, emit
import os

# Initialisation de l'application principale Flask

# Configuration de la clé secrète pour la gestion des sessions Flask
# Par défaut, une clé de développement est utilisée.
# Pour plus de sécurité en production, définissez la variable d'environnement FLASK_SECRET_KEY.
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-key-canmore')
socketio = SocketIO(app, cors_allowed_origins="*")

# Enregistrement des blueprints (routes) dans l'application Flask
from server.routes.info_route import info_bp  # Page d'informations
app.register_blueprint(home_bp)              # Accueil
app.register_blueprint(map_bp)               # Carte
app.register_blueprint(report_bp)            # Rapport
app.register_blueprint(incident_types_bp)    # Types d'incidents
app.register_blueprint(incidents_api)        # API incidents
app.register_blueprint(user_settings_api)    # API paramètres utilisateur
app.register_blueprint(info_bp)              # Informations

# Démarrage du serveur Flask (en mode debug pour le développement)
if __name__ == "__main__":
    socketio.run(app, debug=True)
