'''
user_settings.py
Ce module gère la sauvegarde et le chargement des préférences utilisateur
à l'aide de la sérialisation Pickle dans un fichier binaire.
'''

import pickle
import os

# Chemin vers le fichier des paramètres (Pickle binaire)
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'user_settings.pkl')

def save_user_settings(settings):
    '''
    Remplace tous les paramètres utilisateur par le dictionnaire fourni.
    '''
    with open(SETTINGS_FILE, 'wb') as f:
        pickle.dump(settings, f)

def get_user_settings():
    '''
    Charge et retourne le dictionnaire des paramètres utilisateur depuis le fichier Pickle.
    Retourne un dictionnaire vide si le fichier n'existe pas.
    '''
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, 'rb') as f:
        return pickle.load(f)

def update_user_settings(new_settings):
    '''
    Met à jour les paramètres utilisateur avec de nouvelles valeurs et les sauvegarde.
    '''
    settings = get_user_settings()
    settings.update(new_settings)
    save_user_settings(settings)
