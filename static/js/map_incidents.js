/**
 * map_incidents.js
 * Coordinateur principal pour la gestion des incidents sur la carte
 * Gère la validation géographique et l'initialisation
 */

var canmoreBoundaryGeoJson = null; // Contient la géométrie de la limite de Canmore

// Chargement de la limite de Canmore (GeoJSON)
window.loadCanmoreBoundary = function(url, callback) {
    fetch(url)
        .then(res => res.json())
        .then(data => {
            canmoreBoundaryGeoJson = data;
            if (callback) callback();
        });
};

// Vérifie si un point est dans la limite de Canmore
function isInsideCanmore(latlng) {
    if (!canmoreBoundaryGeoJson) return false;
    var pt = turf.point([latlng.lng, latlng.lat]);
    // Récupère la géométrie du FeatureCollection
    var polygon = null;
    if (canmoreBoundaryGeoJson.type === 'FeatureCollection' && canmoreBoundaryGeoJson.features.length > 0) {
        polygon = canmoreBoundaryGeoJson.features[0].geometry;
    } else if (canmoreBoundaryGeoJson.type === 'Feature' && canmoreBoundaryGeoJson.geometry) {
        polygon = canmoreBoundaryGeoJson.geometry;
    } else {
        polygon = canmoreBoundaryGeoJson;
    }
    return turf.booleanPointInPolygon(pt, polygon);
}

// Affiche un message d'erreur si clic hors limite
window.showError = function(map, latlng) {
    L.popup()
        .setLatLng(latlng)
        .setContent('<span style="color:red">Vous ne pouvez signaler un incident qu\'à l\'intérieur de Canmore.</span>')
        .openOn(map);
};

// Initialisation après chargement de la carte
window.setupIncidentReporting = function(map) {
    // Affiche tous les incidents existants au chargement de la carte
    window.displayAllIncidents(map);

    // Ajoute les écouteurs sur les filtres incidents
    document.querySelectorAll('.incident-filter').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            window.displayAllIncidents(map);
        });
    });

    // Gestion du clic sur la carte pour signaler un incident ou afficher une erreur
    map.on('click', function(e) {
        if (isInsideCanmore(e.latlng)) {
            window.showIncidentForm(map, e.latlng);
        } else {
            window.showError(map, e.latlng);
        }
    });
};
