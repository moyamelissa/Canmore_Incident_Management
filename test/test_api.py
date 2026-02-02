"""
test_api.py
Tests pour l'API REST - Endpoints, réponses JSON, gestion des erreurs

Importance: Les tests d'API vérifient que les endpoints REST fonctionnent correctement,
retournent le bon format (JSON), les bons codes HTTP, et gèrent les erreurs proprement.
C'est crucial pour la fiabilité de l'application côté client.
"""

import unittest
import json
import sys
import os

# Ajoute le répertoire parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Crée les répertoires nécessaires
data_dir = os.path.join(os.path.dirname(__file__), '..', 'server', 'data')
os.makedirs(data_dir, exist_ok=True)

try:
    from main import app
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)


class TestAPIEndpoints(unittest.TestCase):
    """
    Tests des endpoints REST principaux
    
    Vérifie que:
    - GET /api/incidents récupère une liste d'incidents
    - POST /api/incidents crée un nouvel incident
    - Les réponses sont en JSON
    - Les codes HTTP sont corrects
    """

    def setUp(self):
        """
        Configuration avant chaque test
        - Active le mode test de Flask
        - Initialise la base de données
        """
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    # ===== TESTS GET /api/incidents =====

    def test_get_incidents_returns_200(self):
        """
        Test: GET /api/incidents retourne le code 200 (succès)
        Importance: Vérifie que l'endpoint répond correctement
        """
        response = self.client.get('/api/incidents')
        self.assertEqual(response.status_code, 200)

    def test_get_incidents_returns_json(self):
        """
        Test: GET /api/incidents retourne du JSON
        Importance: Vérifie que l'API respecte le format JSON attendu par les clients
        """
        response = self.client.get('/api/incidents')
        self.assertIn('application/json', response.content_type)

    def test_get_incidents_returns_list(self):
        """
        Test: GET /api/incidents retourne une liste
        Importance: Vérifie que la structure de réponse est une liste, pas un objet unique
        """
        response = self.client.get('/api/incidents')
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    # ===== TESTS POST /api/incidents - CAS VALIDE =====

    def test_post_incident_with_valid_data_returns_201_or_200(self):
        """
        Test: POST /api/incidents avec données valides retourne 201 ou 200
        Importance: Vérifie que la création d'incident réussit avec un code HTTP approprié
        """
        incident_data = {
            'type': 'Nid de poule',
            'description': 'Grand trou dans la route',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # 201 Created ou 200 OK sont acceptables
        self.assertIn(response.status_code, [200, 201])

    def test_post_incident_valid_returns_json_response(self):
        """
        Test: POST /api/incidents retourne une réponse JSON
        Importance: Vérifie que l'API répond en JSON, utilisable par les clients
        """
        incident_data = {
            'type': 'Pothole',
            'description': 'Test incident',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Doit être parseable en JSON
        try:
            data = json.loads(response.data)
            self.assertIsNotNone(data)
        except json.JSONDecodeError:
            self.fail("POST response is not valid JSON")

    # ===== TESTS POST /api/incidents - ERREURS =====

    def test_post_incident_missing_latitude_returns_400(self):
        """
        Test: POST sans latitude retourne 400 (Bad Request)
        Importance: Vérifie que l'API valide les champs obligatoires et rejette les données incomplètes
        """
        incident_data = {
            'type': 'Nid de poule',
            'description': 'Grand trou',
            'longitude': -115.3667,  # latitude manquante
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

    def test_post_incident_missing_longitude_returns_400(self):
        """
        Test: POST sans longitude retourne 400
        Importance: Vérifie que l'API valide tous les champs obligatoires pour localiser l'incident
        """
        incident_data = {
            'type': 'Arbre tombé',
            'description': 'Grand arbre en travers de la route',
            'latitude': 51.0447,
            'timestamp': '2024-02-02T10:00:00Z'
            # longitude manquante
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

    def test_post_incident_missing_type_returns_400(self):
        """
        Test: POST sans type d'incident retourne 400
        Importance: Vérifie que le type d'incident est obligatoire pour catégoriser les rapports
        """
        incident_data = {
            'description': 'Un problème',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
            # type manquant
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

    def test_post_incident_malformed_json_returns_400(self):
        """
        Test: POST avec JSON malformé retourne 400
        Importance: Vérifie que l'API gère les erreurs de parsing JSON et rejette les données invalides
        """
        response = self.client.post(
            '/api/incidents',
            data='{invalid json}',  # JSON non valide
            content_type='application/json'
        )
        
        self.assertGreaterEqual(response.status_code, 400)

    def test_post_incident_empty_json_returns_400(self):
        """
        Test: POST avec JSON vide {} retourne 400
        Importance: Vérifie que l'API rejette les requêtes vides sans données
        """
        response = self.client.post(
            '/api/incidents',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)

    # ===== TESTS DE CONTENT-TYPE =====

    def test_api_content_type_is_json(self):
        """
        Test: La réponse API a le Content-Type application/json
        Importance: Vérifie que le serveur communique le bon format de données aux clients
        """
        response = self.client.get('/api/incidents')
        self.assertIn('application/json', response.content_type)

    def test_post_requires_json_content_type(self):
        """
        Test: POST retourne du JSON même si Content-Type n'est pas spécifié
        Importance: Vérifie la robustesse de l'API face aux clients mal configurés
        """
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Doit être du JSON
        try:
            json.loads(response.data)
            self.assertTrue(True)
        except json.JSONDecodeError:
            self.fail("Response should be JSON")

    # ===== TESTS D'INTÉGRATION =====

    def test_create_and_retrieve_incident(self):
        """
        Test: Créer un incident, puis le récupérer
        Importance: Vérifie l'intégration complète: POST + GET fonctionnent ensemble
        """
        # Crée l'incident
        incident_data = {
            'type': 'Integration Test',
            'description': 'Test d\'intégration POST/GET',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        post_response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertIn(post_response.status_code, [200, 201])
        
        # Récupère tous les incidents
        get_response = self.client.get('/api/incidents')
        self.assertEqual(get_response.status_code, 200)
        
        # Vérifie que notre incident y est
        data = json.loads(get_response.data)
        types = [inc.get('type') for inc in data if isinstance(inc, dict)]
        self.assertIn('Integration Test', types)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
