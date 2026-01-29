/**
 * map_incidents.js
 * Gestion de l'affichage, du filtrage et du signalement des incidents sur la carte Leaflet
 * Inclut la gestion du mode administrateur, le filtrage, et la soumission d'incidents.
 */

// Gestion du mode administrateur
window.disableAdminMode = function() {
    window.isAdmin = false;
    localStorage.removeItem('isAdmin');
    localStorage.removeItem('adminLoginTime');
    var adminBtn = document.querySelector('.admin-link');
    if (adminBtn) {
        adminBtn.textContent = 'Connexion Administrateur';
        adminBtn.style.color = '';
    }
    location.reload();
};
// Activation du mode admin
window.isAdmin = localStorage.getItem('isAdmin') === 'true';
window.enableAdminMode = function() {
    const password = window.prompt('Entrez le mot de passe administrateur :');
    if (password === 'canmore') {
        window.isAdmin = true;
        localStorage.setItem('isAdmin', 'true');
        // Stocke l'heure de connexion (en ms)
        localStorage.setItem('adminLoginTime', Date.now().toString());
        alert('Mode administrateur activé !');
        // Met à jour l'interface utilisateur 
        var adminBtn = document.querySelector('.admin-link');
        if (adminBtn) {
            adminBtn.textContent = 'Mode Administrateur';
            adminBtn.style.color = 'green';
        }
        // Rafraîchit les marqueurs incidents pour afficher les contrôles admin
        if (window.map) {
            location.reload();
        }
    } else {
        alert('Mot de passe incorrect.');
    }
};

