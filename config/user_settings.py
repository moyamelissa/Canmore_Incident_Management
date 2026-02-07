'''
user_settings.py
Ce module gère la sauvegarde et le chargement des préférences utilisateur
à l'aide de la sérialisation Pickle dans un fichier binaire.
'''

import pickle    # Sérialisation binaire Python
import os        # Gestion des chemins de fichiers

# Chemin vers le fichier de données (même dossier que ce module)
SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'user_settings.pkl')

def save_user_settings(settings):
    '''
    Sauvegarde complète - Remplace tous les paramètres utilisateur.
    '''
    with open(SETTINGS_FILE, 'wb') as f:    # 'wb' = écriture binaire
        pickle.dump(settings, f)             # Sérialise dictionnaire → bytes

def get_user_settings():
    '''
    Charge et retourne les paramètres sauvegardés.
    Retourne un dictionnaire vide si le fichier n'existe pas.
    '''
    if not os.path.exists(SETTINGS_FILE):   # Si fichier inexistant
        return {}                            # → retourne dict vide
    with open(SETTINGS_FILE, 'rb') as f:    # 'rb' = lecture binaire
        return pickle.load(f)                # Désérialise bytes → dictionnaire

def update_user_settings(new_settings):
    '''
    Mise à jour partielle - Fusionne les nouveaux paramètres avec les existants.
    '''
    settings = get_user_settings()          # 1. Charge paramètres actuels
    settings.update(new_settings)           # 2. Fusionne avec nouveaux
    save_user_settings(settings)            # 3. Sauvegarde le tout
