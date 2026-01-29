"""
=========================
 Titre : Route Flask - Types d'incidents
 Explication : Fournit une API pour récupérer les types d'incidents et leurs détails à partir d'un fichier CSV pour l'application Canmore Incident Management.
=========================
"""
from flask import Blueprint, jsonify
import csv
import os
import codecs


# =========================
# Définition du Blueprint
# Explication: Création d'un blueprint pour l'API des types d'incidents
incident_types_bp = Blueprint('incident_types', __name__)



# =========================
# Route GET : Récupérer les types d'incidents
# Explication: Lit le fichier CSV, regroupe les sujets et détails, et retourne la liste au format JSON
@incident_types_bp.route('/api/incident_types', methods=['GET'])
def get_incident_types():
	# =========================
	# Chemin du fichier CSV
	# Explication: Définit le chemin vers le fichier CSV contenant les types d'incidents
	csv_path = os.path.join(
		os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
		'static', 'data', 'incident_types.csv'
	)

	subjects = {}  # Dictionnaire pour regrouper les sujets et leurs détails

	# Ouvre le fichier CSV en gérant le BOM éventuel (utf-8-sig)
	with codecs.open(csv_path, encoding='utf-8-sig') as csvfile:
		reader = csv.DictReader(csvfile)
		# Affiche les noms de colonnes pour le débogage
		print("Noms des colonnes CSV :", reader.fieldnames)
		# Normalise les noms de colonnes pour gérer la casse et les espaces
		fieldnames = {name.strip().upper(): name for name in reader.fieldnames}
		subject_key = fieldnames.get('SUBJECT')
		detail_key = fieldnames.get('DETAILS')
		if not subject_key or not detail_key:
			# Erreur si les en-têtes ne sont pas corrects
			return jsonify({'error': 'Le CSV doit contenir les colonnes SUBJECT et DETAILS'}), 400
		for row in reader:
			subject = row[subject_key]
			detail = row[detail_key]
			# Ignore une éventuelle ligne d'en-tête dans les données
			if subject.strip().upper() == 'SUBJECT':
				continue
			# Ajoute le sujet s'il n'existe pas encore
			if subject not in subjects:
				subjects[subject] = []
			# Ajoute le détail s'il n'est pas déjà présent pour ce sujet
			if detail not in subjects[subject]:
				subjects[subject].append(detail)

	# Transforme le dictionnaire en liste de dictionnaires pour le frontend
	result = [
		{'subject': subject, 'details': details}
		for subject, details in subjects.items()
	]
	# Retourne la liste au format JSON
	return jsonify(result)