// Initialisation du mode admin au chargement
window.addEventListener('DOMContentLoaded', function() {
    // Déconnexion automatique de l'admin après 10 minutes (600000 ms)
    if (window.isAdmin) {
        var loginTime = parseInt(localStorage.getItem('adminLoginTime'), 10);
        if (!loginTime || (Date.now() - loginTime > 600000)) {
            window.disableAdminMode();
        } else {
            // Met en place un intervalle pour déconnecter automatiquement après 10 minutes
            setInterval(function() {
                var loginTime = parseInt(localStorage.getItem('adminLoginTime'), 10);
                if (window.isAdmin && loginTime && (Date.now() - loginTime > 600000)) {
                    alert('Session administrateur expirée.');
                    window.disableAdminMode();
                }
            }, 60000); // vérifie chaque minute
        }
    }
    // Fonction pour mettre à jour l'UI admin (appelée au chargement et après login)
    function updateAdminUI() {
        var adminBtn = document.querySelector('.admin-link');
        // Ajoute ou met à jour le minuteur admin
        function updateAdminTimer() {
            var timerSpan = document.getElementById('admin-timer');
            if (!window.isAdmin) {
                if (timerSpan) timerSpan.remove();
                return;
            }
            var loginTime = parseInt(localStorage.getItem('adminLoginTime'), 10);
            var now = Date.now();
            var msLeft = 600000 - (now - loginTime);
            if (msLeft < 0) msLeft = 0;
            var min = Math.floor(msLeft / 60000);
            var sec = Math.floor((msLeft % 60000) / 1000);
            var txt = ' (' + min + 'm ' + (sec < 10 ? '0' : '') + sec + 's avant déconnexion)';
            if (!timerSpan) {
                timerSpan = document.createElement('span');
                timerSpan.id = 'admin-timer';
                timerSpan.style.marginLeft = '8px';
                timerSpan.style.fontWeight = 'normal';
                timerSpan.style.fontSize = '0.95em';
                    timerSpan.style.color = '#1976d2';
                adminBtn.parentNode.appendChild(timerSpan);
            }
            timerSpan.textContent = txt;
        }
        if (adminBtn) {
            if (window.isAdmin) {
                adminBtn.textContent = 'Mode Administrateur';
                adminBtn.style.color = 'green';
                // Ajoute le bouton de déconnexion admin si absent
                if (!document.getElementById('admin-logout-btn')) {
                    var logoutBtn = document.createElement('button');
                    logoutBtn.id = 'admin-logout-btn';
                    logoutBtn.textContent = 'Déconnexion Admin';
                    logoutBtn.style.marginLeft = '10px';
                        logoutBtn.style.background = '#1976d2';
                    logoutBtn.style.color = 'white';
                    logoutBtn.style.border = 'none';
                    logoutBtn.style.padding = '4px 10px';
                    logoutBtn.style.borderRadius = '4px';
                    logoutBtn.style.cursor = 'pointer';
                    adminBtn.parentNode.appendChild(logoutBtn);
                    logoutBtn.onclick = function() {
                        window.disableAdminMode();
                    };
                }
                updateAdminTimer();
                // Met à jour le timer chaque seconde
                if (!window._adminTimerInterval) {
                    window._adminTimerInterval = setInterval(function() {
                        if (window.isAdmin) {
                            updateAdminTimer();
                        } else {
                            clearInterval(window._adminTimerInterval);
                            window._adminTimerInterval = null;
                        }
                    }, 1000);
                }
            } else {
                adminBtn.textContent = 'Connexion Administrateur';
                adminBtn.style.color = '';
                var logoutBtn = document.getElementById('admin-logout-btn');
                if (logoutBtn) logoutBtn.remove();
                var timerSpan = document.getElementById('admin-timer');
                if (timerSpan) timerSpan.remove();
                if (window._adminTimerInterval) {
                    clearInterval(window._adminTimerInterval);
                    window._adminTimerInterval = null;
                }
            }
        }
    }
    // Toujours mettre à jour l'UI admin au chargement
    updateAdminUI();
    // Ajoute l'écouteur de clic (évite doublons)
    var adminBtn = document.querySelector('.admin-link');
    if (adminBtn && !adminBtn._adminListenerAdded) {
        adminBtn.addEventListener('click', function(e) {
            e.preventDefault();
            window.enableAdminMode();
            updateAdminUI(); // Met à jour l'UI après login
        });
        adminBtn._adminListenerAdded = true;
    }
    // Si déjà admin au chargement, forcer l'UI
    if (window.isAdmin) {
        updateAdminUI();
    }
});
// Affichage et gestion des incidents sur la carte
var incidentMarkers = [];
function displayAllIncidents(map) {
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

                // Construit le HTML du popup pour chaque incident
                var popupHtml = '<b>Incident signalé</b><br>' +
                    'Sujet : ' + (incident.type || '') + '<br>' +
                    'Détail : ' + (incident.description || '') + '<br>' +
                    'Horodatage : ' + (incident.timestamp || '') + '<br>';

                // Si admin, ajoute le menu déroulant de statut et le bouton de mise à jour
                if (window.isAdmin) {
                    popupHtml +=
                        '<div style="margin-top:8px">' +
                        '<label for="status-select-' + incident.id + '">Statut :</label> ' +
                        '<select id="status-select-' + incident.id + '">' +
                        '<option value="unsolved"' + (!isSolved ? ' selected' : '') + '>Non résolu</option>' +
                        '<option value="solved"' + (isSolved ? ' selected' : '') + '>Résolu</option>' +
                        '</select> ' +
                        '<button id="update-status-btn-' + incident.id + '" class="admin-status-btn">Mettre à jour le statut</button>' +
                        '<button id="delete-incident-btn-' + incident.id + '" class="admin-delete-btn" style="margin-left:8px;background:#d32f2f;color:white;border:none;padding:4px 10px;border-radius:4px;cursor:pointer;">Supprimer</button>' +
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
            console.error('Erreur lors du chargement des incidents :', err); // Affiche l'erreur dans la console
        });
}
// Signalement d'un incident sur la carte (utilisateur)

var canmoreBoundaryGeoJson = null; // Contient la géométrie de la limite de Canmore

// Chargement de la limite de Canmore (GeoJSON)
function loadCanmoreBoundary(url, callback) {
    fetch(url)
        .then(res => res.json())
        .then(data => {
            canmoreBoundaryGeoJson = data;
            if (callback) callback();
        });
}

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

