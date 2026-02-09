# Canmore Incident Management

[![Tests CI/CD](https://github.com/moyamelissa/Canmore_Incident_Management/actions/workflows/tests.yml/badge.svg)](https://github.com/moyamelissa/Canmore_Incident_Management/actions/workflows/tests.yml)

⚠️ **ATTENTION:** This is a **university project** and is intended for **development and educational purposes only**. This is **NOT** an official incident management system for the Town of Canmore and should **NOT** be used for real-world incident reporting.

🇫🇷 [Lire la documentation en français](#documentation-en-français)

## 📋 Overview

Canmore Incident Management is a web-based incident reporting and tracking application for the City of Canmore. Report incidents directly on an interactive map, track their status in real-time, and manage administrative tasks with an intuitive interface.

## ✨ Features

- 🗺️ **Interactive Map** - Report and visualize incidents on a live map
- 🔍 **Advanced Filtering** - Filter incidents by type and resolution status
- 👤 **User Preferences** - Persistent dark mode and personalized settings
- 🛡️ **Dashboard** - Overview of the incident statuses
- ⚡ **Real-time Notifications** - WebSocket-powered live updates

## 🛠️ Technologies Used

- **Backend:** Python (Flask, Sanic)
- **Frontend:** JavaScript (Leaflet.js, WebSocket)
- **Markup:** HTML5, CSS3
- **Database:** SQLite (incidents), CSV (reference data: addresses, buildings, parks, trails)

## 📦 Installation

### Windows

1. **Install Python 3.x**
   - Download from https://www.python.org/downloads/

2. **Clone the repository:**
   ```bash
   git clone https://github.com/moyamelissa/Canmore_Incident_Management.git
   cd Canmore_Incident_Management
   ```

3. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Linux / macOS

1. **Install Python 3.x**
   - Download from https://www.python.org/downloads/

2. **Install required packages (Ubuntu/Debian):**
   ```bash
   sudo apt install python3-pip python3-venv
   ```

3. **Clone the repository:**
   ```bash
   git clone https://github.com/moyamelissa/Canmore_Incident_Management.git
   cd Canmore_Incident_Management
   ```

4. **Create a virtual environment (recommended):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Launching the Application

The application requires two servers to run simultaneously:

**Terminal 1 - WebSocket Server:**
```bash
python websocket_server.py
```
The WebSocket server will start on `http://localhost:8001`

**Terminal 2 - Flask Web Server:**
```bash
python main.py
```
The application will be available at `http://localhost:5000`

## 🎮 Usage

1. **Report an Incident:**
   - Click on the map to mark an incident location
   - Select the incident type from the dropdown
   - Submit the report

2. **View Incidents:**
   - Browse all reported incidents on the map
   - Filter by type or resolution status
   - Click incidents to see details

3. **Admin Features:**
   - Access admin panel to manage incident statuses
   - Mark incidents as resolved
   - Delete incidents as needed

4. **User Settings:**
   - Toggle dark mode for comfortable nighttime use
   - Settings persist across sessions


## 👩‍💻 Credits

**Development:**
- Code, design, and architecture: Melissa Moya
- Programming assistance: GitHub Copilot

**Inspirations:**
- City of Canmore community feedback
- Modern incident tracking systems

**Data & Resources:**
- Map tiles: Leaflet.js
- Geographic data: OpenStreetMap
- **Official Canmore data:** https://opendata-canmore.opendata.arcgis.com/

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more information.

---

# Documentation en Français

🇺🇸 [Read English documentation](#overview)

⚠️ **ATTENTION:** Ceci est un **projet universitaire** conçu à des fins **éducatives et de développement uniquement**. Ceci n'est **PAS** un système officiel de gestion des incidents pour la Ville de Canmore et ne doit **PAS** être utilisé pour des signalements d'incidents réels.

## 📋 Aperçu

Canmore Incident Management est une application web de signalement et de suivi d'incidents pour la Ville de Canmore. Signalez des incidents directement sur une carte interactive, suivez leur statut en temps réel et gérez les tâches administratives via une interface intuitive.

## ✨ Fonctionnalités

- 🗺️ **Carte Interactive** - Signalez et visualisez les incidents sur une carte en direct
- 🔍 **Filtrage Avancé** - Filtrez les incidents par type et statut de résolution
- 👤 **Préférences Utilisateur** - Mode sombre persistant et paramètres personnalisés
- ⚡ **Notifications en Temps Réel** - Mises à jour en direct via WebSocket
- 🛡️ **Tableau de Bord Admin** - Gérez les statuts et permissions des incidents
- 📱 **Design Responsive** - Fonctionne parfaitement sur ordinateur et mobile

## 🛠️ Technologies Utilisées

- **Backend:** Python (Flask, Sanic)
- **Frontend:** JavaScript (Leaflet.js, WebSocket)
- **Markup:** HTML5, CSS3
- **Base de Données:** SQLite (incidents), CSV (données de référence: adresses, bâtiments, parcs, sentiers)

## 📦 Installation

### Windows

1. **Installer Python 3.x**
   - Téléchargez depuis https://www.python.org/downloads/

2. **Cloner le dépôt:**
   ```bash
   git clone https://github.com/moyamelissa/Canmore_Incident_Management.git
   cd Canmore_Incident_Management
   ```

3. **Créer un environnement virtuel (recommandé):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

4. **Installer les dépendances:**
   ```bash
   pip install -r requirements.txt
   ```

### Linux / macOS

1. **Installer Python 3.x**
   - Téléchargez depuis https://www.python.org/downloads/

2. **Installer les paquets requis (Ubuntu/Debian):**
   ```bash
   sudo apt install python3-pip python3-venv
   ```

3. **Cloner le dépôt:**
   ```bash
   git clone https://github.com/moyamelissa/Canmore_Incident_Management.git
   cd Canmore_Incident_Management
   ```

4. **Créer un environnement virtuel (recommandé):**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

5. **Installer les dépendances:**
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Lancement de l'Application

L'application nécessite deux serveurs fonctionnant simultanément:

**Terminal 1 - Serveur WebSocket:**
```bash
python websocket_server.py
```
Le serveur WebSocket démarrera sur `http://localhost:8001`

**Terminal 2 - Serveur Flask:**
```bash
python main.py
```
L'application sera accessible sur `http://localhost:5000`

## 🎮 Utilisation

1. **Signaler un Incident:**
   - Cliquez sur la carte pour marquer un emplacement
   - Sélectionnez le type d'incident dans le menu déroulant
   - Validez le signalement

2. **Voir les Incidents:**
   - Consultez tous les incidents signalés sur la carte
   - Filtrez par type ou statut de résolution
   - Cliquez sur un incident pour voir les détails

3. **Fonctionnalités Admin:**
   - Accédez au panneau administrateur pour gérer les statuts
   - Marquez les incidents comme résolus
   - Supprimez les incidents si nécessaire

4. **Paramètres Utilisateur:**
   - Activez le mode sombre pour une utilisation nocturne confortable
   - Les paramètres sont sauvegardés entre les sessions

## 🧪 Tests et Gestion des Erreurs

### Exécuter les Tests

Lancez la suite de tests:
```bash
python -m pytest test_incidents.py -v
```

Ou avec couverture de code:
```bash
python -m pytest test_incidents.py --cov=server --cov-report=term
```

### Implémentation de la Gestion des Erreurs

Le projet implémente une gestion complète des erreurs par exceptions:

#### 1. **Erreurs de Base de Données** (`incidents_api.py`)
```python
try:
    conn = get_db_connection()
    conn.execute('INSERT INTO incidents ...')
except Exception as e:
    logger.error(f"Erreur BD: {e}")
    return jsonify({'error': 'Erreur base de données'}), 500
```

#### 2. **Erreurs d'Entrées/Sorties** (`incident_types.py`)
```python
try:
    with codecs.open(csv_path, encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
except FileNotFoundError:
    return jsonify({'error': 'Fichier CSV non trouvé'}), 404
except Exception as e:
    return jsonify({'error': f'Erreur lecture CSV: {str(e)}'}), 500
```

#### 3. **Erreurs Requêtes HTTP** (`websocket_server.py`)
```python
try:
    await client.send(msg)
except Exception as e:
    logger.error(f"Erreur broadcast: {e}")
```

#### 4. **Erreurs de Validation** (`incidents_api.py`)
```python
required_fields = ['type', 'description', 'latitude', 'longitude', 'timestamp']
if not all(field in data for field in required_fields):
    return jsonify({'error': 'Champs manquants'}), 400
```

#### 5. **Gestion des Erreurs Frontend** (`map_incidents.js`)
```javascript
.catch(err => {
    alert('Erreur: ' + err.message);
    logger.error(err);
});
```

### Couverture des Tests

- ✅ **Tests des API** - Opérations POST, GET, PATCH, DELETE
- ✅ **Tests de Validation** - Champs requis, types de données, contraintes
- ✅ **Tests de Gestion d'Erreurs** - Gestion des exceptions et récupération
- ✅ **Tests d'Intégration** - Persistance en BD et mises à jour WebSocket
- ✅ **Tests des Routes** - Pages statiques et rendu des templates

## 📁 Structure du Projet

```
Canmore_Incident_Management/
├── main.py                      # Application Flask principale
├── websocket_server.py          # Serveur WebSocket pour mises à jour
├── requirements.txt             # Dépendances Python
├── README.md                    # Ce fichier
│
├── config/
│   ├── user_settings.py        # Gestion des préférences utilisateur
│   └── __pycache__/
│
├── server/
│   ├── routes/                 # Blueprints Flask (routes)
│   │   ├── home_route.py       # Page d'accueil
│   │   ├── map_route.py        # Page carte
│   │   ├── report_route.py     # Page signalement
│   │   ├── info_route.py       # Page informations
│   │   ├── incident_types.py   # API types d'incidents
│   │   ├── incidents_api.py    # API incidents
│   │   └── user_settings_api.py# API paramètres utilisateur
│   └── data/                   # Fichiers de données
│
├── static/                      # Ressources statiques
│   ├── css/                    # Feuilles de style
│   ├── js/                     # Scripts côté client
│   ├── data/                   # Données GeoJSON et CSV
│   ├── img/                    # Images
│   ├── icons/                  # Icônes UI
│   └── audio/                  # Effets sonores
│
└── templates/                   # Templates HTML (Jinja2)
    ├── home.html
    ├── map.html
    ├── report.html
    └── info.html
```

## 👩‍💻 Crédits

**Développement:**
- Code, design et architecture : Melissa Moya
- Assistance programmation : GitHub Copilot

**Inspirations:**
- Retours de la communauté de Canmore
- Systèmes modernes de suivi d'incidents

**Données et Ressources:**
- Tuiles de carte : Leaflet.js
- Données géographiques : OpenStreetMap
- **Données officielles de Canmore:** https://opendata-canmore.opendata.arcgis.com/

## 📄 Licence

Ce projet est autorisé sous la Licence MIT. Consultez le fichier LICENSE pour plus d'informations.
