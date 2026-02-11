"""
test_flask_socketio.py
Tests pour l'intégration Flask-SocketIO :
- Vérifie que flask_socketio est installée et importable
- Vérifie que l'application Flask démarre avec SocketIO
- Vérifie la connexion d'un client SocketIO
"""

import unittest
from flask import Flask
from flask_socketio import SocketIO, emit
from flask_socketio import test_client

class TestFlaskSocketIOIntegration(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.secret_key = 'test-key'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        @self.socketio.on('ping')
        def handle_ping(msg):
            emit('pong', msg)

        self.client = self.socketio.test_client(self.app)

    def test_flask_socketio_import(self):
        try:
            import flask_socketio
        except ImportError:
            self.fail("flask_socketio should be importable")

    def test_socketio_class_available(self):
        try:
            from flask_socketio import SocketIO
        except ImportError:
            self.fail("SocketIO class should be available in flask_socketio")

    def test_client_can_connect(self):
        self.assertTrue(self.client.is_connected(), "Le client SocketIO doit pouvoir se connecter.")

    def test_ping_pong(self):
        self.client.emit('ping', {'data': 'hello'})
        received = self.client.get_received()
        found = any(event['name'] == 'pong' and event['args'][0]['data'] == 'hello' for event in received)
        self.assertTrue(found, "Le serveur doit répondre 'pong' avec les mêmes données.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
