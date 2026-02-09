/**
 * map_incidents_form.js
 * Gestion du formulaire de signalement d'incident
 */

// Affiche le formulaire de signalement d'incident
window.showIncidentForm = function(map, latlng) {
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
                        if (!subjectSelect.value) {
                            alert('Veuillez sélectionner un sujet avant de soumettre le signalement.');
                            return;
                        }
                        if (!detailSelect.value) {
                            alert('Veuillez sélectionner un détail avant de soumettre le signalement.');
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
};
