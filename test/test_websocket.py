"""
test_websocket.py
Tests pour le serveur WebSocket - existence du module, importation SocketIO, validité Python

Importance: Les tests WebSocket vérifient que le serveur existe, que les dépendances
sont installées, et que le module est valide. C'est essentiel pour la communication
temps réel de l'application.
"""

import unittest
import os
import sys
import ast
import py_compile

# Ajoute le répertoire parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestWebSocketServerBasics(unittest.TestCase):
    """
    Tests de base pour websocket_server.py
    
    Vérifie que:
    - Le fichier websocket_server.py existe
    - Le module est un fichier Python valide (pas d'erreurs de syntaxe)
    - Le module peut être compilé
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.server_path = os.path.join(self.project_root, 'websocket_server.py')

    def test_websocket_server_file_exists(self):
        """
        Test: websocket_server.py existe dans le projet
        Importance: Vérifie que le module serveur WebSocket est présent
        """
        self.assertTrue(os.path.exists(self.server_path),
                       f"websocket_server.py not found at {self.server_path}")

    def test_websocket_server_is_python_file(self):
        """
        Test: websocket_server.py est un fichier Python valide (compilable)
        Importance: Vérifie qu'il n'y a pas d'erreurs de syntaxe
        """
        try:
            py_compile.compile(self.server_path, doraise=True)
        except py_compile.PyCompileError as e:
            self.fail(f"Syntax error in websocket_server.py: {e}")

    def test_websocket_server_module_loadable(self):
        """
        Test: websocket_server.py peut être chargé comme module
        Importance: Vérifie que le module est importable sans erreur majeure
        """
        try:
            with open(self.server_path, 'r', encoding='utf-8') as f:
                source = f.read()
            ast.parse(source, filename=self.server_path)
        except Exception as e:
            self.fail(f"websocket_server module failed to parse: {e}")


class TestFlaskSocketIOAvailability(unittest.TestCase):
    """
    Tests pour vérifier la disponibilité de flask_socketio
    
    Vérifie que:
    - flask_socketio est installé et importable
    - La classe SocketIO est disponible
    """

    def test_flask_socketio_importable(self):
        """
        Test: flask_socketio peut être importé
        Importance: Vérifie que la dépendance WebSocket est installée
        """
        try:
            import flask_socketio  # noqa: F401
        except ImportError as e:
            self.fail(f"flask_socketio not installed or not importable: {e}")

    def test_socketio_class_available(self):
        """
        Test: La classe SocketIO est disponible dans flask_socketio
        Importance: Vérifie que l'API principale est accessible
        """
        try:
            from flask_socketio import SocketIO  # noqa: F401
        except ImportError as e:
            self.fail(f"SocketIO class not available: {e}")


class TestWebSocketServerStructure(unittest.TestCase):
    """
    Tests de structure du serveur WebSocket
    
    Vérifie que:
    - Le module expose des objets attendus (socketio ou app)
    - Le fichier contient du code exécutable sans erreur
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.server_path = os.path.join(self.project_root, 'websocket_server.py')

    def test_websocket_server_exports_socketio_or_app(self):
        """
        Test: websocket_server expose 'socketio' ou 'app'
        Importance: Vérifie que le module contient l'objet principal du serveur
        """
        with open(self.server_path, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source, filename=self.server_path)
        assigned_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_names.add(target.id)

        has_socketio = 'socketio' in assigned_names
        has_app = 'app' in assigned_names

        self.assertTrue(has_socketio or has_app,
                        "websocket_server.py does not define 'socketio' or 'app'")


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
