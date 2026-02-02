"""
test_database.py
Tests pour la base de données SQLite - Schéma, contraintes, persistance

Importance: Les tests de base de données vérifient que les données sont stockées correctement,
que le schéma est valide, et que les contraintes d'intégrité sont respectées.
C'est fondamental pour la fiabilité de l'application.
"""

import unittest
import sqlite3
import sys
import os
import tempfile

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


class TestDatabaseInitialization(unittest.TestCase):
    """
    Tests de l'initialisation de la base de données
    
    Vérifie que:
    - Le fichier de base de données est créé
    - La table 'incidents' existe
    - Le schéma est correct
    """

    def setUp(self):
        """
        Configuration avant chaque test
        - Initialise l'application Flask
        - Initialise la base de données
        """
        self.app = app
        self.app.config['TESTING'] = True
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db, DB_PATH
            self.db_path = DB_PATH
            init_db()

    def test_database_file_exists(self):
        """
        Test: Le fichier incidents.db existe après initialisation
        Importance: Vérifie que la base de données est créée au démarrage de l'app
        """
        self.assertTrue(os.path.exists(self.db_path), 
                       f"Database file not found at {self.db_path}")

    def test_database_is_valid_sqlite(self):
        """
        Test: Le fichier est une base de données SQLite valide
        Importance: Vérifie que le fichier n'est pas corrompu et peut être ouvert
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Exécute une requête simple pour vérifier que c'est une BD valide
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            conn.close()
            
            # Doit avoir au moins une table
            self.assertGreater(len(tables), 0)
        except Exception as e:
            self.fail(f"Database is not valid SQLite: {e}")

    def test_incidents_table_exists(self):
        """
        Test: La table 'incidents' existe dans la base de données
        Importance: Vérifie que la structure de base de la BD est en place
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Cherche la table 'incidents'
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
        result = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(result, "incidents table not found")

    def test_incidents_table_has_required_columns(self):
        """
        Test: La table incidents a toutes les colonnes requises
        Importance: Vérifie que le schéma de la BD est correct (id, type, lat, lon, timestamp)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupère les informations sur les colonnes
        cursor.execute("PRAGMA table_info(incidents);")
        columns = cursor.fetchall()
        conn.close()
        
        # Extrait les noms des colonnes
        column_names = [col[1] for col in columns]
        
        # Vérifie que toutes les colonnes requises sont présentes
        required_columns = ['id', 'type', 'latitude', 'longitude', 'timestamp']
        for col in required_columns:
            self.assertIn(col, column_names, 
                         f"Column '{col}' not found in incidents table")

    def test_id_column_is_primary_key(self):
        """
        Test: La colonne 'id' est la clé primaire
        Importance: Vérifie que chaque incident peut être identifié uniquement
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Récupère les infos sur les colonnes
        cursor.execute("PRAGMA table_info(incidents);")
        columns = cursor.fetchall()
        conn.close()
        
        # Cherche la colonne 'id'
        id_column = [col for col in columns if col[1] == 'id']
        
        self.assertTrue(id_column, "id column not found")
        # col[5] = 1 si primary key, 0 sinon
        self.assertEqual(id_column[0][5], 1, "id column is not a primary key")


