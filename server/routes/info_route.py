'''
info_route.py
Ce module définit la route Flask pour la page d'information (info.html)
de l'application Canmore Incident Management.
'''

from flask import Blueprint, render_template

# Création d'un blueprint pour la page d'information
info_bp = Blueprint('info', __name__)

@info_bp.route('/info')
def info():
    '''
    Affiche la page d'information (info.html).
    '''
    return render_template('info.html')
