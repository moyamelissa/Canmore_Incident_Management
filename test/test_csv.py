"""
test_csv.py
Tests pour la lecture et écriture de fichiers CSV - Parsing, headers, round-trip

Importance: Les tests CSV vérifient que les données de référence (incident_types.csv)
peuvent être lues correctement, que les données peuvent être écrites et relues sans perte,
et que les headers sont détectés correctement. C'est essentiel pour le chargement des types
d'incidents et l'export de données.
"""

import unittest
import csv
import tempfile
import os
import sys

# Ajoute le répertoire parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import app
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)


class TestCSVFileReading(unittest.TestCase):
    """
    Tests pour la lecture des fichiers CSV
    
    Vérifie que:
    - Le fichier incident_types.csv existe
    - Le fichier peut être ouvert et lu
    - Le fichier n'est pas vide
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        
        # Chemin du fichier incident_types.csv
        self.csv_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'static',
            'data',
            'incident_types.csv'
        )

    def test_incident_types_csv_exists(self):
        """
        Test: Le fichier incident_types.csv existe
        Importance: Vérifie que le fichier de données de base existe et est accessible
        """
        self.assertTrue(os.path.exists(self.csv_path),
                       f"incident_types.csv not found at {self.csv_path}")

    def test_incident_types_csv_is_readable(self):
        """
        Test: Le fichier incident_types.csv peut être lu
        Importance: Vérifie que le fichier n'est pas corrompu et a les bonnes permissions
        """
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.assertGreater(len(content), 0, "CSV file is empty")
        except Exception as e:
            self.fail(f"Cannot read CSV file: {e}")

    def test_incident_types_csv_not_empty(self):
        """
        Test: Le fichier incident_types.csv contient des données
        Importance: Vérifie que le fichier n'est pas vide et contient au least un header
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Doit avoir au least le header
        self.assertGreater(len(rows), 0, "CSV file has no rows")

    def test_incident_types_csv_has_multiple_rows(self):
        """
        Test: Le fichier incident_types.csv a au least 2 lignes (header + 1 incident)
        Importance: Vérifie qu'il y a des types d'incidents définis
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Doit avoir header + au least 1 incident type
        self.assertGreater(len(rows), 1, "CSV file has no data rows")


class TestCSVParsing(unittest.TestCase):
    """
    Tests pour le parsing des fichiers CSV
    
    Vérifie que:
    - Les lignes peuvent être lues comme listes (reader)
    - Les lignes peuvent être lues comme dicts (DictReader)
    - Les deux méthodes donnent les mêmes données
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        
        # Chemin du fichier incident_types.csv
        self.csv_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'static',
            'data',
            'incident_types.csv'
        )

    def test_read_csv_as_list_rows(self):
        """
        Test: Fichier CSV peut être lu comme liste de listes
        Importance: Vérifie le parsing basique avec csv.reader()
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        # Doit retourner une liste
        self.assertIsInstance(rows, list)
        
        # Chaque ligne doit être une liste
        for row in rows:
            self.assertIsInstance(row, list)

    def test_read_csv_as_dicts(self):
        """
        Test: Fichier CSV peut être lu comme liste de dicts (DictReader)
        Importance: Vérifie le parsing avec noms de colonnes (plus lisible)
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Doit retourner une liste
        self.assertIsInstance(rows, list)
        
        # Chaque ligne doit être un dict
        for row in rows:
            self.assertIsInstance(row, dict)

    def test_dict_reader_has_column_names(self):
        """
        Test: DictReader récupère les noms de colonnes du header
        Importance: Vérifie que les colonnes sont identifiées correctement
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        # Au less une ligne
        self.assertGreater(len(rows), 0)
        
        # Les colonnes doivent être dans chaque dict
        first_row = rows[0]
        self.assertIsInstance(first_row, dict)
        self.assertGreater(len(first_row), 0)

    def test_reader_and_dict_reader_consistency(self):
        """
        Test: csv.reader et csv.DictReader donnent les mêmes données
        Importance: Vérifie que les deux méthodes de parsing sont cohérentes
        """
        # Lecture avec reader
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows_list = list(reader)
        
        # Lecture avec DictReader
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            dict_reader = csv.DictReader(f)
            rows_dict = list(dict_reader)
        
        # Même nombre de lignes (à part le header)
        # rows_list inclut le header, rows_dict ne l'inclut pas
        self.assertEqual(len(rows_list) - 1, len(rows_dict))
        
        # Si pas vide, vérifier que les colonnes correspondent
        if len(rows_dict) > 0:
            # Nombre de colonnes doit match
            self.assertEqual(len(rows_list[0]), len(rows_dict[0]))

    def test_csv_column_count_consistent(self):
        """
        Test: Toutes les lignes du CSV ont le même nombre de colonnes
        Importance: Vérifie que le CSV n'est pas malformé (colonnes manquantes)
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
        
        if len(rows) > 0:
            first_row_length = len(rows[0])
            
            for i, row in enumerate(rows[1:], 1):
                self.assertEqual(len(row), first_row_length,
                               f"Row {i} has different column count")


