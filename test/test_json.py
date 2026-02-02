"""
test_json.py
Tests pour la sérialisation JSON - Conversion, caractères spéciaux, structures imbriquées

Importance: Les tests JSON vérifient que les données Python peuvent être converties en JSON
et reconstruites sans perte d'information. C'est essentiel pour la communication avec les clients
et le stockage des données. Les caractères spéciaux et structures imbriquées doivent être gérés correctement.
"""

import unittest
import json
import sys
import os
from datetime import datetime

# Ajoute le répertoire parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import app
except ImportError as e:
    print(f"Erreur d'import: {e}")
    sys.exit(1)


class TestJSONRoundTrip(unittest.TestCase):
    """
    Tests pour la conversion aller-retour JSON
    
    Vérifie que:
    - Dict Python → JSON → Dict Python récupère les données identiques
    - Les types de base (str, int, float, bool) sont préservés
    - Les structures simples sont correctement sérialisées
    """

    def test_simple_dict_round_trip(self):
        """
        Test: Dict simple peut faire un aller-retour JSON
        Importance: Vérifie la base de la sérialisation JSON
        """
        original = {
            'type': 'Nid de poule',
            'latitude': 51.0447,
            'longitude': -115.3667
        }
        
        # Sérialise en JSON
        json_string = json.dumps(original)
        
        # Désérialise
        recovered = json.loads(json_string)
        
        # Doit être identique
        self.assertEqual(original, recovered)

    def test_string_type_preserved(self):
        """
        Test: Type string est préservé après aller-retour JSON
        Importance: Vérifie que les chaînes restent des chaînes
        """
        original = {'description': 'Test string value'}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertIsInstance(recovered['description'], str)
        self.assertEqual(recovered['description'], 'Test string value')

    def test_integer_type_preserved(self):
        """
        Test: Type int est préservé après aller-retour JSON
        Importance: Vérifie que les entiers restent des entiers
        """
        original = {'count': 42, 'id': 1}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertIsInstance(recovered['count'], int)
        self.assertEqual(recovered['count'], 42)

    def test_float_type_preserved(self):
        """
        Test: Type float est préservé après aller-retour JSON
        Importance: Vérifie que les nombres décimaux restent des floats
        """
        original = {'latitude': 51.0447, 'longitude': -115.3667}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertIsInstance(recovered['latitude'], float)
        self.assertAlmostEqual(recovered['latitude'], 51.0447, places=4)

    def test_boolean_type_preserved(self):
        """
        Test: Type bool (true/false) est préservé après aller-retour JSON
        Importance: Vérifie que les booléens deviennent True/False en JSON (pas "true"/"false")
        """
        original = {'active': True, 'deleted': False}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertIsInstance(recovered['active'], bool)
        self.assertTrue(recovered['active'])
        self.assertFalse(recovered['deleted'])

    def test_null_value_preserved(self):
        """
        Test: Valeur null/None est préservée
        Importance: Vérifie que les champs vides sont correctement représentés en JSON
        """
        original = {'description': None, 'type': 'Test'}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertIsNone(recovered['description'])
        self.assertEqual(recovered['type'], 'Test')

    def test_empty_dict_round_trip(self):
        """
        Test: Dict vide peut faire un aller-retour JSON
        Importance: Vérifie les cas limites
        """
        original = {}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)

    def test_dict_with_many_fields_round_trip(self):
        """
        Test: Dict avec de nombreux champs peut faire un aller-retour JSON
        Importance: Vérifie la sérialisation de structures complexes
        """
        original = {
            'id': 1,
            'type': 'Nid de poule',
            'description': 'Grand trou',
            'latitude': 51.0447,
            'longitude': -115.3667,
            'timestamp': '2024-02-02T10:00:00Z',
            'status': 'unsolved',
            'priority': 'high'
        }
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)


