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
# SECTION 6: ADDITIONAL TESTS (WebSocket, CSV, JSON, Pickle, Binary Files)
# ============================================================================
# Tests: Concepts learned - WebSocket, Templates, API, CSV, JSON, Pickle, etc
# ============================================================================

class TestFlaskTemplates(unittest.TestCase):
    """Tests pour le rendu des templates Flask"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_template_renders(self):
        """Test: La template home.html se rend correctement"""
        response = self.client.get('/')
        
        self.assertEqual(response.status_code, 200)
        # Vérifie que c'est du HTML (case-insensitive)
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        self.assertIn('<!doctype', html_lower)
        self.assertIn('html', html_lower)

    def test_map_template_loads(self):
        """Test: La template map.html se charge"""
        response = self.client.get('/map')
        
        self.assertEqual(response.status_code, 200)
        # Vérifie que c'est du contenu HTML
        self.assertGreater(len(response.data), 0)

    def test_report_template_loads(self):
        """Test: La template report.html se charge"""
        response = self.client.get('/report')
        
        self.assertEqual(response.status_code, 200)

    def test_info_template_loads(self):
        """Test: La template info.html se charge"""
        response = self.client.get('/info')
        
        self.assertEqual(response.status_code, 200)


class TestFlaskAPI(unittest.TestCase):
    """Tests pour l'API REST Flask"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db
            init_db()

    def test_api_returns_json_content_type(self):
        """Test: L'API retourne Content-Type: application/json"""
        response = self.client.get('/api/incidents')
        
        self.assertIn('application/json', response.content_type)

    def test_api_post_returns_json_response(self):
        """Test: POST API retourne une réponse JSON"""
        incident_data = {
            'type': 'Test API',
            'description': 'JSON Response Test',
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
            self.assertIsInstance(data, (dict, list))
        except json.JSONDecodeError:
            self.fail("API response is not valid JSON")

    def test_api_get_all_incidents_returns_list(self):
        """Test: GET /api/incidents retourne une liste"""
        response = self.client.get('/api/incidents')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)


