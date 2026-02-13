# Canmore Incident Management

[![Tests CI/CD](https://github.com/moyamelissa/Canmore_Incident_Management/actions/workflows/tests.yml/badge.svg)](https://github.com/moyamelissa/Canmore_Incident_Management/actions/workflows/tests.yml)

⚠️ **ATTENTION:** This is a **university project** and is intended for **development and educational purposes only**. This is **NOT** an official incident management system for the Town of Canmore and should **NOT** be used for real-world incident reporting.

🇫🇷 [Lire la documentation en français](#documentation-en-français)

## 📋 Overview

Canmore Incident Management is a web-based incident reporting and tracking application for the City of Canmore. Report incidents directly on an interactive map, track their status in real-time, and manage administrative tasks with an intuitive interface.

## 🚀 Live Demo

- YouTube Demo: https://www.youtube.com/watch?v=YKiiNFLKF_c
- Deployed Web App: [https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/](https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/)

## ✨ Features

- 🗺️ **Interactive Map** - Report and visualize incidents on a live map
- 🛡️ **Dashboard** - Overview of the incident statuses
- 📚 **Information Search** — Quickly look up adresses, parcs, incidents and more!
- 👤 **User Preferences** - Persistent dark mode and personalized settings
- ⚡ **Real-time Notifications** - WebSocket-powered live updates

## 🛠️ Technologies Used

- **Backend:** Python (Flask, Flask-SocketIO)
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

5. **Python version required:**
   - This project requires **Python 3.12 or higher**. If you use an older version, some features (especially real-time updates) may not work.

6. **Secret key (optional, for production):**
   - By default, a development secret key is used for Flask sessions.
   - For better security in production, set the environment variable `FLASK_SECRET_KEY` before running the app:
     ```bash
     set FLASK_SECRET_KEY=your-very-secret-key
     ```
   - If not set, the app will still work for local development and testing.

7. **Run the application:**
   ```bash
   python main.py
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

6. **Python version required:**
   - This project requires **Python 3.12 or higher**. If you use an older version, some features (especially real-time updates) may not work.

7. **Secret key (optional, for production):**
   - By default, a development secret key is used for Flask sessions.
   - For better security in production, set the environment variable `FLASK_SECRET_KEY` before running the app:
     ```bash
     export FLASK_SECRET_KEY=your-very-secret-key
     ```
   - If not set, the app will still work for local development and testing.

8. **Run the application:**
   ```bash
   python main.py
   ```

## 🚀 Launching the Application

The application requires only the Flask server to run:

**Flask Web Server:**
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
- Icons: https://www.flaticon.com
- Music: https://sounddino.com

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for more information.

---

# Documentation en Français

🇺🇸 [Read English documentation](#overview)

⚠️ **ATTENTION:** Ceci est un **projet universitaire** conçu à des fins **éducatives et de développement uniquement**. Ceci n'est **PAS** un système officiel de gestion des incidents pour la Ville de Canmore et ne doit **PAS** être utilisé pour des signalements d'incidents réels.

## 📋 Aperçu

Canmore Incident Management est une application web de signalement et de suivi d'incidents pour la Ville de Canmore. Signalez des incidents directement sur une carte interactive, suivez leur statut en temps réel et gérez les tâches administratives via une interface intuitive.

## 🚀 Démo en ligne

- Démo YouTube : https://www.youtube.com/watch?v=YKiiNFLKF_c
- Application déployée : [https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/](https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/)

## ✨ Fonctionnalités

- 🗺️ **Carte interactive** — Signalez et visualisez les incidents sur une carte en temps réel  
- 🛡️ **Tableau de bord** — Vue d’ensemble des statuts des incidents  
- 📚 **Recherche d'informations** — Recherchez rapidement des adresses, des parcs, des incidents et plus encore !  
- 👤 **Préférences utilisateur** — Mode sombre persistant et paramètres personnalisés  
- ⚡ **Notifications en temps réel** — Mises à jour instantanées grâce à WebSocket 

## 🛠️ Technologies Utilisées

- **Backend:** Python (Flask, Flask-SocketIO)
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

5. **Version de Python requise:**
   - Ce projet nécessite **Python 3.12 ou supérieur**. Si vous utilisez une version plus ancienne, certaines fonctionnalités (notamment les mises à jour en temps réel) peuvent ne pas fonctionner.

6. **Clé secrète (optionnel, pour la production):**
   - Par défaut, une clé secrète de développement est utilisée pour les sessions Flask.
   - Pour une meilleure sécurité en production, définissez la variable d'environnement `FLASK_SECRET_KEY` avant de lancer l'application :
     ```bash
     set FLASK_SECRET_KEY=your-very-secret-key
     ```
   - Si elle n'est pas définie, l'application fonctionnera toujours pour le développement local et les tests.

7. **Lancer l'application:**
   ```bash
   python main.py
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

6. **Version de Python requise:**
   - Ce projet nécessite **Python 3.12 ou supérieur**. Si vous utilisez une version plus ancienne, certaines fonctionnalités (notamment les mises à jour en temps réel) peuvent ne pas fonctionner.

7. **Clé secrète (optionnel, pour la production):**
   - Par défaut, une clé secrète de développement est utilisée pour les sessions Flask.
   - Pour une meilleure sécurité en production, définissez la variable d'environnement `FLASK_SECRET_KEY` avant de lancer l'application :
     ```bash
     export FLASK_SECRET_KEY=your-very-secret-key
     ```
   - Si elle n'est pas définie, l'application fonctionnera toujours pour le développement local et les tests.

8. **Lancer l'application:**
   ```bash
   python main.py
   ```

## 🚀 Lancement de l'Application

L'application nécessite uniquement le serveur Flask pour fonctionner:

**Serveur Flask:**
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
- Icônes : https://www.flaticon.com
- Musique : https://sounddino.com

## 📄 Licence

Ce projet est autorisé sous la Licence MIT. Consultez le fichier LICENSE pour plus d'informations.

---

## 🚀 Live Demo / Démo en ligne

- YouTube Demo: [Link TBD]
- Démo YouTube : [Lien à venir]
- Deployed Web App: [https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/](https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/)
- Application déployée : [https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/](https://canmore-incident-management-fxdcc6esbmc4g0aw.canadacentral-01.azurewebsites.net/)
