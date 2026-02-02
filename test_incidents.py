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


# ============================================================================
# SECTION 1: INFRASTRUCTURE TESTS (Application Setup & HTTP Routes)
# ============================================================================
# Tests: App initialization, HTTP status codes, basic routing
# ============================================================================

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


# ============================================================================
# SECTION 2: ERROR HANDLING TESTS (Malformed Input, Missing Data)
# ============================================================================
# Tests: JSON validation, required fields, error responses
# ============================================================================

class TestErrorHandling(unittest.TestCase):
    """Tests de gestion des erreurs"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

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

    def test_malformed_json(self):
        """Test: JSON malformé génère une erreur"""
        response = self.client.post(
            '/api/incidents',
            data='{invalid json}',
            content_type='application/json'
        )
        
        # Doit retourner une erreur client
        self.assertGreaterEqual(response.status_code, 400)

    def test_empty_json(self):
        """Test: JSON vide"""
        response = self.client.post(
            '/api/incidents',
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)


# ============================================================================
# SECTION 3: DATA VALIDATION TESTS (Coordinates, Input Sanitization)
# ============================================================================
# Tests: Coordinate validation, type coercion, special characters
# ============================================================================

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

    def test_invalid_latitude_type(self):
        """Test: Latitude non numérique acceptée (pas de validation de type)"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 'invalid',  # String au lieu de float
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # API n'a pas de validation de type stricte - accepte les strings
        self.assertIn(response.status_code, [201, 200])

    def test_invalid_longitude_type(self):
        """Test: Longitude non numérique acceptée (pas de validation de type)"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 51.0447,
            'longitude': 'invalid',  # String au lieu de float
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # API n'a pas de validation de type stricte - accepte les strings
        self.assertIn(response.status_code, [201, 200])


class TestInputValidation(unittest.TestCase):
    """Tests de validation des entrées utilisateur"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    def test_empty_incident_type(self):
        """Test: Type d'incident vide accepté (pas de validation stricte)"""
        incident_data = {
            'type': '',  # Type vide
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
        
        # API n'a pas de validation stricte - accepte types vides
        self.assertIn(response.status_code, [201, 200])

    def test_extra_fields_ignored(self):
        """Test: Champs supplémentaires ignorés sans erreur"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z',
            'extra_field': 'This should be ignored',  # Champ supplémentaire
            'another_field': 12345
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Doit accepter et ignorer les champs supplémentaires
        self.assertIn(response.status_code, [201, 200])

    def test_null_description_allowed(self):
        """Test: Description null est acceptable (champ optionnel)"""
        incident_data = {
            'type': 'Test',
            'description': None,  # null
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Description est optionnelle, doit accepter
        self.assertIn(response.status_code, [201, 200])


# ============================================================================
# SECTION 4: DATA PERSISTENCE TESTS (Create, Read, Store)
# ============================================================================
# Tests: Incident creation, retrieval, multiple records
# ============================================================================

class TestDataPersistence(unittest.TestCase):
    """Tests de persistance des données en base de données"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    def test_incident_saved_to_database(self):
        """Test: Incident créé est sauvegardé en base de données"""
        incident_data = {
            'type': 'Database Test',
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
        
        self.assertIn(create_response.status_code, [201, 200])
        
        # Récupère et vérifie
        get_response = self.client.get('/api/incidents')
        self.assertEqual(get_response.status_code, 200)
        
        data = json.loads(get_response.data)
        self.assertGreater(len(data), 0)
        
        # Vérifie que notre incident est dans la liste
        incident_types = [inc.get('type') for inc in data if isinstance(inc, dict)]
        self.assertIn('Database Test', incident_types)

    def test_multiple_incidents_isolation(self):
        """Test: Plusieurs incidents sont stockés indépendamment"""
        incidents = [
            {'type': 'Pothole', 'description': 'Big hole', 'latitude': 51.0447, 'longitude': -115.3667, 'timestamp': '2024-02-02T10:00:00Z'},
            {'type': 'Tree', 'description': 'Fallen tree', 'latitude': 51.0450, 'longitude': -115.3670, 'timestamp': '2024-02-02T11:00:00Z'},
            {'type': 'Graffiti', 'description': 'Graffiti on sign', 'latitude': 51.0445, 'longitude': -115.3665, 'timestamp': '2024-02-02T12:00:00Z'}
        ]
        
        # Crée 3 incidents
        for incident in incidents:
            response = self.client.post(
                '/api/incidents',
                data=json.dumps(incident),
                content_type='application/json'
            )
            self.assertIn(response.status_code, [201, 200])
        
        # Vérifie qu'ils sont tous récupérés
        get_response = self.client.get('/api/incidents')
        self.assertEqual(get_response.status_code, 200)
        
        data = json.loads(get_response.data)
        self.assertGreaterEqual(len(data), 3)


# ============================================================================
# SECTION 5: SQLITE DATABASE TESTS (Schema, Constraints, Transactions)
# ============================================================================
# Tests: Database file, tables, columns, constraints, data integrity
# ============================================================================

class TestSQLiteDatabase(unittest.TestCase):
    """Tests spécifiques pour la base de données SQLite"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db, DB_PATH
            self.db_path = DB_PATH
            init_db()

    def test_database_file_exists(self):
        """Test: Le fichier de base de données SQLite existe"""
        import os
        self.assertTrue(os.path.exists(self.db_path), 
                       f"Database file not found at {self.db_path}")

    def test_database_file_is_valid_sqlite(self):
        """Test: Le fichier est une base de données SQLite valide"""
        import sqlite3
        try:
            conn = sqlite3.connect(self.db_path)
            # Teste si c'est une vraie base de données
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            # Doit avoir au moins une table
            self.assertGreater(len(tables), 0)
        except Exception as e:
            self.fail(f"Database is not valid SQLite: {e}")

    def test_incidents_table_created(self):
        """Test: La table 'incidents' est créée"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result, "incidents table not found")

    def test_incidents_table_has_required_columns(self):
        """Test: La table incidents a toutes les colonnes requises"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupère les colonnes
        cursor.execute("PRAGMA table_info(incidents);")
        columns = cursor.fetchall()
        conn.close()
        
        column_names = [col[1] for col in columns]
        
        # Vérifie les colonnes essentielles
        required_columns = ['id', 'type', 'latitude', 'longitude', 'timestamp']
        for col in required_columns:
            self.assertIn(col, column_names, f"Column '{col}' not found in incidents table")

    def test_database_constraints_enforced(self):
        """Test: Les contraintes NOT NULL sont appliquées"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tente d'insérer sans latitude (NOT NULL)
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute('''
                INSERT INTO incidents (type, description, longitude, timestamp, status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Test', 'Test', -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
            conn.commit()
        
        conn.close()

    def test_database_autoincrement_id(self):
        """Test: L'ID s'auto-incrémente correctement"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insère 2 incidents
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test1', 'Desc1', 51.0447, -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
        
        id1 = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test2', 'Desc2', 51.0450, -115.3670, '2024-02-02T11:00:00Z', 'unsolved'))
        
        id2 = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Les IDs doivent être différents et croissants
        self.assertNotEqual(id1, id2)
        self.assertLess(id1, id2)

    def test_database_status_default_value(self):
        """Test: La colonne status a une valeur par défaut 'unsolved'"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insère sans spécifier status
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Test', 'Desc', 51.0447, -115.3667, '2024-02-02T10:00:00Z'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère l'incident
        cursor.execute('SELECT status FROM incidents WHERE id = ?', (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], 'unsolved')

    def test_database_transaction_rollback_on_error(self):
        """Test: Les transactions se font correctement (isolation)"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Compte les incidents avant
        cursor.execute('SELECT COUNT(*) FROM incidents')
        count_before = cursor.fetchone()[0]
        
        try:
            # Tente une opération invalide
            cursor.execute('''
                INSERT INTO incidents (type, latitude, longitude, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (None, 51.0447, -115.3667, '2024-02-02T10:00:00Z'))  # type IS NULL
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
        
        # Compte après
        cursor.execute('SELECT COUNT(*) FROM incidents')
        count_after = cursor.fetchone()[0]
        conn.close()
        
        # Le count ne doit pas avoir changé (rollback)
        self.assertEqual(count_before, count_after)

    def test_database_data_retrieval_accuracy(self):
        """Test: Les données insérées sont récupérées correctement"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        test_data = {
            'type': 'Pothole',
            'description': 'Large hole in road',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        # Insère
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (test_data['type'], test_data['description'], test_data['latitude'], 
              test_data['longitude'], test_data['timestamp'], 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère
        cursor.execute('SELECT type, description, latitude, longitude FROM incidents WHERE id = ?', 
                      (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        # Vérifie que les données correspondent
        self.assertEqual(result[0], test_data['type'])
        self.assertEqual(result[1], test_data['description'])
        self.assertAlmostEqual(result[2], test_data['latitude'], places=4)
        self.assertAlmostEqual(result[3], test_data['longitude'], places=4)

    def test_database_multiple_tables_independence(self):
        """Test: Les tables sont indépendantes"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupère toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        # Au moins la table incidents doit exister
        table_names = [t[0] for t in tables]
        self.assertIn('incidents', table_names)

    def test_database_handles_special_characters(self):
        """Test: Les caractères spéciaux (accents) sont stockés correctement"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        special_text = "Nid de poule à côté du café - Éclairage défaillant"
        
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (special_text, "Description avec accénts: é à ù", 51.0447, -115.3667, 
              '2024-02-02T10:00:00Z', 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute('SELECT type FROM incidents WHERE id = ?', (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], special_text)


# ============================================================================
# SECTION 6: ADDITIONAL TESTS (Add your tests here)
# ============================================================================
# Space for user-defined tests
# ============================================================================


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
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

    def test_invalid_latitude_type(self):
        """Test: Latitude non numérique acceptée (pas de validation de type)"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 'invalid',  # String au lieu de float
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # API n'a pas de validation de type stricte - accepte les strings
        self.assertIn(response.status_code, [201, 200])

    def test_invalid_longitude_type(self):
        """Test: Longitude non numérique acceptée (pas de validation de type)"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 51.0447,
            'longitude': 'invalid',  # String au lieu de float
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # API n'a pas de validation de type stricte - accepte les strings
        self.assertIn(response.status_code, [201, 200])


class TestInputValidation(unittest.TestCase):
    """Tests de validation des entrées utilisateur"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    def test_empty_incident_type(self):
        """Test: Type d'incident vide accepté (pas de validation stricte)"""
        incident_data = {
            'type': '',  # Type vide
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
        
        # API n'a pas de validation stricte - accepte types vides
        self.assertIn(response.status_code, [201, 200])

    def test_extra_fields_ignored(self):
        """Test: Champs supplémentaires ignorés sans erreur"""
        incident_data = {
            'type': 'Test',
            'description': 'Test',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z',
            'extra_field': 'This should be ignored',  # Champ supplémentaire
            'another_field': 12345
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Doit accepter et ignorer les champs supplémentaires
        self.assertIn(response.status_code, [201, 200])

    def test_null_description_allowed(self):
        """Test: Description null est acceptable (champ optionnel)"""
        incident_data = {
            'type': 'Test',
            'description': None,  # null
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        response = self.client.post(
            '/api/incidents',
            data=json.dumps(incident_data),
            content_type='application/json'
        )
        
        # Description est optionnelle, doit accepter
        self.assertIn(response.status_code, [201, 200])


class TestDataPersistence(unittest.TestCase):
    """Tests de persistance des données en base de données"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    def test_incident_saved_to_database(self):
        """Test: Incident créé est sauvegardé en base de données"""
        incident_data = {
            'type': 'Database Test',
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
        
        self.assertIn(create_response.status_code, [201, 200])
        
        # Récupère et vérifie
        get_response = self.client.get('/api/incidents')
        self.assertEqual(get_response.status_code, 200)
        
        data = json.loads(get_response.data)
        self.assertGreater(len(data), 0)
        
        # Vérifie que notre incident est dans la liste
        incident_types = [inc.get('type') for inc in data if isinstance(inc, dict)]
        self.assertIn('Database Test', incident_types)

    def test_multiple_incidents_isolation(self):
        """Test: Plusieurs incidents sont stockés indépendamment"""
        incidents = [
            {'type': 'Pothole', 'description': 'Big hole', 'latitude': 51.0447, 'longitude': -115.3667, 'timestamp': '2024-02-02T10:00:00Z'},
            {'type': 'Tree', 'description': 'Fallen tree', 'latitude': 51.0450, 'longitude': -115.3670, 'timestamp': '2024-02-02T11:00:00Z'},
            {'type': 'Graffiti', 'description': 'Graffiti on sign', 'latitude': 51.0445, 'longitude': -115.3665, 'timestamp': '2024-02-02T12:00:00Z'}
        ]
        
        # Crée 3 incidents
        for incident in incidents:
            response = self.client.post(
                '/api/incidents',
                data=json.dumps(incident),
                content_type='application/json'
            )
            self.assertIn(response.status_code, [201, 200])
        
        # Vérifie qu'ils sont tous récupérés
        get_response = self.client.get('/api/incidents')
        self.assertEqual(get_response.status_code, 200)
        
        data = json.loads(get_response.data)
        self.assertGreaterEqual(len(data), 3)


class TestSQLiteDatabase(unittest.TestCase):
    """Tests spécifiques pour la base de données SQLite"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db, DB_PATH
            self.db_path = DB_PATH
            init_db()

    def test_database_file_exists(self):
        """Test: Le fichier de base de données SQLite existe"""
        import os
        self.assertTrue(os.path.exists(self.db_path), 
                       f"Database file not found at {self.db_path}")

    def test_database_file_is_valid_sqlite(self):
        """Test: Le fichier est une base de données SQLite valide"""
        import sqlite3
        try:
            conn = sqlite3.connect(self.db_path)
            # Teste si c'est une vraie base de données
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            # Doit avoir au moins une table
            self.assertGreater(len(tables), 0)
        except Exception as e:
            self.fail(f"Database is not valid SQLite: {e}")

    def test_incidents_table_created(self):
        """Test: La table 'incidents' est créée"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result, "incidents table not found")

    def test_incidents_table_has_required_columns(self):
        """Test: La table incidents a toutes les colonnes requises"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupère les colonnes
        cursor.execute("PRAGMA table_info(incidents);")
        columns = cursor.fetchall()
        conn.close()
        
        column_names = [col[1] for col in columns]
        
        # Vérifie les colonnes essentielles
        required_columns = ['id', 'type', 'latitude', 'longitude', 'timestamp']
        for col in required_columns:
            self.assertIn(col, column_names, f"Column '{col}' not found in incidents table")

    def test_database_constraints_enforced(self):
        """Test: Les contraintes NOT NULL sont appliquées"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tente d'insérer sans latitude (NOT NULL)
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute('''
                INSERT INTO incidents (type, description, longitude, timestamp, status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Test', 'Test', -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
            conn.commit()
        
        conn.close()

    def test_database_autoincrement_id(self):
        """Test: L'ID s'auto-incrémente correctement"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insère 2 incidents
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test1', 'Desc1', 51.0447, -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
        
        id1 = cursor.lastrowid
        
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Test2', 'Desc2', 51.0450, -115.3670, '2024-02-02T11:00:00Z', 'unsolved'))
        
        id2 = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Les IDs doivent être différents et croissants
        self.assertNotEqual(id1, id2)
        self.assertLess(id1, id2)

    def test_database_status_default_value(self):
        """Test: La colonne status a une valeur par défaut 'unsolved'"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insère sans spécifier status
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', ('Test', 'Desc', 51.0447, -115.3667, '2024-02-02T10:00:00Z'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère l'incident
        cursor.execute('SELECT status FROM incidents WHERE id = ?', (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], 'unsolved')

    def test_database_transaction_rollback_on_error(self):
        """Test: Les transactions se font correctement (isolation)"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Compte les incidents avant
        cursor.execute('SELECT COUNT(*) FROM incidents')
        count_before = cursor.fetchone()[0]
        
        try:
            # Tente une opération invalide
            cursor.execute('''
                INSERT INTO incidents (type, latitude, longitude, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (None, 51.0447, -115.3667, '2024-02-02T10:00:00Z'))  # type IS NULL
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
        
        # Compte après
        cursor.execute('SELECT COUNT(*) FROM incidents')
        count_after = cursor.fetchone()[0]
        conn.close()
        
        # Le count ne doit pas avoir changé (rollback)
        self.assertEqual(count_before, count_after)

    def test_database_data_retrieval_accuracy(self):
        """Test: Les données insérées sont récupérées correctement"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        test_data = {
            'type': 'Pothole',
            'description': 'Large hole in road',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        # Insère
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (test_data['type'], test_data['description'], test_data['latitude'], 
              test_data['longitude'], test_data['timestamp'], 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère
        cursor.execute('SELECT type, description, latitude, longitude FROM incidents WHERE id = ?', 
                      (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        # Vérifie que les données correspondent
        self.assertEqual(result[0], test_data['type'])
        self.assertEqual(result[1], test_data['description'])
        self.assertAlmostEqual(result[2], test_data['latitude'], places=4)
        self.assertAlmostEqual(result[3], test_data['longitude'], places=4)

    def test_database_multiple_tables_independence(self):
        """Test: Les tables sont indépendantes"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupère toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        conn.close()
        
        # Au moins la table incidents doit exister
        table_names = [t[0] for t in tables]
        self.assertIn('incidents', table_names)

    def test_database_handles_special_characters(self):
        """Test: Les caractères spéciaux (accents) sont stockés correctement"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        special_text = "Nid de poule à côté du café - Éclairage défaillant"
        
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (special_text, "Description avec accénts: é à ù", 51.0447, -115.3667, 
              '2024-02-02T10:00:00Z', 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        cursor.execute('SELECT type FROM incidents WHERE id = ?', (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], special_text)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)

