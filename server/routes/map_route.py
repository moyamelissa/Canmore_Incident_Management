'''
map_route.py
Ce module définit la route Flask pour la page de la carte interactive (map.html)
de l'application Canmore Incident Management.
'''

from flask import Blueprint, render_template

# Création d'un blueprint pour la page de la carte
map_bp = Blueprint('map', __name__)

@map_bp.route('/map')
def map():
    '''
    Affiche la page de la carte interactive (map.html).
    '''
    return render_template('map.html')
