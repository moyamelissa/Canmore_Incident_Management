# =========================
# Titre : Route Flask - Rapport
# Explication : Gère les routes pour la page de rapport et les statistiques associées dans l'application Canmore Incident Management.
# =========================
# Importations
# Explication: Importation des modules nécessaires pour Flask
from flask import Blueprint, render_template, jsonify
import json
import os

# =========================
# Définition du Blueprint
# Explication: Création d'un blueprint pour la page de rapport
report_bp = Blueprint('report', __name__)

# =========================
# Chemin du dossier des données
# Explication: Définit le chemin vers le dossier contenant les fichiers de données GeoJSON
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../static/data')

# =========================
# Fonction utilitaire pour compter les entités d'un fichier GeoJSON
# Explication: Ouvre un fichier GeoJSON et retourne le nombre d'éléments dans "features"
def count_features(filename):
    with open(os.path.join(DATA_DIR, filename), encoding='utf-8') as f:
        data = json.load(f)
        return len(data['features'])

# =========================
# Route pour la page de rapport
# Explication: Définit la route qui affiche la page report.html
@report_bp.route('/report')
def report():
    return render_template('report.html')

# =========================
# Route pour les totaux par catégorie
# Explication: Retourne le nombre d'entités pour chaque catégorie de données (bâtiments, parcs, terrains de sport, sentiers)
@report_bp.route('/report/category_totals')
def category_totals():
    return jsonify({
        'buildings': count_features('buildings.geojson'),
        'parcs': count_features('parcs.geojson'),
        'sports_fields': count_features('sports_fields.geojson'),
        'trails': count_features('trails.geojson')
    })
