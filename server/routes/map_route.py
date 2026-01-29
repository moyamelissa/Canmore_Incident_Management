# =========================
# Titre : Route Flask - Carte
# Explication : Gère la route pour l'affichage de la page de la carte interactive dans l'application Canmore Incident Management.
# =========================
# Importations
# Explication: Importation des modules nécessaires pour Flask
from flask import Blueprint, render_template

# =========================
# Définition du Blueprint
# Explication: Création d'un blueprint pour la page de la carte
map_bp = Blueprint('map', __name__)

 # =========================
# Route pour la page de la carte
# Explication: Définit la route qui affiche la page map.html
@map_bp.route('/map')
def map():
    return render_template('map.html')
