'''
home_route.py
Ce module définit la route Flask pour la page d'accueil de l'application Canmore Incident Management.
'''

from flask import Blueprint, render_template

# Création d'un blueprint pour la page d'accueil
home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    '''
    Affiche la page d'accueil (home.html).
    '''
    return render_template('home.html')