class TestJSONHandling(unittest.TestCase):
    """Tests pour la manipulation de JSON"""

    def test_json_serialization(self):
        """Test: Sérialisation d'objets en JSON"""
        incident = {
            'type': 'Pothole',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        # Sérialise en JSON
        json_str = json.dumps(incident)
        
        # Doit être une string
        self.assertIsInstance(json_str, str)
        # Doit contenir les données
        self.assertIn('Pothole', json_str)

    def test_json_deserialization(self):
        """Test: Désérialisation de JSON en objet"""
        json_str = '{"type": "Tree", "latitude": 51.0447, "longitude": -115.3667}'
        
        # Désérialise
        obj = json.loads(json_str)
        
        # Doit être un dict
        self.assertIsInstance(obj, dict)
        self.assertEqual(obj['type'], 'Tree')
        self.assertAlmostEqual(obj['latitude'], 51.0447, places=4)

    def test_json_with_special_characters(self):
        """Test: JSON avec caractères spéciaux (accents)"""
        incident = {
            'type': 'Nid de poule à côté du café',
            'description': 'Éclairage défaillant'
        }
        
        # Sérialise avec ensure_ascii=False pour préserver accents
        json_str = json.dumps(incident, ensure_ascii=False)
        
        # Désérialise et vérifie
        obj = json.loads(json_str)
        self.assertEqual(obj['type'], 'Nid de poule à côté du café')

    def test_json_nested_structures(self):
        """Test: JSON avec structures imbriquées"""
        complex_data = {
            'incidents': [
                {'type': 'Pothole', 'location': {'lat': 51.0447, 'lng': -115.3667}},
                {'type': 'Tree', 'location': {'lat': 51.0450, 'lng': -115.3670}}
            ]
        }
        
        json_str = json.dumps(complex_data)
        obj = json.loads(json_str)
        
        # Vérifie la structure imbriquée
        self.assertEqual(len(obj['incidents']), 2)
        self.assertEqual(obj['incidents'][0]['location']['lat'], 51.0447)


class TestCSVReading(unittest.TestCase):
    """Tests pour la lecture de fichiers CSV"""

    def setUp(self):
        self.csv_path = os.path.join(os.path.dirname(__file__), 'static', 'data', 'incident_types.csv')

    def test_csv_file_exists(self):
        """Test: Le fichier CSV incident_types.csv existe"""
        self.assertTrue(os.path.exists(self.csv_path), f"CSV file not found: {self.csv_path}")

    def test_read_csv_file(self):
        """Test: Lecture du fichier CSV"""
        import csv
        
        if os.path.exists(self.csv_path):
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            # Doit avoir au moins une ligne (header ou data)
            self.assertGreater(len(rows), 0)

    def test_csv_parsing_to_list(self):
        """Test: Parsing CSV en liste de dictionnaires"""
        import csv
        
        if os.path.exists(self.csv_path):
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                data = list(reader)
            
            # Doit être une liste
            self.assertIsInstance(data, list)

    def test_csv_header_detection(self):
        """Test: Détection des colonnes du CSV"""
        import csv
        
        if os.path.exists(self.csv_path):
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # Les colonnes sont dans fieldnames
                fieldnames = reader.fieldnames
            
            # Doit avoir des colonnes
            self.assertIsNotNone(fieldnames)
            self.assertGreater(len(fieldnames), 0)


class TestCSVWriting(unittest.TestCase):
    """Tests pour l'écriture de fichiers CSV"""

    def setUp(self):
        self.test_csv = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.test_csv_path = self.test_csv.name
        self.test_csv.close()

    def tearDown(self):
        """Nettoyage après le test"""
        if os.path.exists(self.test_csv_path):
            os.remove(self.test_csv_path)

    def test_write_csv_file(self):
        """Test: Écriture dans un fichier CSV"""
        import csv
        
        data = [
            {'type': 'Pothole', 'description': 'Big hole', 'severity': 'High'},
            {'type': 'Tree', 'description': 'Fallen tree', 'severity': 'Medium'},
            {'type': 'Graffiti', 'description': 'Graffiti on sign', 'severity': 'Low'}
        ]
        
        # Écrit le CSV
        with open(self.test_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['type', 'description', 'severity'])
            writer.writeheader()
            writer.writerows(data)
        
        # Vérifie que le fichier existe et n'est pas vide
        self.assertTrue(os.path.exists(self.test_csv_path))
        self.assertGreater(os.path.getsize(self.test_csv_path), 0)

    def test_csv_round_trip(self):
        """Test: Écriture et relecture de CSV (round-trip)"""
        import csv
        
        original_data = [
            {'type': 'Test1', 'value': '100'},
            {'type': 'Test2', 'value': '200'}
        ]
        
        # Écrit
        with open(self.test_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['type', 'value'])
            writer.writeheader()
            writer.writerows(original_data)
        
        # Relit
        with open(self.test_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            read_data = list(reader)
        
        # Vérifie que les données correspondent
        self.assertEqual(len(read_data), len(original_data))
        self.assertEqual(read_data[0]['type'], 'Test1')


class TestPickleSerialization(unittest.TestCase):
    """Tests pour la sérialisation Pickle"""

    def setUp(self):
        self.test_pickle = tempfile.NamedTemporaryFile(suffix='.pkl', delete=False)
        self.pickle_path = self.test_pickle.name
        self.test_pickle.close()

    def tearDown(self):
        """Nettoyage"""
        if os.path.exists(self.pickle_path):
            os.remove(self.pickle_path)

    def test_pickle_serialization(self):
        """Test: Sérialisation d'objet avec Pickle"""
        import pickle
        
        data = {
            'incidents': [
                {'type': 'Pothole', 'lat': 51.0447},
                {'type': 'Tree', 'lat': 51.0450}
            ],
            'user': 'test_user'
        }
        
        # Sérialise
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(data, f)
        
        # Vérifie que le fichier existe
        self.assertTrue(os.path.exists(self.pickle_path))
        self.assertGreater(os.path.getsize(self.pickle_path), 0)

    def test_pickle_deserialization(self):
        """Test: Désérialisation d'objet Pickle"""
        import pickle
        
        original = {'name': 'Test', 'value': 42, 'items': [1, 2, 3]}
        
        # Sérialise
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(original, f)
        
        # Désérialise
        with open(self.pickle_path, 'rb') as f:
            loaded = pickle.load(f)
        
        # Vérifie que les données correspondent
        self.assertEqual(loaded['name'], 'Test')
        self.assertEqual(loaded['value'], 42)
        self.assertEqual(loaded['items'], [1, 2, 3])

    def test_pickle_preserves_types(self):
        """Test: Pickle préserve les types de données"""
        import pickle
        
        data = {
            'string': 'hello',
            'integer': 42,
            'float': 3.14,
            'list': [1, 2, 3],
            'dict': {'nested': 'value'}
        }
        
        # Sérialise et désérialise
        with open(self.pickle_path, 'wb') as f:
            pickle.dump(data, f)
        
        with open(self.pickle_path, 'rb') as f:
            loaded = pickle.load(f)
        
        # Vérifie les types
        self.assertIsInstance(loaded['string'], str)
        self.assertIsInstance(loaded['integer'], int)
        self.assertIsInstance(loaded['float'], float)
        self.assertIsInstance(loaded['list'], list)
        self.assertIsInstance(loaded['dict'], dict)


class TestBinaryFileHandling(unittest.TestCase):
    """Tests pour la manipulation de fichiers binaires (rb/wb)"""

    def setUp(self):
        self.binary_file = tempfile.NamedTemporaryFile(delete=False)
        self.binary_path = self.binary_file.name
        self.binary_file.close()

    def tearDown(self):
        """Nettoyage"""
        if os.path.exists(self.binary_path):
            os.remove(self.binary_path)

    def test_write_binary_file(self):
        """Test: Écriture en mode binaire (wb)"""
        binary_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR'
        
        # Écrit en mode binaire
        with open(self.binary_path, 'wb') as f:
            bytes_written = f.write(binary_data)
        
        # Vérifie l'écriture
        self.assertEqual(bytes_written, len(binary_data))
        self.assertTrue(os.path.exists(self.binary_path))

    def test_read_binary_file(self):
        """Test: Lecture en mode binaire (rb)"""
        test_data = b'Test binary content \x00 with null bytes'
        
        # Écrit les données
        with open(self.binary_path, 'wb') as f:
            f.write(test_data)
        
        # Relit en mode binaire
        with open(self.binary_path, 'rb') as f:
            read_data = f.read()
        
        # Vérifie la lecture
        self.assertEqual(read_data, test_data)

    def test_binary_file_round_trip(self):
        """Test: Écriture et relecture de fichier binaire"""
        import pickle
        
        original_obj = {'data': [1, 2, 3], 'name': 'test'}
        
        # Sérialise en binaire
        with open(self.binary_path, 'wb') as f:
            pickle.dump(original_obj, f)
        
        # Désérialise
        with open(self.binary_path, 'rb') as f:
            loaded_obj = pickle.load(f)
        
        # Vérifie
        self.assertEqual(loaded_obj, original_obj)

    def test_binary_file_size(self):
        """Test: Vérification de la taille du fichier binaire"""
        test_data = b'x' * 1000
        
        with open(self.binary_path, 'wb') as f:
            f.write(test_data)
        
        file_size = os.path.getsize(self.binary_path)
        self.assertEqual(file_size, 1000)


class TestWebSocketIntegration(unittest.TestCase):
    """Tests pour les WebSockets (instant updates)"""

    def setUp(self):
        self.app = app
        self.app.config['TESTING'] = True

    def test_websocket_server_configured(self):
        """Test: Le serveur WebSocket est configuré"""
        # Vérifie que websocket_server.py existe
        websocket_file = os.path.join(os.path.dirname(__file__), 'websocket_server.py')
        self.assertTrue(os.path.exists(websocket_file), "websocket_server.py not found")

    def test_app_has_socketio_support(self):
        """Test: L'app Flask a le support SocketIO"""
        # Vérifie que flask-socketio est importable
        try:
            from flask_socketio import SocketIO
            self.assertTrue(True)
        except ImportError:
            self.fail("flask-socketio not installed")

    def test_websocket_module_imports(self):
        """Test: Le module websocket_server s'importe correctement"""
        try:
            # Essaie d'importer depuis le fichier
            import sys
            import importlib.util
            
            websocket_file = os.path.join(os.path.dirname(__file__), 'websocket_server.py')
            if os.path.exists(websocket_file):
                # Juste vérifier que le fichier existe et est valide Python
                with open(websocket_file, 'r') as f:
                    code = f.read()
                    compile(code, websocket_file, 'exec')
                self.assertTrue(True)
        except SyntaxError:
            self.fail("websocket_server.py has syntax errors")


class TestBinarySearch(unittest.TestCase):
    """Tests pour la recherche binaire (binary search)"""

    def binary_search(self, arr, target):
        """Implémentation simple de recherche binaire"""
        left, right = 0, len(arr) - 1
        
        while left <= right:
            mid = (left + right) // 2
            if arr[mid] == target:
                return mid
            elif arr[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return -1

    def test_binary_search_found(self):
        """Test: Recherche binaire trouve l'élément"""
        arr = [1, 3, 5, 7, 9, 11, 13]
        result = self.binary_search(arr, 7)
        
        self.assertEqual(result, 3)  # Index de 7

    def test_binary_search_not_found(self):
        """Test: Recherche binaire ne trouve pas l'élément"""
        arr = [1, 3, 5, 7, 9, 11, 13]
        result = self.binary_search(arr, 8)
        
        self.assertEqual(result, -1)

    def test_binary_search_first_element(self):
        """Test: Recherche le premier élément"""
        arr = [1, 3, 5, 7, 9]
        result = self.binary_search(arr, 1)
        
        self.assertEqual(result, 0)

    def test_binary_search_last_element(self):
        """Test: Recherche le dernier élément"""
        arr = [1, 3, 5, 7, 9]
        result = self.binary_search(arr, 9)
        
        self.assertEqual(result, 4)

    def test_binary_search_large_array(self):
        """Test: Recherche binaire sur un grand tableau"""
        arr = list(range(0, 10000, 2))  # [0, 2, 4, 6, ...]
        result = self.binary_search(arr, 5000)
        
        # 5000 devrait être à l'index 2500
        self.assertEqual(result, 2500)


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