class TestSpecialCharactersJSON(unittest.TestCase):
    """
    Tests pour la gestion des caractères spéciaux en JSON
    
    Vérifie que:
    - Les caractères accentués (é, è, ê, ç) sont correctement encodés/décodés
    - Les caractères unicode sont préservés
    - Les caractères d'échappement spéciaux (quotes, backslash) sont gérés
    """

    def test_french_accents_preserved(self):
        """
        Test: Les accents français (é, è, ê, ç) sont préservés en JSON
        Importance: Canmore est bilingue, le français doit être supporté
        """
        original = {
            'description': 'Nid de poule à côté du café',
            'type': 'Escalier défaillant'
        }
        
        json_string = json.dumps(original, ensure_ascii=False)
        recovered = json.loads(json_string)
        
        self.assertEqual(original['description'], recovered['description'])
        self.assertEqual(original['type'], recovered['type'])
        self.assertIn('é', recovered['description'])
        self.assertIn('é', recovered['type'])

    def test_accents_with_ensure_ascii(self):
        """
        Test: Les accents sont préservés même avec ensure_ascii=True
        Importance: Vérifie que l'encodage en unicode escape (\\uXXXX) fonctionne
        """
        original = {'city': 'Éclairage défaillant'}
        
        # Sérialise avec ensure_ascii=True (défaut)
        json_string = json.dumps(original, ensure_ascii=True)
        
        # Doit contenir des escapes unicode
        self.assertIn('\\u', json_string)
        
        # Mais la désérialisation doit retrouver les accents
        recovered = json.loads(json_string)
        self.assertEqual(original['city'], recovered['city'])

    def test_double_quotes_escaped(self):
        """
        Test: Les guillemets doubles sont correctement échappés en JSON
        Importance: Vérifie que les descriptions avec guillemets ne cassent pas le JSON
        """
        original = {'description': 'L\'arbre a dit: "Attention!"'}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original['description'], recovered['description'])

    def test_backslash_escaped(self):
        """
        Test: Les backslashs sont correctement échappés
        Importance: Vérifie que les chemins Windows (C:\\path\\file) sont gérés
        """
        original = {'path': 'C:\\Users\\Documents\\file.txt'}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original['path'], recovered['path'])

    def test_newline_characters_preserved(self):
        """
        Test: Les caractères de nouvelle ligne sont préservés en JSON
        Importance: Vérifie que les descriptions multi-lignes restent intactes
        """
        original = {'description': 'Ligne 1\nLigne 2\nLigne 3'}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original['description'], recovered['description'])
        self.assertIn('\n', recovered['description'])

    def test_tab_characters_preserved(self):
        """
        Test: Les caractères de tabulation sont préservés
        Importance: Vérifie que le formatage avec tabs est conservé
        """
        original = {'description': 'Column1\tColumn2\tColumn3'}
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original['description'], recovered['description'])

    def test_special_math_symbols(self):
        """
        Test: Les symboles mathématiques spéciaux sont préservés
        Importance: Vérifie que les caractères unicode au-delà de ASCII sont gérés
        """
        original = {
            'symbols': '± × ÷ ° μ',
            'currency': '€ £ ¥'
        }
        
        json_string = json.dumps(original, ensure_ascii=False)
        recovered = json.loads(json_string)
        
        self.assertEqual(original['symbols'], recovered['symbols'])
        self.assertEqual(original['currency'], recovered['currency'])

    def test_emoji_preserved(self):
        """
        Test: Les emojis sont préservés en JSON
        Importance: Vérifie que les caractères unicode 4-bytes (emoji) sont gérés
        """
        original = {'description': 'Urgent! ⚠️ 🚨'}
        
        json_string = json.dumps(original, ensure_ascii=False)
        recovered = json.loads(json_string)
        
        self.assertEqual(original['description'], recovered['description'])
        self.assertIn('⚠️', recovered['description'])


