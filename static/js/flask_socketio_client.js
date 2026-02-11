// flask_socketio_client.js (anciennement websocket_client.js)
// Client Socket.IO pour la mise à jour en temps réel de l'application.

// Assurez-vous d'inclure la bibliothèque Socket.IO dans votre HTML :
// <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

const socket = io(); // Se connecte automatiquement à l'origine du site (Flask)

socket.on('connect', function() {
    const wsMsg = document.createElement('div');
    wsMsg.textContent = 'Mise à jour en temps réel ACTIVÉE (Socket.IO)';
    wsMsg.style.position = 'fixed';
    wsMsg.style.right = '24px';
    wsMsg.style.bottom = '24px';
    wsMsg.style.background = '#d4edda';
    wsMsg.style.color = '#155724';
    wsMsg.style.padding = '12px 20px';
    wsMsg.style.borderRadius = '8px';
    wsMsg.style.boxShadow = '0 2px 8px rgba(0,0,0,0.12)';
    wsMsg.style.fontWeight = 'bold';
    wsMsg.style.zIndex = '9999';
    wsMsg.style.fontSize = '1.1em';
    wsMsg.style.fontFamily = 'sans-serif';
    wsMsg.style.letterSpacing = '0.5px';
    wsMsg.style.textAlign = 'center';
    wsMsg.style.pointerEvents = 'none';
    document.body.appendChild(wsMsg);
    setTimeout(() => wsMsg.remove(), 3500);
});

// Réception d'un message : déclenche la mise à jour en temps réel
socket.on('message', function(msg) {
    if (typeof window.displayAllIncidents === 'function' && window.map) {
        window.displayAllIncidents(window.map);
    }
    if (typeof updateTable === 'function' && typeof updateSummary === 'function') {
        fetch('/api/incidents')
            .then(res => res.json())
            .then(data => {
                allIncidents = data;
                updateTable(data);
                updateSummary(data);
            });
    }
});

socket.on('incident_added', function(data) {
    if (typeof window.displayAllIncidents === 'function' && window.map) {
        window.displayAllIncidents(window.map);
    }
    if (typeof updateTable === 'function' && typeof updateSummary === 'function') {
        fetch('/api/incidents')
            .then(res => res.json())
            .then(data => {
                allIncidents = data;
                updateTable(data);
                updateSummary(data);
            });
    }
});
socket.on('incident_updated', function(data) {
    if (typeof window.displayAllIncidents === 'function' && window.map) {
        window.displayAllIncidents(window.map);
    }
    if (typeof updateTable === 'function' && typeof updateSummary === 'function') {
        fetch('/api/incidents')
            .then(res => res.json())
            .then(data => {
                allIncidents = data;
                updateTable(data);
                updateSummary(data);
            });
    }
});
socket.on('incident_deleted', function(data) {
    if (typeof window.displayAllIncidents === 'function' && window.map) {
        window.displayAllIncidents(window.map);
    }
    if (typeof updateTable === 'function' && typeof updateSummary === 'function') {
        fetch('/api/incidents')
            .then(res => res.json())
            .then(data => {
                allIncidents = data;
                updateTable(data);
                updateSummary(data);
            });
    }
});

socket.on('disconnect', function() {
    const wsErr = document.createElement('div');
    wsErr.textContent = 'Connexion Socket.IO perdue : la mise à jour en temps réel est désactivée.';
    wsErr.style.position = 'fixed';
    wsErr.style.right = '24px';
    wsErr.style.bottom = '24px';
    wsErr.style.background = '#f8d7da';
    wsErr.style.color = '#721c24';
    wsErr.style.padding = '12px 20px';
    wsErr.style.borderRadius = '8px';
    wsErr.style.boxShadow = '0 2px 8px rgba(0,0,0,0.12)';
    wsErr.style.fontWeight = 'bold';
    wsErr.style.zIndex = '9999';
    wsErr.style.fontSize = '1.1em';
    wsErr.style.fontFamily = 'sans-serif';
    wsErr.style.letterSpacing = '0.5px';
    wsErr.style.textAlign = 'center';
    wsErr.style.pointerEvents = 'none';
    document.body.appendChild(wsErr);
    setTimeout(() => wsErr.remove(), 3500);
});

// Pour envoyer un message :
// socket.emit('message', 'Votre message ici');
