'''
report_route.py
Ce module définit les routes Flask pour la page de rapport et les statistiques associées
dans l'application Canmore Incident Management.
'''

from flask import Blueprint, render_template, jsonify
import json
import os

# Création d'un blueprint pour la page de rapport
report_bp = Blueprint('report', __name__)

# Chemin du dossier contenant les fichiers de données GeoJSON
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../static/data')

def count_features(filename):
    '''
    Ouvre un fichier GeoJSON et retourne le nombre d'éléments dans "features".
    '''
    with open(os.path.join(DATA_DIR, filename), encoding='utf-8') as f:
        data = json.load(f)
        return len(data['features'])

@report_bp.route('/report')
def report():
    '''
    Affiche la page de rapport (report.html).
    '''
    return render_template('report.html')

@report_bp.route('/report/category_totals')
def category_totals():
    '''
    Retourne le nombre d'entités pour chaque catégorie de données (bâtiments, parcs, terrains de sport, sentiers).
    '''
    return jsonify({
        'buildings': count_features('buildings.geojson'),
        'parcs': count_features('parcs.geojson'),
        'sports_fields': count_features('sports_fields.geojson'),
        'trails': count_features('trails.geojson')
    })