class TestDatabaseConstraints(unittest.TestCase):
    """
    Tests des contraintes d'intégrité de la base de données
    
    Vérifie que:
    - Les colonnes NOT NULL sont respectées
    - Les données invalides sont rejetées
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db, DB_PATH
            self.db_path = DB_PATH
            init_db()

    def test_latitude_not_null_constraint(self):
        """
        Test: La colonne latitude ne peut pas être NULL
        Importance: Vérifie que tous les incidents ont une position géographique valide
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tente d'insérer sans latitude (doit échouer)
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute('''
                INSERT INTO incidents (type, description, longitude, timestamp, status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Test', 'Test', -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
            conn.commit()
        
        conn.close()

    def test_longitude_not_null_constraint(self):
        """
        Test: La colonne longitude ne peut pas être NULL
        Importance: Vérifie que tous les incidents ont une position géographique valide (longitude)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tente d'insérer sans longitude (doit échouer)
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute('''
                INSERT INTO incidents (type, description, latitude, timestamp, status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Test', 'Test', 51.0447, '2024-02-02T10:00:00Z', 'unsolved'))
            conn.commit()
        
        conn.close()

    def test_type_not_null_constraint(self):
        """
        Test: La colonne type ne peut pas être NULL
        Importance: Vérifie que tous les incidents ont une catégorie
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tente d'insérer sans type (doit échouer)
        with self.assertRaises(sqlite3.IntegrityError):
            cursor.execute('''
                INSERT INTO incidents (description, latitude, longitude, timestamp, status)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Test', 51.0447, -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
            conn.commit()
        
        conn.close()


class TestDatabasePersistence(unittest.TestCase):
    """
    Tests de la persistance et récupération des données
    
    Vérifie que:
    - Les données insérées sont correctement stockées
    - Les données peuvent être récupérées intégralement
    - Les modifications sont persistantes
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db, DB_PATH
            self.db_path = DB_PATH
            init_db()

    def test_insert_and_retrieve_incident(self):
        """
        Test: Insérer un incident, puis le récupérer et vérifier les données
        Importance: Vérifie que l'insertion ET la lecture fonctionnent correctement
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Données d'insertion
        test_data = {
            'type': 'Nid de poule',
            'description': 'Grand trou dans la route',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z'
        }
        
        # Insère l'incident
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (test_data['type'], test_data['description'], test_data['latitude'],
              test_data['longitude'], test_data['timestamp'], 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère l'incident
        cursor.execute('SELECT type, description, latitude, longitude, timestamp FROM incidents WHERE id = ?',
                      (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        # Vérifie que les données correspondent
        self.assertEqual(result[0], test_data['type'])
        self.assertEqual(result[1], test_data['description'])
        self.assertAlmostEqual(result[2], test_data['latitude'], places=4)
        self.assertAlmostEqual(result[3], test_data['longitude'], places=4)
        self.assertEqual(result[4], test_data['timestamp'])

    def test_multiple_incidents_stored_independently(self):
        """
        Test: Plusieurs incidents peuvent être insérés et récupérés indépendamment
        Importance: Vérifie que les données ne se mélangent pas et que chaque incident est unique
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insère 3 incidents différents
        incidents = [
            ('Pothole', 'Large hole', 51.0447, -115.3667, '2024-02-02T10:00:00Z'),
            ('Tree', 'Fallen tree', 51.0450, -115.3670, '2024-02-02T11:00:00Z'),
            ('Graffiti', 'Graffiti on sign', 51.0445, -115.3665, '2024-02-02T12:00:00Z')
        ]
        
        ids = []
        for incident in incidents:
            cursor.execute('''
                INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (*incident, 'unsolved'))
            ids.append(cursor.lastrowid)
        
        conn.commit()
        
        # Récupère tous les incidents et vérifie leur unicité
        cursor.execute('SELECT id, type FROM incidents ORDER BY id')
        results = cursor.fetchall()
        conn.close()
        
        # Vérifie qu'on a au moins 3 incidents avec des types différents
        self.assertGreaterEqual(len(results), 3)
        types = [r[1] for r in results]
        self.assertIn('Pothole', types)
        self.assertIn('Tree', types)
        self.assertIn('Graffiti', types)


class TestDatabaseAutoIncrement(unittest.TestCase):
    """
    Tests de l'auto-incrémentation des IDs
    
    Vérifie que:
    - Chaque nouvel incident reçoit un ID unique
    - Les IDs augmentent séquentiellement
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db, DB_PATH
            self.db_path = DB_PATH
            init_db()

    def test_autoincrement_ids(self):
        """
        Test: Les IDs s'auto-incrémentent correctement
        Importance: Vérifie que chaque incident reçoit un ID unique et séquentiel
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insère 2 incidents et récupère leurs IDs
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
        
        # Vérifie que les IDs sont différents et croissants
        self.assertNotEqual(id1, id2)
        self.assertLess(id1, id2)
        self.assertEqual(id2, id1 + 1)  # Doit être séquentiel

    def test_id_uniqueness(self):
        """
        Test: Aucun ID dupliqué n'existe
        Importance: Vérifie que chaque incident a un ID unique (contrainte PRIMARY KEY)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insère plusieurs incidents
        for i in range(5):
            cursor.execute('''
                INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (f'Type{i}', f'Desc{i}', 51.0447, -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
        
        conn.commit()
        
        # Récupère tous les IDs
        cursor.execute('SELECT id FROM incidents ORDER BY id')
        ids = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        # Vérifie qu'il n'y a pas de doublons
        self.assertEqual(len(ids), len(set(ids)))


class TestSpecialCharactersHandling(unittest.TestCase):
    """
    Tests de la gestion des caractères spéciaux (accents, tirets, etc.)
    
    Vérifie que:
    - Les caractères français (é, è, ê, ç, etc.) sont stockés correctement
    - Les caractères spéciaux sont récupérés sans corruption
    - L'encodage UTF-8 est correctement géré
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        
        with self.app.app_context():
            from server.routes.incidents_api import init_db, DB_PATH
            self.db_path = DB_PATH
            init_db()

    def test_accents_stored_correctly(self):
        """
        Test: Les caractères accentués (é, è, ê, etc.) sont stockés correctement
        Importance: Vérifie que le français est supporté (Canmore est bilingue)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Données avec accents
        text_with_accents = "Nid de poule à côté du café"
        
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (text_with_accents, "Description avec accénts: é à ù", 
              51.0447, -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère et vérifie
        cursor.execute('SELECT type, description FROM incidents WHERE id = ?', (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], text_with_accents)
        self.assertIn('é', result[1])

    def test_special_characters_in_description(self):
        """
        Test: Les caractères spéciaux (tirets, apostrophes, etc.) sont stockés correctement
        Importance: Vérifie que les descriptions naturelles peuvent contenir du texte formaté
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Description avec caractères spéciaux
        description = "L'arbre s'est tombé - grand dommage!"
        
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Arbre tombé', description, 51.0447, -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère et vérifie
        cursor.execute('SELECT description FROM incidents WHERE id = ?', (incident_id,))
        result = cursor.fetchone()
        conn.close()
        
        self.assertEqual(result[0], description)

    def test_unicode_characters_round_trip(self):
        """
        Test: Les caractères unicode font un aller-retour correct (insert → retrieve)
        Importance: Vérifie que l'encodage UTF-8 ne corrompt pas les données
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Texte avec nombreux caractères spéciaux
        original_text = "Éclairage défaillant - Escalier à côté du café"
        
        cursor.execute('''
            INSERT INTO incidents (type, description, latitude, longitude, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('Éclairage', original_text, 51.0447, -115.3667, '2024-02-02T10:00:00Z', 'unsolved'))
        
        incident_id = cursor.lastrowid
        conn.commit()
        
        # Récupère
        cursor.execute('SELECT description FROM incidents WHERE id = ?', (incident_id,))
        retrieved_text = cursor.fetchone()[0]
        conn.close()
        
        # Doit être identique
        self.assertEqual(original_text, retrieved_text)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
