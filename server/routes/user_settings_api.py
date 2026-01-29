from flask import Blueprint, request, jsonify
from config.user_settings import update_user_settings, get_user_settings

user_settings_api = Blueprint('user_settings_api', __name__)

@user_settings_api.route('/save_user_settings', methods=['POST'])
def save_settings():
    data = request.get_json()
    update_user_settings(data)
    return jsonify({'status': 'ok'})

@user_settings_api.route('/get_user_settings', methods=['GET'])
def get_settings():
    settings = get_user_settings()
    return jsonify(settings)
