import pickle
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'user_settings.pkl')

def save_user_settings(settings):
    with open(SETTINGS_FILE, 'wb') as f:
        pickle.dump(settings, f)

def load_user_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, 'rb') as f:
        return pickle.load(f)

def get_user_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {}
    with open(SETTINGS_FILE, 'rb') as f:
        return pickle.load(f)

def update_user_settings(new_settings):
    settings = get_user_settings()
    settings.update(new_settings)
    save_user_settings(settings)
