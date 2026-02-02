"""
test_templates.py
Tests pour le rendu des templates Flask HTML

Importance: Les tests de templates vérifient que les pages se chargent correctement,
retournent du HTML valide, et que le contenu attendu est présent.
C'est essentiel pour l'expérience utilisateur de l'application web.
"""

import unittest
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


class TestTemplateRoutes(unittest.TestCase):
    """
    Tests du rendu des templates Flask
    
    Vérifie que:
    - Toutes les routes principales se chargent (HTTP 200)
    - Les réponses contiennent du HTML valide
    - Le doctype HTML5 est présent
    - Les pages ne retournent pas d'erreurs serveur
    """

    def setUp(self):
        """
        Configuration avant chaque test
        - Active le mode test de Flask
        - Initialise le client de test
        """
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    # ===== TESTS DE LA PAGE D'ACCUEIL (/) =====

    def test_home_page_returns_200(self):
        """
        Test: GET / retourne le code 200 (succès)
        Importance: Vérifie que la page d'accueil est accessible
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_returns_html(self):
        """
        Test: GET / retourne du contenu HTML
        Importance: Vérifie que la réponse contient du HTML, pas du JSON ou une erreur
        """
        response = self.client.get('/')
        
        # Vérifie que c'est du HTML
        content_type = response.content_type
        self.assertIn('text/html', content_type)

    def test_home_page_contains_doctype(self):
        """
        Test: La page d'accueil contient le doctype HTML5
        Importance: Vérifie que le HTML est valide et bien formé (<!DOCTYPE html>)
        """
        response = self.client.get('/')
        
        # Décode la réponse et convertit en minuscules pour test case-insensitive
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<!doctype', html_lower)

    def test_home_page_contains_html_tag(self):
        """
        Test: La page d'accueil contient une balise <html>
        Importance: Vérifie la structure de base du HTML
        """
        response = self.client.get('/')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<html', html_lower)

    def test_home_page_contains_body_tag(self):
        """
        Test: La page d'accueil contient une balise <body>
        Importance: Vérifie que le HTML a du contenu à afficher
        """
        response = self.client.get('/')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<body', html_lower)

    def test_home_page_has_content(self):
        """
        Test: La page d'accueil contient du contenu (pas vide)
        Importance: Vérifie que la template ne retourne pas une page vide
        """
        response = self.client.get('/')
        
        self.assertGreater(len(response.data), 100)  # Au moins 100 bytes de contenu

    # ===== TESTS DE LA PAGE CARTE (/map) =====

    def test_map_page_returns_200(self):
        """
        Test: GET /map retourne le code 200
        Importance: Vérifie que la page carte est accessible
        """
        response = self.client.get('/map')
        self.assertEqual(response.status_code, 200)

    def test_map_page_returns_html(self):
        """
        Test: GET /map retourne du contenu HTML
        Importance: Vérifie que la carte se rend en HTML
        """
        response = self.client.get('/map')
        self.assertIn('text/html', response.content_type)

    def test_map_page_contains_doctype(self):
        """
        Test: La page carte contient le doctype HTML5
        Importance: Vérifie que la page carte est du HTML valide
        """
        response = self.client.get('/map')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<!doctype', html_lower)

    def test_map_page_has_content(self):
        """
        Test: La page carte contient du contenu
        Importance: Vérifie que la page n'est pas vide
        """
        response = self.client.get('/map')
        self.assertGreater(len(response.data), 100)

    # ===== TESTS DE LA PAGE RAPPORT (/report) =====

    def test_report_page_returns_200(self):
        """
        Test: GET /report retourne le code 200
        Importance: Vérifie que la page rapport est accessible
        """
        response = self.client.get('/report')
        self.assertEqual(response.status_code, 200)

    def test_report_page_returns_html(self):
        """
        Test: GET /report retourne du contenu HTML
        Importance: Vérifie que le rapport se rend en HTML
        """
        response = self.client.get('/report')
        self.assertIn('text/html', response.content_type)

    def test_report_page_contains_doctype(self):
        """
        Test: La page rapport contient le doctype HTML5
        Importance: Vérifie que la page rapport est du HTML valide
        """
        response = self.client.get('/report')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<!doctype', html_lower)

    def test_report_page_has_content(self):
        """
        Test: La page rapport contient du contenu
        Importance: Vérifie que la page n'est pas vide
        """
        response = self.client.get('/report')
        self.assertGreater(len(response.data), 100)

    # ===== TESTS DE LA PAGE INFO (/info) =====

    def test_info_page_returns_200(self):
        """
        Test: GET /info retourne le code 200
        Importance: Vérifie que la page info est accessible
        """
        response = self.client.get('/info')
        self.assertEqual(response.status_code, 200)

    def test_info_page_returns_html(self):
        """
        Test: GET /info retourne du contenu HTML
        Importance: Vérifie que la page info se rend en HTML
        """
        response = self.client.get('/info')
        self.assertIn('text/html', response.content_type)

    def test_info_page_contains_doctype(self):
        """
        Test: La page info contient le doctype HTML5
        Importance: Vérifie que la page info est du HTML valide
        """
        response = self.client.get('/info')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<!doctype', html_lower)

    def test_info_page_has_content(self):
        """
        Test: La page info contient du contenu
        Importance: Vérifie que la page n'est pas vide
        """
        response = self.client.get('/info')
        self.assertGreater(len(response.data), 100)

    # ===== TESTS DE ROBUSTESSE =====

    def test_all_main_routes_accessible(self):
        """
        Test: Toutes les routes principales sont accessibles
        Importance: Vérifie qu'aucune route ne retourne 500 (erreur serveur)
        """
        routes = ['/', '/map', '/report', '/info']
        
        for route in routes:
            response = self.client.get(route)
            
            # Doit être 200 ou un code de redirection (3xx), pas une erreur serveur (5xx)
            self.assertLess(response.status_code, 500, 
                           f"Route {route} returned server error: {response.status_code}")

    def test_all_main_routes_return_html(self):
        """
        Test: Toutes les routes principales retournent du HTML
        Importance: Vérifie la cohérence du format de réponse pour toutes les pages
        """
        routes = ['/', '/map', '/report', '/info']
        
        for route in routes:
            response = self.client.get(route)
            self.assertIn('text/html', response.content_type, 
                         f"Route {route} did not return HTML")

    # ===== TESTS DE CONTENU VARIABLE (OPTIONNEL) =====

    def test_home_page_contains_head_section(self):
        """
        Test: La page d'accueil contient une section <head>
        Importance: Vérifie que la template inclut les métadonnées HTML (CSS, JS, etc.)
        """
        response = self.client.get('/')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<head', html_lower)

    def test_home_page_contains_title(self):
        """
        Test: La page d'accueil contient une balise <title>
        Importance: Vérifie que le titre de la page est défini (important pour le SEO et UX)
        """
        response = self.client.get('/')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<title', html_lower)

    def test_map_page_contains_script_tags(self):
        """
        Test: La page carte contient des balises <script>
        Importance: Vérifie que la page inclut JavaScript (probablement pour la carte)
        """
        response = self.client.get('/map')
        html_lower = response.data.decode('utf-8', errors='ignore').lower()
        
        self.assertIn('<script', html_lower)

    # ===== TESTS D'ERREURS =====

    def test_nonexistent_route_returns_404(self):
        """
        Test: Une route inexistante retourne 404
        Importance: Vérifie que l'application gère correctement les routes invalides
        """
        response = self.client.get('/nonexistent')
        self.assertEqual(response.status_code, 404)

    def test_404_page_is_html(self):
        """
        Test: La page 404 retourne du HTML
        Importance: Vérifie que même les erreurs sont formatées en HTML
        """
        response = self.client.get('/nonexistent')
        
        # Doit contenir du HTML, même pour une erreur
        content_type = response.content_type
        self.assertIn('text/html', content_type)


# ========== EXÉCUTION DES TESTS ==========

if __name__ == '__main__':
    unittest.main(verbosity=2)
