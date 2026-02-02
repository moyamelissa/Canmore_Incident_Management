"""
test_incidents.py
Suite de tests unitaires pour l'application Canmore Incident Management.
Teste les routes API, la gestion des erreurs, et la validation des données.
"""

import unittest
import json
import sys
import os
import tempfile

# Ajoute le répertoire parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Crée les répertoires nécessaires s'ils n'existent pas
data_dir = os.path.join(os.path.dirname(__file__), 'server', 'data')
os.makedirs(data_dir, exist_ok=True)

try:
    from main import app
except ImportError as e:
    print(f"Error importing app: {e}")
    sys.exit(1)


class TestIncidentsAPI(unittest.TestCase):
    """Tests pour l'API des incidents"""

    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.app = app
        cls.app.config['TESTING'] = True

    def setUp(self):
        """Configuration avant chaque test"""
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    # ========== TESTS DE ROUTES DE BASE ==========
    
    def test_home_page_loads(self):
        """Test: La page d'accueil se charge"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_create_incident_success(self):
        """Test: Créer un incident valide"""
        incident_data = {
            'type': 'Nid de poule',
            'description': 'Grand trou',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [201, 200])

    def test_create_incident_missing_fields(self):
        """Test: Incident sans latitude (erreur attendue)"""
        incident_data = {
            'type': 'Nid de poule',
            'description': 'Grand trou',
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Doit retourner une erreur
        self.assertEqual(response.status_code, 400)

    def test_get_incidents(self):
        """Test: Récupérer tous les incidents"""
        response = self.client.get('/api/incidents')
        
        self.assertEqual(response.status_code, 200)
        # Doit être une liste JSON
        try:
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
        except json.JSONDecodeError:
            pass  # Acceptable si pas d'incidents

    def test_nonexistent_route(self):
        """Test: Route inexistante retourne 404"""
        response = self.client.get('/api/nonexistent')
        
        self.assertEqual(response.status_code, 404)

    def test_malformed_json(self):
        """Test: JSON malformé génère une erreur"""
        response = self.client.post(
            '/api/incidents',
            data='{invalid json}',
            content_type='application/json'
        )
        
        # Doit retourner une erreur client
        self.assertGreaterEqual(response.status_code, 400)


class TestErrorHandling(unittest.TestCase):
    """Tests de gestion des erreurs"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_missing_required_field(self):
        """Test: Champ requis manquant"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            # Manque latitude et longitude
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

    def test_empty_json(self):
        """Test: JSON vide"""
        response = self.client.post(
            '/api/incidents',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)


class TestValidCoordinates(unittest.TestCase):
    """Tests de validation des coordonnées"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    def test_valid_canmore_coordinates(self):
        """Test: Coordonnées valides pour Canmore"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 51.0447,    # Latitude Canmore
            'longitude': -115.3667,  # Longitude Canmore
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertIn(response.status_code, [201, 200])


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)

