"""
test_binary.py
Tests pour les fichiers binaires - Écriture/lecture en mode binaire, vérification de taille

Importance: Les tests binaires vérifient que les données binaires peuvent être écrites
et relues correctement en utilisant les modes 'wb' (write binary) et 'rb' (read binary).
C'est essentiel pour la sérialisation de données complexes et la persistence.
"""

import unittest
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


class TestBinaryFileWriteRead(unittest.TestCase):
    """
    Tests pour l'écriture et la lecture de fichiers binaires
    
    Vérifie que:
    - Les bytes peuvent être écrits en mode 'wb'
    - Les bytes peuvent être lus en mode 'rb'
    - Les données écrites correspondent aux données lues
    """

    def test_write_simple_bytes_to_binary_file(self):
        """
        Test: Écrire des bytes simples dans un fichier binaire
        Importance: Vérifie que les données binaires peuvent être écrites correctement
        """
        test_data = b'Hello, World!'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Écrit les bytes en mode binaire
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            # Vérifie que le fichier a été créé
            self.assertTrue(os.path.exists(temp_path))
        finally:
            os.unlink(temp_path)

    def test_read_bytes_from_binary_file(self):
        """
        Test: Lire des bytes à partir d'un fichier binaire
        Importance: Vérifie que les données binaires peuvent être lues correctement
        """
        test_data = b'Test binary data'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Écrit les données
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            # Lit les données
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            # Les données doivent être identiques
            self.assertEqual(test_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_write_and_read_empty_binary_file(self):
        """
        Test: Écrire et lire un fichier binaire vide
        Importance: Vérifie la gestion des cas limites (fichier vide)
        """
        test_data = b''
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            self.assertEqual(test_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_write_and_read_large_binary_data(self):
        """
        Test: Écrire et lire un fichier binaire volumineux
        Importance: Vérifie que les données volumineuses sont gérées correctement
        """
        # Crée 1 MB de données aléatoires
        test_data = os.urandom(1024 * 1024)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            self.assertEqual(test_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_write_and_read_binary_with_null_bytes(self):
        """
        Test: Écrire et lire des données binaires contenant des bytes null
        Importance: Vérifie que les données binaires "réelles" avec null bytes sont gérées
        """
        test_data = b'\x00\x01\x02\x03\x04\x05\x00\x00'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            self.assertEqual(test_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_write_bytes_in_chunks(self):
        """
        Test: Écrire des bytes par chunks, puis lire tout
        Importance: Vérifie que l'écriture en plusieurs appels fonctionne correctement
        """
        chunk1 = b'First chunk, '
        chunk2 = b'Second chunk, '
        chunk3 = b'Third chunk'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Écrit par chunks
            with open(temp_path, 'wb') as f:
                f.write(chunk1)
                f.write(chunk2)
                f.write(chunk3)
            
            # Lit tout
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            # Doit être la concaténation de tous les chunks
            expected = chunk1 + chunk2 + chunk3
            self.assertEqual(expected, read_data)
        finally:
            os.unlink(temp_path)

    def test_read_bytes_in_chunks(self):
        """
        Test: Écrire des données, puis les lire par chunks
        Importance: Vérifie que la lecture par chunks fonctionne correctement
        """
        test_data = b'A' * 1000
        chunk_size = 100
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            # Lit par chunks
            chunks = []
            with open(temp_path, 'rb') as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    chunks.append(chunk)
            
            # Reconstruit
            read_data = b''.join(chunks)
            self.assertEqual(test_data, read_data)
        finally:
            os.unlink(temp_path)


class TestBinaryFileSizeVerification(unittest.TestCase):
    """
    Tests pour la vérification de la taille des fichiers binaires
    
    Vérifie que:
    - La taille du fichier correspond à celle attendue
    - La taille peut être vérifiée avant la lecture
    - Les fichiers de différentes tailles sont correctement distingués
    """

    def test_file_size_matches_data_written(self):
        """
        Test: La taille du fichier correspond aux données écrites
        Importance: Vérifie que le fichier contient exactement les données écrites
        """
        test_data = b'Test data with specific size'
        expected_size = len(test_data)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            # Vérifie la taille du fichier
            actual_size = os.path.getsize(temp_path)
            self.assertEqual(expected_size, actual_size)
        finally:
            os.unlink(temp_path)

    def test_file_size_before_reading_entire_file(self):
        """
        Test: Vérifier la taille du fichier avant de lire tout son contenu
        Importance: Permet d'optimiser la lecture (pré-allocation de mémoire)
        """
        test_data = b'X' * 1000
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            # Vérifie la taille
            file_size = os.path.getsize(temp_path)
            
            # Lit le fichier
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            # La taille du fichier doit correspondre à la taille des données
            self.assertEqual(file_size, len(test_data))
            self.assertEqual(file_size, len(read_data))
        finally:
            os.unlink(temp_path)

    def test_multiple_files_have_different_sizes(self):
        """
        Test: Plusieurs fichiers de différentes tailles sont correctement différenciés
        Importance: Vérifie que la taille est une signature fiable de différence
        """
        data_100 = b'A' * 100
        data_500 = b'B' * 500
        data_1000 = b'C' * 1000
        
        try:
            # Crée 3 fichiers
            with tempfile.NamedTemporaryFile(delete=False, suffix='_100') as f:
                path1 = f.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='_500') as f:
                path2 = f.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='_1000') as f:
                path3 = f.name
            
            with open(path1, 'wb') as f:
                f.write(data_100)
            with open(path2, 'wb') as f:
                f.write(data_500)
            with open(path3, 'wb') as f:
                f.write(data_1000)
            
            # Vérifie les tailles
            size1 = os.path.getsize(path1)
            size2 = os.path.getsize(path2)
            size3 = os.path.getsize(path3)
            
            self.assertEqual(size1, 100)
            self.assertEqual(size2, 500)
            self.assertEqual(size3, 1000)
            self.assertLess(size1, size2)
            self.assertLess(size2, size3)
        finally:
            for path in [path1, path2, path3]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_empty_file_has_zero_size(self):
        """
        Test: Un fichier vide a une taille de 0 bytes
        Importance: Vérifie la gestion des fichiers vides
        """
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Crée un fichier vide
            with open(temp_path, 'wb') as f:
                pass  # Ne rien écrire
            
            file_size = os.path.getsize(temp_path)
            self.assertEqual(file_size, 0)
        finally:
            os.unlink(temp_path)

    def test_file_size_with_utf8_encoded_text(self):
        """
        Test: La taille d'un fichier avec du texte UTF-8 encodé correspond à len(encoded)
        Importance: Vérifie que l'encodage UTF-8 affecte correctement la taille
        """
        text = "Nid de poule à côté du café"
        encoded_data = text.encode('utf-8')
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(encoded_data)
            
            file_size = os.path.getsize(temp_path)
            # UTF-8 avec accents crée plus de bytes que len(text)
            self.assertEqual(file_size, len(encoded_data))
            # Vérifie que la taille est supérieure à len(text) due aux accents
            self.assertGreater(len(encoded_data), len(text))
        finally:
            os.unlink(temp_path)


class TestBinaryDataIntegrity(unittest.TestCase):
    """
    Tests pour l'intégrité des données binaires
    
    Vérifie que:
    - Les données écrites sont identiques aux données lues (byte par byte)
    - Les modifications de données sont détectées
    - Les données binaires ne sont pas altérées
    """

    def test_all_bytes_match_after_round_trip(self):
        """
        Test: Tous les bytes correspondent exactement après aller-retour
        Importance: Vérifie qu'aucun byte n'est altéré ou perdu
        """
        test_data = bytes(range(256))  # Tous les bytes possibles (0-255)
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            # Chaque byte doit correspondre
            self.assertEqual(len(test_data), len(read_data))
            for i, (original, read) in enumerate(zip(test_data, read_data)):
                self.assertEqual(original, read, f"Byte {i} doesn't match")
        finally:
            os.unlink(temp_path)

    def test_binary_data_not_text_converted(self):
        """
        Test: Les données binaires ne sont pas converties en texte
        Importance: Vérifie que 'rb'/'wb' ne font pas de conversions de ligne de fin
        """
        # Données avec \r\n (line endings Windows)
        test_data = b'Line1\r\nLine2\r\nLine3\r\n'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            # Les \r\n doivent être préservés tels quels
            self.assertEqual(test_data, read_data)
            self.assertEqual(read_data.count(b'\r\n'), 3)
        finally:
            os.unlink(temp_path)

    def test_binary_data_with_special_bytes(self):
        """
        Test: Les bytes spéciaux (00, FF) ne sont pas altérés
        Importance: Vérifie que tous les bytes 0x00-0xFF sont gérés correctement
        """
        test_data = b'\x00\xFF\x00\xFF\x00\xFF'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            self.assertEqual(test_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_modified_file_detected(self):
        """
        Test: Une modification du fichier est détectée
        Importance: Vérifie que les modifications ne passent pas inaperçues
        """
        test_data = b'Original data'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Écrit les données originales
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            # Modifie le fichier
            modified_data = b'Modified data'
            with open(temp_path, 'wb') as f:
                f.write(modified_data)
            
            # Vérifie que les données lues sont différentes
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            self.assertNotEqual(test_data, read_data)
            self.assertEqual(modified_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_byte_order_preserved(self):
        """
        Test: L'ordre des bytes est préservé exactement
        Importance: Vérifie que la sérialisation respecte l'ordre des données
        """
        test_data = b'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            self.assertEqual(test_data, read_data)
            # Vérifie byte par byte
            for i in range(len(test_data)):
                self.assertEqual(test_data[i], read_data[i])
        finally:
            os.unlink(temp_path)


class TestBinaryModeEdgeCases(unittest.TestCase):
    """
    Tests pour les cas limites du mode binaire
    
    Vérifie que:
    - Les fichiers binaires multiples ne s'interfèrent pas
    - La position du curseur fonctionne correctement
    - Les fichiers peuvent être réouverts avec différents modes
    """

    def test_multiple_binary_files_independent(self):
        """
        Test: Plusieurs fichiers binaires sont indépendants (pas d'interférence)
        Importance: Vérifie que l'écriture simultanée dans plusieurs fichiers fonctionne
        """
        data1 = b'Data in file 1'
        data2 = b'Data in file 2'
        
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='_1') as f:
                path1 = f.name
            with tempfile.NamedTemporaryFile(delete=False, suffix='_2') as f:
                path2 = f.name
            
            # Écrit dans les deux fichiers
            with open(path1, 'wb') as f:
                f.write(data1)
            with open(path2, 'wb') as f:
                f.write(data2)
            
            # Lit les deux fichiers
            with open(path1, 'rb') as f:
                read1 = f.read()
            with open(path2, 'rb') as f:
                read2 = f.read()
            
            # Les données doivent être indépendantes
            self.assertEqual(data1, read1)
            self.assertEqual(data2, read2)
            self.assertNotEqual(read1, read2)
        finally:
            for path in [path1, path2]:
                if os.path.exists(path):
                    os.unlink(path)

    def test_file_cursor_position_after_write(self):
        """
        Test: Après l'écriture, la lecture doit commencer au début du fichier
        Importance: Vérifie que la réouverture en mode 'rb' remet le curseur à zéro
        """
        test_data = b'Test cursor position'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Écrit les données
            with open(temp_path, 'wb') as f:
                f.write(test_data)
            
            # Réouvre en mode lecture (doit commencer au début)
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            # Doit lire tout à partir du début
            self.assertEqual(test_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_reopen_file_appends_or_replaces(self):
        """
        Test: Réouvrir avec 'wb' remplace le contenu, pas d'ajout
        Importance: Vérifie que 'wb' n'ajoute pas mais remplace
        """
        original_data = b'Original data'
        new_data = b'New'
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Écrit les données originales
            with open(temp_path, 'wb') as f:
                f.write(original_data)
            
            # Réouvre avec 'wb' et écrit moins de data
            with open(temp_path, 'wb') as f:
                f.write(new_data)
            
            # Lit
            with open(temp_path, 'rb') as f:
                read_data = f.read()
            
            # Doit contenir seulement les nouvelles données (pas le reste des anciennes)
            self.assertEqual(new_data, read_data)
            self.assertNotEqual(original_data, read_data)
        finally:
            os.unlink(temp_path)

    def test_binary_file_utf8_encoding(self):
        """
        Test: Encoder du texte UTF-8 en bytes, puis lire et décoder
        Importance: Vérifie l'interopérabilité entre texte et binaire
        """
        original_text = "Éclairage défaillant"
        encoded_bytes = original_text.encode('utf-8')
        
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_path = f.name
        
        try:
            # Écrit en mode binaire
            with open(temp_path, 'wb') as f:
                f.write(encoded_bytes)
            
            # Lit en mode binaire
            with open(temp_path, 'rb') as f:
                read_bytes = f.read()
            
            # Décode et compare
            decoded_text = read_bytes.decode('utf-8')
            self.assertEqual(original_text, decoded_text)
        finally:
            os.unlink(temp_path)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
