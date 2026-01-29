# =========================
# Importations
# Explication: Importation des modules nécessaires pour Flask
from flask import Blueprint, render_template

# =========================
# Définition du Blueprint
# Explication: Création d'un blueprint pour la page d'accueil
home_bp = Blueprint('home', __name__)

# =========================
# Route pour la page d'accueil
# Explication: Définit la route qui affiche la page home.html
@home_bp.route('/')
def home():
    return render_template('home.html')