// Affiche le formulaire de signalement d'incident
function showIncidentForm(map, latlng) {
    // Récupère les types d'incidents depuis l'API et affiche le formulaire
    fetch('/api/incident_types')
        .then(res => res.json())
        .then(function(incidentTypes) {
            var subjectOptions = `<option value="" disabled selected>Choisissez un sujet</option>` +
                incidentTypes.map(function(type, idx) {
                    return `<option value="${idx}">${type.subject}</option>`;
                }).join('');

            var detailsOptions = `<option value="" disabled selected>Choisissez un détail</option>`;

            // Formulaire HTML pour le signalement
            var formHtml = `
                <form id="incident-comment-form">
                    <label for="incident-subject">Sujet :</label><br>
                    <select id="incident-subject" name="subject">${subjectOptions}</select><br><br>
                    <label for="incident-detail">Détail :</label><br>
                    <select id="incident-detail" name="detail" disabled>${detailsOptions}</select><br><br>
                    <label for="incident-comment">Commentaires :</label><br>
                    <textarea id="incident-comment" name="comment" rows="3" cols="25" placeholder="Décrivez l'incident..."></textarea><br>
                    <div id="word-count" style="font-size: 0.9em; color: #555;">0 / 150 mots</div>
                    <button type="submit">Envoyer</button>
                </form>
            `;
            L.popup()
                .setLatLng(latlng)
                .setContent(formHtml)
                .openOn(map);

            // Initialisation des éléments du formulaire après affichage
            setTimeout(function() {
                var form = document.getElementById('incident-comment-form');
                var subjectSelect = document.getElementById('incident-subject');
                var detailSelect = document.getElementById('incident-detail');
                var commentArea = document.getElementById('incident-comment');
                var wordCountDiv = document.getElementById('word-count');
                if (subjectSelect && detailSelect) {
                    subjectSelect.onchange = function() {
                        var idx = subjectSelect.value;
                        if (idx !== "") {
                            var options = `<option value=\"\" disabled selected>Choisissez un détail</option>` +
                                incidentTypes[idx].details.map(function(detail) {
                                    return `<option value=\"${detail}\">${detail}</option>`;
                                }).join('');
                            detailSelect.innerHTML = options;
                            detailSelect.disabled = false;
                        } else {
                            detailSelect.innerHTML = `<option value=\"\" disabled selected>Choisissez un détail</option>`;
                            detailSelect.disabled = true;
                        }
                    };
                }
                if (commentArea && wordCountDiv) {
                    var updateWordCount = function() {
                        var comment = commentArea.value.trim();
                        var wordCount = comment ? comment.split(/\s+/).filter(Boolean).length : 0;
                        wordCountDiv.textContent = wordCount + ' / 150 mots';
                    };
                    commentArea.addEventListener('input', updateWordCount);
                    updateWordCount();
                }
                if (form) {
                    form.onsubmit = function(e) {
                            e.preventDefault();
                            var comment = commentArea.value.trim();
                            var wordCount = comment.split(/\s+/).filter(Boolean).length;
                            if (wordCount > 150) {
                                alert('Le commentaire ne doit pas dépasser 150 mots.');
                                return;
                            }
                            // Dépose un marqueur rouge à l'emplacement de l'incident
                            var redIcon = L.icon({
                                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
                                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
                                iconSize: [25, 41],
                                iconAnchor: [12, 41],
                                popupAnchor: [1, -34],
                                shadowSize: [41, 41]
                            });
                            var marker = L.marker(latlng, {icon: redIcon}).addTo(map);
                            marker.bindPopup('<b>Incident signalé</b><br>' +
                                'Sujet : ' + subjectSelect.options[subjectSelect.selectedIndex].text + '<br>' +
                                'Détail : ' + detailSelect.options[detailSelect.selectedIndex].text + '<br>' +
                                'Commentaire : ' + commentArea.value.replace(/</g, '&lt;').replace(/>/g, '&gt;')
                            ).openPopup();
                            map.closePopup();

                            // Envoie les données de l'incident au backend
                            var incidentData = {
                                type: subjectSelect.options[subjectSelect.selectedIndex].text,
                                description: detailSelect.options[detailSelect.selectedIndex].text,
                                latitude: latlng.lat,
                                longitude: latlng.lng,
                                timestamp: new Date().toISOString()
                            };
                            fetch('/api/incidents', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(incidentData)
                            })
                            .then(res => res.json())
                            .then(data => {
                            })
                            .catch(err => {
                            });
                    };
                }
            }, 100);
        });
}

// Affiche un message d'erreur si clic hors limite
function showError(map, latlng) {
    L.popup()
        .setLatLng(latlng)
        .setContent('<span style="color:red">Vous ne pouvez signaler un incident qu\'à l\'intérieur de Canmore.</span>')
        .openOn(map);
}

// Initialisation après chargement de la carte
function setupIncidentReporting(map) {
    // Affiche tous les incidents existants au chargement de la carte
    displayAllIncidents(map);

    // Ajoute les écouteurs sur les filtres incidents
    document.querySelectorAll('.incident-filter').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            displayAllIncidents(map);
        });
    });

    // Gestion du clic sur la carte pour signaler un incident ou afficher une erreur
    map.on('click', function(e) {
        if (isInsideCanmore(e.latlng)) {
            showIncidentForm(map, e.latlng);
        } else {
            showError(map, e.latlng);
        }
    });
}