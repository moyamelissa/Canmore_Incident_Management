"""
test_pickle.py
Tests pour la sérialisation Pickle - sauvegarde, rechargement, types préservés

Importance: Les tests Pickle vérifient que les objets Python peuvent être sérialisés
et rechargés sans perte. C'est essentiel pour la persistance rapide et les sauvegardes.
"""

import unittest
import pickle
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


class TestPickleRoundTrip(unittest.TestCase):
    """
    Tests pour l'aller-retour Pickle (serialize → deserialize)
    
    Vérifie que:
    - Les objets peuvent être sauvegardés dans un fichier
    - Les objets peuvent être rechargés avec les mêmes valeurs
    - Les structures simples et complexes sont supportées
    """

    def test_pickle_simple_object_round_trip(self):
        """
        Test: Objet simple (dict) peut faire un aller-retour Pickle
        Importance: Vérifie la base de la sérialisation Pickle
        """
        original = {
            'type': 'Nid de poule',
            'latitude': 51.0447,
            'longitude': -115.3667
        }

        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            with open(temp_path, 'wb') as f:
                pickle.dump(original, f)

            with open(temp_path, 'rb') as f:
                recovered = pickle.load(f)

            self.assertEqual(original, recovered)
        finally:
            os.unlink(temp_path)

    def test_pickle_list_round_trip(self):
        """
        Test: Liste d'objets peut faire un aller-retour Pickle
        Importance: Vérifie que les listes sont correctement sérialisées
        """
        original = [
            {'id': 1, 'type': 'Pothole'},
            {'id': 2, 'type': 'Tree'},
            {'id': 3, 'type': 'Graffiti'}
        ]

        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            with open(temp_path, 'wb') as f:
                pickle.dump(original, f)

            with open(temp_path, 'rb') as f:
                recovered = pickle.load(f)

            self.assertEqual(original, recovered)
        finally:
            os.unlink(temp_path)

    def test_pickle_nested_structure_round_trip(self):
        """
        Test: Structure imbriquée peut faire un aller-retour Pickle
        Importance: Vérifie que les dicts avec listes imbriquées sont préservés
        """
        original = {
            'incident': {
                'id': 1,
                'tags': ['urgent', 'safety'],
                'location': {
                    'latitude': 51.0447,
                    'longitude': -115.3667
                }
            }
        }

        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            with open(temp_path, 'wb') as f:
                pickle.dump(original, f)

            with open(temp_path, 'rb') as f:
                recovered = pickle.load(f)

            self.assertEqual(original, recovered)
        finally:
            os.unlink(temp_path)


class TestPickleTypePreservation(unittest.TestCase):
    """
    Tests pour la préservation des types avec Pickle
    
    Vérifie que:
    - Les ints restent des ints
    - Les floats restent des floats
    - Les listes restent des listes
    - Les dicts restent des dicts
    - Les booléens et None sont préservés
    """

    def test_int_type_preserved(self):
        """
        Test: Les entiers restent des int après Pickle
        Importance: Vérifie que les types numériques ne changent pas
        """
        original = 42

        data = pickle.dumps(original)
        recovered = pickle.loads(data)

        self.assertIsInstance(recovered, int)
        self.assertEqual(original, recovered)

    def test_float_type_preserved(self):
        """
        Test: Les floats restent des float après Pickle
        Importance: Vérifie la précision des nombres décimaux
        """
        original = 51.0447

        data = pickle.dumps(original)
        recovered = pickle.loads(data)

        self.assertIsInstance(recovered, float)
        self.assertAlmostEqual(original, recovered, places=4)

    def test_list_type_preserved(self):
        """
        Test: Les listes restent des listes après Pickle
        Importance: Vérifie que les collections sont préservées
        """
        original = ['a', 'b', 'c']

        data = pickle.dumps(original)
        recovered = pickle.loads(data)

        self.assertIsInstance(recovered, list)
        self.assertEqual(original, recovered)

    def test_dict_type_preserved(self):
        """
        Test: Les dicts restent des dicts après Pickle
        Importance: Vérifie que les structures clé-valeur sont préservées
        """
        original = {'key': 'value', 'number': 10}

        data = pickle.dumps(original)
        recovered = pickle.loads(data)

        self.assertIsInstance(recovered, dict)
        self.assertEqual(original, recovered)

    def test_boolean_type_preserved(self):
        """
        Test: Les booléens restent des bool après Pickle
        Importance: Vérifie que True/False ne changent pas de type
        """
        original = True

        data = pickle.dumps(original)
        recovered = pickle.loads(data)

        self.assertIsInstance(recovered, bool)
        self.assertEqual(original, recovered)

    def test_none_type_preserved(self):
        """
        Test: None est préservé après Pickle
        Importance: Vérifie que les valeurs nulles restent nulles
        """
        original = None

        data = pickle.dumps(original)
        recovered = pickle.loads(data)

        self.assertIsNone(recovered)


class TestPickleBinaryRoundTrip(unittest.TestCase):
    """
    Tests pour l'aller-retour binaire Pickle (fichier)
    
    Vérifie que:
    - Les données Pickle peuvent être écrites en binaire
    - Les données peuvent être relues sans corruption
    - Le contenu binaire correspond à l'objet original
    """

    def test_pickle_file_binary_round_trip(self):
        """
        Test: Écriture/lecture Pickle en mode binaire fonctionne
        Importance: Vérifie l'utilisation classique de Pickle avec fichiers
        """
        original = {
            'id': 1,
            'type': 'Tree',
            'status': 'unsolved',
            'coordinates': [51.0447, -115.3667]
        }

        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            with open(temp_path, 'wb') as f:
                pickle.dump(original, f, protocol=pickle.HIGHEST_PROTOCOL)

            with open(temp_path, 'rb') as f:
                recovered = pickle.load(f)

            self.assertEqual(original, recovered)
        finally:
            os.unlink(temp_path)

    def test_pickle_bytes_round_trip(self):
        """
        Test: Pickle en bytes (dumps/loads) fait un aller-retour correct
        Importance: Vérifie le round-trip binaire en mémoire
        """
        original = ['a', 1, 2.5, True, None]

        data = pickle.dumps(original, protocol=pickle.HIGHEST_PROTOCOL)
        recovered = pickle.loads(data)

        self.assertEqual(original, recovered)

    def test_pickle_large_object_round_trip(self):
        """
        Test: Objet volumineux peut être sérialisé et rechargé
        Importance: Vérifie que Pickle gère les grosses structures
        """
        original = [{'id': i, 'value': f'item-{i}'} for i in range(1000)]

        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name

        try:
            with open(temp_path, 'wb') as f:
                pickle.dump(original, f, protocol=pickle.HIGHEST_PROTOCOL)

            with open(temp_path, 'rb') as f:
                recovered = pickle.load(f)

            self.assertEqual(original, recovered)
            self.assertEqual(len(recovered), 1000)
        finally:
            os.unlink(temp_path)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
