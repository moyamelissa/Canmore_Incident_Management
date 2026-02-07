/**
 * map_incidents_display.js
 * Affichage et gestion (CRUD) des incidents sur la carte
 */

// Stockage des marqueurs d'incidents
var incidentMarkers = [];

// Affiche tous les incidents sur la carte avec filtrage
window.displayAllIncidents = function(map) {
    // Supprime les anciens marqueurs
    incidentMarkers.forEach(function(m) { map.removeLayer(m); });
    incidentMarkers = [];
    fetch('/api/incidents')
        .then(res => res.json())
        .then(incidents => {
            // Lit les filtres cochés (résolu/non résolu)
            var showUnsolved = document.querySelector('.incident-filter[data-status="unsolved"]').checked;
            var showSolved = document.querySelector('.incident-filter[data-status="solved"]').checked;
            incidents.forEach(incident => {
                var isSolved = (incident.status === 'solved' || incident.status === 'résolu');
                if ((isSolved && !showSolved) || (!isSolved && !showUnsolved)) {
                    return; // Ne pas afficher ce marqueur
                }
                var iconUrl = isSolved
                    ? 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png'
                    : 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png';
                var markerIcon = L.icon({
                    iconUrl: iconUrl,
                    shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                    iconSize: [25, 41],
                    iconAnchor: [12, 41],
                    popupAnchor: [1, -34],
                    shadowSize: [41, 41]
                });
                var marker = L.marker([incident.latitude, incident.longitude], {icon: markerIcon}).addTo(map);
                incidentMarkers.push(marker);

                // Formate le timestamp pour un affichage convivial
                var formattedTime = '';
                if (incident.timestamp) {
                    var date = new Date(incident.timestamp);
                    var options = { year: 'numeric', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit' };
                    formattedTime = date.toLocaleDateString('fr-FR', options);
                }

                // Construit le HTML du popup pour chaque incident
                var popupHtml = '<b>Incident signalé</b><br>' +
                    'Sujet : ' + (incident.type || '') + '<br>' +
                    'Détail : ' + (incident.description || '') + '<br>' +
                    'Horodatage : ' + (formattedTime || incident.timestamp || '') + '<br>';

                // Si admin, ajoute le menu déroulant de statut et le bouton de mise à jour
                if (window.isAdmin) {
                    popupHtml +=
                        '<div style="margin-top:8px">' +
                        '<label for="status-select-' + incident.id + '">Statut :</label> ' +
                        '<select id="status-select-' + incident.id + '" style="margin-left:4px;padding:4px 8px;border-radius:4px;border:1px solid #ccc !important;background:#fff !important;color:#333 !important;">' +
                        '<option value="unsolved"' + (!isSolved ? ' selected' : '') + '>Non résolu</option>' +
                        '<option value="solved"' + (isSolved ? ' selected' : '') + '>Résolu</option>' +
                        '</select><br><br>' +
                        '<button id="update-status-btn-' + incident.id + '" class="admin-status-btn" style="background:#6c757d !important;color:white !important;border:none !important;padding:6px 12px;border-radius:4px;cursor:pointer;font-weight:500;">Mettre à jour le statut</button> ' +
                        '<button id="delete-incident-btn-' + incident.id + '" class="admin-delete-btn" style="background:#d32f2f !important;color:white !important;border:none !important;padding:6px 12px;border-radius:4px;cursor:pointer;font-weight:500;">Supprimer</button>' +
                        '</div>';
                }

                marker.bindPopup(popupHtml);

                // Ajoute un écouteur d'événement pour la mise à jour du statut si admin
                if (window.isAdmin) {
                    marker.on('popupopen', function() {
                        var btn = document.getElementById('update-status-btn-' + incident.id);
                        var select = document.getElementById('status-select-' + incident.id);
                        var delBtn = document.getElementById('delete-incident-btn-' + incident.id);
                        if (btn && select) {
                            btn.onclick = function() {
                                var newStatus = select.value;
                                // Envoie la mise à jour du statut au backend
                                fetch('/api/incidents/' + incident.id, {
                                    method: 'PATCH',
                                    headers: { 'Content-Type': 'application/json' },
                                    body: JSON.stringify({ status: newStatus })
                                })
                                .then(res => {
                                    if (!res.ok) throw new Error('Erreur lors de la mise à jour du statut');
                                    return res.json();
                                })
                                .then(data => {
                                    var newIconUrl = newStatus === 'solved'
                                        ? 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-grey.png'
                                        : 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png';
                                    marker.setIcon(L.icon({
                                        iconUrl: newIconUrl,
                                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                                        iconSize: [25, 41],
                                        iconAnchor: [12, 41],
                                        popupAnchor: [1, -34],
                                        shadowSize: [41, 41]
                                    }));
                                    marker.closePopup(); // Ferme le popup après la mise à jour
                                })
                                .catch(err => {
                                    alert('Erreur lors de la mise à jour du statut: ' + err.message);
                                });
                            };
                        }
                        if (delBtn) {
                            delBtn.onclick = function() {
                                if (confirm('Êtes-vous sûr de vouloir supprimer cet incident ?')) {
                                    fetch('/api/incidents/' + incident.id, {
                                        method: 'DELETE'
                                    })
                                    .then(res => {
                                        if (!res.ok) throw new Error('Erreur lors de la suppression');
                                        return res.json();
                                    })
                                    .then(data => {
                                        marker.remove(); // Retire le marqueur après suppression
                                    })
                                    .catch(err => {
                                        alert('Erreur lors de la suppression: ' + err.message);
                                    });
                                }
                            };
                        }
                    });
                }
            });
        })
        .catch(err => {
            console.error('Erreur lors du chargement des incidents :', err);
        });
};
