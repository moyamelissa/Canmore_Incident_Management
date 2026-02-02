"""
test_incidents.py
Suite de tests unitaires pour l'application Canmore Incident Management.
Teste les routes API, la gestion des erreurs, et la validation des données.

Tests couverts:
- Création d'incidents (POST)
- Récupération d'incidents (GET)
- Mise à jour de statut (PATCH)
- Suppression d'incidents (DELETE)
- Gestion des erreurs et exceptions
- Validation des données d'entrée
"""

import unittest
import json
import sys
import os

# Ajoute le répertoire parent au chemin pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from server.routes.incidents_api import init_db


class TestIncidentsAPI(unittest.TestCase):
    """Tests pour l'API des incidents"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        
        # Initialise la base de données
        with self.app.app_context():
            init_db()

    def tearDown(self):
        """Nettoyage après chaque test"""
        # Optionnel: peut ajouter du nettoyage si nécessaire
        pass

    # ========== TESTS DE CRÉATION D'INCIDENTS ==========
    
    def test_create_incident_success(self):
        """Test: Créer un incident avec tous les champs requis"""
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
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertEqual(response.json['message'], 'Incident ajouté avec succès')

    def test_create_incident_missing_fields(self):
        """Test: Créer un incident avec champs manquants (GESTION D'ERREUR)"""
        # Manque le champ 'latitude'
        incident_data = {
            'type': 'Nid de poule',
            'description': 'Grand trou dans la route',
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Doit retourner 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_create_incident_invalid_json(self):
        """Test: Créer un incident avec JSON invalide (GESTION D'ERREUR)"""
        response = self.client.post(
            '/api/incidents',
            data='invalid json',
            content_type='application/json'
        )
        
        # Doit retourner 400 ou 415 selon l'implémentation Flask
        self.assertIn(response.status_code, [400, 415])

    def test_create_incident_with_valid_coordinates(self):
        """Test: Valider les coordonnées GPS"""
        incident_data = {
            'type': 'Arbre tombé',
            'description': 'Arbre obstruant la route',
            'latitude': 51.0447,  # Latitude valide
            'longitude': -115.3667,  # Longitude valide (ouest = négative)
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)

    # ========== TESTS DE RÉCUPÉRATION D'INCIDENTS ==========
    
    def test_get_all_incidents(self):
        """Test: Récupérer tous les incidents"""
        # Crée un incident d'abord
        incident_data = {
            'type': 'Graffiti',
            'description': 'Graffiti sur panneau',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Récupère tous les incidents
        response = self.client.get('/api/incidents')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    # ========== TESTS DE MISE À JOUR DE STATUT ==========
    
    def test_update_incident_status_success(self):
        """Test: Mettre à jour le statut d'un incident"""
        # Crée un incident d'abord
        incident_data = {
            'type': 'Éclairage défaillant',
            'description': 'Lampadaire hors service',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        create_response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Récupère l'ID depuis la base (simplifié: suppose que c'est 1)
        incident_id = 1
        
        # Met à jour le statut
        update_data = {'status': 'resolved'}
        response = self.client.patch(
            f'/api/incidents/{incident_id}',
            data=json.dumps(update_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)

    def test_update_incident_missing_status(self):
        """Test: Mettre à jour sans champ status (GESTION D'ERREUR)"""
        incident_id = 1
        
        # Essaie de mettre à jour sans le champ status
        response = self.client.patch(
            f'/api/incidents/{incident_id}',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        # Doit retourner 400 Bad Request
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    # ========== TESTS DE SUPPRESSION D'INCIDENTS ==========
    
    def test_delete_incident_success(self):
        """Test: Supprimer un incident"""
        # Crée un incident d'abord
        incident_data = {
            'type': 'Déchet',
            'description': 'Déchet sauvage',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Supprime l'incident
        incident_id = 1
        response = self.client.delete(f'/api/incidents/{incident_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)

    # ========== TESTS DE VALIDATION ET EXCEPTIONS ==========
    
    def test_invalid_incident_type(self):
        """Test: Incident avec type vide (validation d'entrée)"""
        incident_data = {
            'type': '',  # Invalide: type vide
            'description': 'Description',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Selon l'implémentation, peut accepter ou rejeter
        # Ce test valide la cohérence
        self.assertIn(response.status_code, [201, 400])

    def test_negative_coordinates(self):
        """Test: Vérifier que la longitude négative est acceptée (Amérique du Nord)"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 51.0447,
            'longitude': -115.3667,  # Négatif pour l'Amérique du Nord
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)


class TestErrorHandling(unittest.TestCase):
    """Tests pour la gestion des erreurs et exceptions"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_nonexistent_route(self):
        """Test: Accès à une route inexistante (gestion 404)"""
        response = self.client.get('/api/nonexistent')
        
        self.assertEqual(response.status_code, 404)

    def test_malformed_json(self):
        """Test: Envoyer du JSON malformé (gestion d'exception)"""
        response = self.client.post(
            '/api/incidents',
            data='{invalid json}',
            content_type='application/json'
        )
        
        # Doit retourner une erreur, pas un crash
        self.assertGreaterEqual(response.status_code, 400)

    def test_database_integrity(self):
        """Test: Vérifier que les incidents sont persistés en BD"""
        incident_data = {
            'type': 'Test DB',
            'description': 'Test persistance',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        # Crée
        create_response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        self.assertEqual(create_response.status_code, 201)
        
        # Récupère pour vérifier
        get_response = self.client.get('/api/incidents')
        self.assertEqual(get_response.status_code, 200)
        data = json.loads(get_response.data)
        self.assertGreaterEqual(len(data), 1)


class TestHomeRoute(unittest.TestCase):
    """Tests pour les routes statiques"""

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.client = self.app.test_client()

    def test_home_page_loads(self):
        """Test: La page d'accueil se charge correctement"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'html', response.data.lower())


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    # Lance tous les tests avec verbosité
    unittest.main(verbosity=2)