class TestCSVRoundTrip(unittest.TestCase):
    """
    Tests pour l'écriture et la lecture de CSV (aller-retour)
    
    Vérifie que:
    - Données écrites dans CSV peuvent être relues
    - Les données sont intactes après aller-retour
    - Les types de données sont préservés (tant que strings)
    """

    def test_write_and_read_simple_csv(self):
        """
        Test: Écrire CSV, le relire, et vérifier que les données correspondent
        Importance: Vérifie le round-trip basique (write → read)
        """
        # Données à écrire
        data = [
            ['ID', 'Type', 'Status'],
            ['1', 'Pothole', 'unsolved'],
            ['2', 'Tree', 'resolved'],
            ['3', 'Graffiti', 'unsolved']
        ]
        
        # Écrit dans un fichier temp
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            # Relit le fichier
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                read_data = list(reader)
            
            # Doit être identique
            self.assertEqual(data, read_data)
        finally:
            os.unlink(temp_path)

    def test_write_and_read_with_dict_writer(self):
        """
        Test: Écrire CSV avec DictWriter, le relire avec DictReader
        Importance: Vérifie le round-trip avec dictionnaires (plus structuré)
        """
        # Données à écrire (liste de dicts)
        data = [
            {'id': '1', 'type': 'Pothole', 'status': 'unsolved'},
            {'id': '2', 'type': 'Tree', 'status': 'resolved'},
            {'id': '3', 'type': 'Graffiti', 'status': 'unsolved'}
        ]
        
        fieldnames = ['id', 'type', 'status']
        
        # Écrit dans un fichier temp
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        try:
            # Relit le fichier
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                read_data = list(reader)
            
            # Doit être identique
            self.assertEqual(data, read_data)
        finally:
            os.unlink(temp_path)

    def test_csv_with_commas_in_data(self):
        """
        Test: Données contenant des virgules sont correctement échappées (quoted)
        Importance: Vérifie que les données avec virgules ne cassent pas le CSV
        """
        data = [
            ['Type', 'Description'],
            ['Pothole', 'Large hole, very deep, dangerous'],
            ['Graffiti', 'Text saying "Hello, World"']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                read_data = list(reader)
            
            # Doit préserver les données avec virgules
            self.assertEqual(len(read_data), len(data))
            self.assertEqual(read_data[1][1], 'Large hole, very deep, dangerous')
        finally:
            os.unlink(temp_path)

    def test_csv_with_newlines_in_data(self):
        """
        Test: Données contenant des sauts de ligne sont correctement échappées
        Importance: Vérifie que les descriptions multi-lignes sont gérées
        """
        data = [
            ['ID', 'Description'],
            ['1', 'Line 1\nLine 2\nLine 3'],
            ['2', 'Single line']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                read_data = list(reader)
            
            # Doit préserver les sauts de ligne
            self.assertEqual(read_data[1][1], 'Line 1\nLine 2\nLine 3')
        finally:
            os.unlink(temp_path)

    def test_csv_with_quotes_in_data(self):
        """
        Test: Données contenant des guillemets sont correctement échappées
        Importance: Vérifie que les textes avec guillemets sont préservés
        """
        data = [
            ['Type', 'Message'],
            ['Sign', 'The sign says "STOP"'],
            ['Graffiti', 'Text: \'Hello World\'']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                read_data = list(reader)
            
            # Doit préserver les guillemets
            self.assertEqual(read_data[1][1], 'The sign says "STOP"')
        finally:
            os.unlink(temp_path)


class TestCSVHeader(unittest.TestCase):
    """
    Tests pour la détection et gestion des headers
    
    Vérifie que:
    - Le premier header existe et peut être récupéré
    - Les noms de colonnes peuvent être utilisés
    - Les headers sont correctement identifiés
    """

    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app
        self.app.config['TESTING'] = True
        
        self.csv_path = os.path.join(
            os.path.dirname(__file__),
            '..',
            'static',
            'data',
            'incident_types.csv'
        )

    def test_csv_header_retrieval(self):
        """
        Test: Les noms de colonnes (header) peuvent être récupérés
        Importance: Vérifie que les colonnes sont identifiables par nom
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
        
        # Le header doit être une liste de colonnes
        self.assertIsInstance(header, list)
        self.assertGreater(len(header), 0)

    def test_csv_header_with_dict_reader(self):
        """
        Test: DictReader utilise automatiquement la première ligne comme header
        Importance: Vérifie que les colonnes sont automatiquement nommées
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Les fieldnames doivent être disponibles
            self.assertIsNotNone(reader.fieldnames)
            self.assertGreater(len(reader.fieldnames), 0)

    def test_data_accessible_by_column_name(self):
        """
        Test: Les données peuvent être accédées par nom de colonne (pas seulement index)
        Importance: Vérifie que DictReader rend les données plus lisibles et robustes
        """
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if len(rows) > 0:
            first_row = rows[0]
            
            # Doit être un dict avec clés (noms de colonnes)
            self.assertIsInstance(first_row, dict)
            
            # Les clés doivent être non-vides
            for key in first_row.keys():
                self.assertIsInstance(key, str)
                self.assertGreater(len(key), 0)

    def test_custom_csv_header_detection(self):
        """
        Test: Une CSV personnalisée avec header personnalisé est correctement parsée
        Importance: Vérifie la robustesse avec des headers arbitraires
        """
        data = [
            ['CustomID', 'CustomType', 'CustomStatus'],
            ['A', 'X', 'Y'],
            ['B', 'X2', 'Y2']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            # Le header personnalisé doit être utilisé
            self.assertEqual(list(rows[0].keys()), ['CustomID', 'CustomType', 'CustomStatus'])
            self.assertEqual(rows[0]['CustomID'], 'A')
            self.assertEqual(rows[0]['CustomType'], 'X')
        finally:
            os.unlink(temp_path)


class TestCSVSpecialCharacters(unittest.TestCase):
    """
    Tests pour la gestion des caractères spéciaux en CSV
    
    Vérifie que:
    - Les accents français sont correctement stockés/lus
    - Les caractères unicode sont gérés
    - Les données multi-langues sont préservées
    """

    def test_write_and_read_french_accents(self):
        """
        Test: Accents français (é, è, ê, ç) sont préservés en CSV
        Importance: Canmore est bilingue, le français doit être supporté en CSV
        """
        data = [
            ['Type', 'Description'],
            ['Nid de poule', 'À côté du café'],
            ['Éclairage', 'Défaillant près de l\'escalier']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                read_data = list(reader)
            
            # Les accents doivent être préservés
            self.assertEqual(data, read_data)
            self.assertIn('À', read_data[1][1])
            self.assertIn('É', read_data[2][0])
        finally:
            os.unlink(temp_path)

    def test_write_and_read_special_symbols(self):
        """
        Test: Symboles spéciaux (±, ×, °) sont préservés
        Importance: Vérifie le support unicode complet
        """
        data = [
            ['Symbol', 'Meaning'],
            ['±', 'Plus or minus'],
            ['°', 'Degree'],
            ['×', 'Multiply']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                read_data = list(reader)
            
            self.assertEqual(data, read_data)
        finally:
            os.unlink(temp_path)

    def test_emoji_in_csv(self):
        """
        Test: Emojis sont préservés en CSV
        Importance: Vérifie que les caractères unicode 4-bytes sont gérés
        """
        data = [
            ['Status', 'Icon'],
            ['Urgent', '⚠️'],
            ['Emergency', '🚨']
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8', newline='') as f:
            temp_path = f.name
            writer = csv.writer(f)
            writer.writerows(data)
        
        try:
            with open(temp_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                read_data = list(reader)
            
            self.assertEqual(data, read_data)
            self.assertIn('⚠️', read_data[1][1])
        finally:
            os.unlink(temp_path)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
