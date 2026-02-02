"""
test_algorithms.py
Tests pour les algorithmes - Recherche binaire (binary search)

Importance: Les tests d'algorithmes vérifient que la recherche binaire fonctionne
correctement sur des tableaux triés, avec des cas normaux et des cas limites.
"""

import unittest
import sys
import os

# Ajoute le répertoire parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from main import app  # noqa: F401
except Exception:
    # L'app n'est pas nécessaire pour ces tests, donc on ignore l'échec d'import.
    app = None


def binary_search(arr, target):
    """
    Recherche binaire sur un tableau trié.
    
    Retourne l'index de la valeur si trouvée, sinon -1.
    """
    left = 0
    right = len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        if arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


class TestBinarySearchAlgorithm(unittest.TestCase):
    """
    Tests pour la recherche binaire
    
    Vérifie que:
    - La valeur est trouvée dans un tableau trié
    - La valeur non trouvée retourne -1
    - Les cas limites (premier/dernier élément) fonctionnent
    - Les grands tableaux sont gérés correctement
    """

    def test_finds_value_in_sorted_array(self):
        """
        Test: La recherche binaire trouve une valeur dans un tableau trié
        Importance: Vérifie le cas normal d'utilisation
        """
        arr = [1, 3, 5, 7, 9, 11, 13]
        index = binary_search(arr, 7)
        self.assertEqual(index, 3)

    def test_returns_minus_one_if_not_found(self):
        """
        Test: Retourne -1 si la valeur n'existe pas
        Importance: Vérifie le comportement en cas d'absence
        """
        arr = [2, 4, 6, 8, 10]
        index = binary_search(arr, 7)
        self.assertEqual(index, -1)

    def test_find_first_element(self):
        """
        Test: Trouve le premier élément du tableau
        Importance: Vérifie un cas limite (bord gauche)
        """
        arr = [10, 20, 30, 40, 50]
        index = binary_search(arr, 10)
        self.assertEqual(index, 0)

    def test_find_last_element(self):
        """
        Test: Trouve le dernier élément du tableau
        Importance: Vérifie un cas limite (bord droit)
        """
        arr = [10, 20, 30, 40, 50]
        index = binary_search(arr, 50)
        self.assertEqual(index, 4)

    def test_large_array(self):
        """
        Test: Fonctionne sur un grand tableau
        Importance: Vérifie la performance et la robustesse sur de grandes tailles
        """
        arr = list(range(0, 100000, 2))  # 0, 2, 4, ..., 99998
        target = 88888
        index = binary_search(arr, target)
        
        # L'index attendu est target / 2
        self.assertEqual(index, target // 2)

    def test_large_array_not_found(self):
        """
        Test: Grand tableau, valeur absente retourne -1
        Importance: Vérifie le comportement en absence sur grands volumes
        """
        arr = list(range(0, 100000, 2))
        index = binary_search(arr, 88889)  # Impair, donc absent
        self.assertEqual(index, -1)

    def test_single_element_found(self):
        """
        Test: Tableau avec un seul élément (trouvé)
        Importance: Vérifie un cas limite minimal
        """
        arr = [42]
        index = binary_search(arr, 42)
        self.assertEqual(index, 0)

    def test_single_element_not_found(self):
        """
        Test: Tableau avec un seul élément (non trouvé)
        Importance: Vérifie un cas limite minimal
        """
        arr = [42]
        index = binary_search(arr, 7)
        self.assertEqual(index, -1)

    def test_empty_array_returns_minus_one(self):
        """
        Test: Tableau vide retourne -1
        Importance: Vérifie le comportement en cas de tableau vide
        """
        arr = []
        index = binary_search(arr, 1)
        self.assertEqual(index, -1)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