class TestNestedStructures(unittest.TestCase):
    """
    Tests pour les structures imbriquées en JSON
    
    Vérifie que:
    - Les listes de dicts sont sérialisées correctement
    - Les dicts contenant des listes sont préservés
    - Les structures profondément imbriquées sont gérées
    """

    def test_list_of_dicts(self):
        """
        Test: Liste de dicts peut faire un aller-retour JSON
        Importance: Vérifie que les collections d'incidents sont correctement sérialisées
        """
        original = [
            {'id': 1, 'type': 'Pothole', 'lat': 51.0447},
            {'id': 2, 'type': 'Tree', 'lat': 51.0450},
            {'id': 3, 'type': 'Graffiti', 'lat': 51.0445}
        ]
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(len(recovered), 3)
        self.assertEqual(recovered[0]['type'], 'Pothole')

    def test_dict_with_list_of_strings(self):
        """
        Test: Dict contenant une liste de chaînes peut faire un aller-retour JSON
        Importance: Vérifie que les listes de tags ou catégories sont gérées
        """
        original = {
            'id': 1,
            'type': 'Multi-hazard',
            'tags': ['urgent', 'safety', 'road']
        }
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(recovered['tags'], ['urgent', 'safety', 'road'])

    def test_dict_with_list_of_numbers(self):
        """
        Test: Dict contenant une liste de nombres peut faire un aller-retour JSON
        Importance: Vérifie que les coordonnées multiples ou statistiques sont gérées
        """
        original = {
            'incident_id': 1,
            'coordinates': [51.0447, -115.3667],
            'severity_history': [1, 2, 3, 2, 1]
        }
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(recovered['coordinates'], [51.0447, -115.3667])

    def test_nested_dict_in_dict(self):
        """
        Test: Dict contenant un dict imbriqué peut faire un aller-retour JSON
        Importance: Vérifie que les structures hiérarchiques sont gérées
        """
        original = {
            'incident': {
                'id': 1,
                'location': {
                    'latitude': 51.0447,
                    'longitude': -115.3667
                },
                'reporter': {
                    'name': 'John Doe',
                    'email': 'john@example.com'
                }
            }
        }
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(recovered['incident']['location']['latitude'], 51.0447)
        self.assertEqual(recovered['incident']['reporter']['name'], 'John Doe')

    def test_deeply_nested_structure(self):
        """
        Test: Structure profondément imbriquée (4+ niveaux) peut faire un aller-retour JSON
        Importance: Vérifie que les structures complexes ne cassent pas la sérialisation
        """
        original = {
            'level1': {
                'level2': {
                    'level3': {
                        'level4': {
                            'value': 'deep value'
                        }
                    }
                }
            }
        }
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(recovered['level1']['level2']['level3']['level4']['value'], 'deep value')

    def test_list_of_dicts_with_nested_lists(self):
        """
        Test: Liste de dicts contenant des listes peut faire un aller-retour JSON
        Importance: Vérifie que les structures multi-dimensionnelles sont gérées
        """
        original = [
            {
                'id': 1,
                'type': 'Pothole',
                'coordinates': [51.0447, -115.3667],
                'tags': ['urgent', 'safety']
            },
            {
                'id': 2,
                'type': 'Tree',
                'coordinates': [51.0450, -115.3670],
                'tags': ['environment']
            }
        ]
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(len(recovered), 2)
        self.assertEqual(recovered[0]['tags'], ['urgent', 'safety'])

    def test_empty_nested_structures(self):
        """
        Test: Structures imbriquées vides peuvent faire un aller-retour JSON
        Importance: Vérifie que les listes et dicts vides sont gérés
        """
        original = {
            'incidents': [],
            'metadata': {},
            'notes': ''
        }
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(recovered['incidents'], [])
        self.assertEqual(recovered['metadata'], {})

    def test_mixed_nested_types(self):
        """
        Test: Structure avec types mixtes imbriqués (lists, dicts, strings, numbers)
        Importance: Vérifie que tous les types JSON coexistent correctement dans une structure
        """
        original = {
            'id': 1,
            'name': 'Complex Incident',
            'priority': 8.5,
            'active': True,
            'notes': None,
            'tags': ['urgent', 'safety'],
            'location': {
                'latitude': 51.0447,
                'longitude': -115.3667,
                'address': 'Main Street'
            },
            'history': [
                {'timestamp': '2024-02-02T10:00:00Z', 'status': 'reported'},
                {'timestamp': '2024-02-02T11:00:00Z', 'status': 'in_progress'},
                {'timestamp': '2024-02-02T12:00:00Z', 'status': 'resolved'}
            ]
        }
        
        json_string = json.dumps(original)
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)
        self.assertEqual(recovered['name'], 'Complex Incident')
        self.assertEqual(len(recovered['history']), 3)
        self.assertIsNone(recovered['notes'])


class TestJSONFormatting(unittest.TestCase):
    """
    Tests pour le formatage et la lisibilité du JSON
    
    Vérifie que:
    - Le JSON peut être formaté (indentation)
    - Le JSON compact est aussi valid
    - Les sauts de ligne ne cassent pas la désérialisation
    """

    def test_compact_json_valid(self):
        """
        Test: JSON compact (une ligne) peut être désérialisé
        Importance: Vérifie que le JSON minifié fonctionne correctement
        """
        original = {'type': 'Test', 'latitude': 51.0447}
        
        # JSON compact (sans indentation)
        json_string = json.dumps(original, separators=(',', ':'))
        
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)

    def test_formatted_json_valid(self):
        """
        Test: JSON formaté (indentation, sauts de ligne) peut être désérialisé
        Importance: Vérifie que le JSON lisible fonctionne correctement
        """
        original = {'type': 'Test', 'latitude': 51.0447}
        
        # JSON formaté (avec indentation et sauts de ligne)
        json_string = json.dumps(original, indent=2)
        
        recovered = json.loads(json_string)
        
        self.assertEqual(original, recovered)

    def test_multiline_json_parsing(self):
        """
        Test: JSON multi-lignes (avec des sauts de ligne internes) peut être parsé
        Importance: Vérifie que les fichiers JSON multi-lignes sont gérés
        """
        json_string = '''{
    "type": "Pothole",
    "latitude": 51.0447,
    "longitude": -115.3667,
    "tags": ["urgent", "safety"]
}'''
        
        recovered = json.loads(json_string)
        
        self.assertEqual(recovered['type'], 'Pothole')
        self.assertEqual(recovered['tags'], ['urgent', 'safety'])

    def test_json_with_extra_whitespace(self):
        """
        Test: JSON avec espaces et tabulations supplémentaires peut être parsé
        Importance: Vérifie la tolérance du parsing pour les espacements variables
        """
        json_string = '''{
            "type"  :  "Test"  ,
            "value" : 42
        }'''
        
        recovered = json.loads(json_string)
        
        self.assertEqual(recovered['type'], 'Test')
        self.assertEqual(recovered['value'], 42)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
