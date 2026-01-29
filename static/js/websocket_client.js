
/**
 * websocket_client.js
 * Client WebSocket pour la mise à jour en temps réel de l'application.
 */

// Connexion WebSocket au serveur
const ws = new WebSocket('ws://localhost:8001/ws');


// Affiche un message lors de la connexion WebSocket
ws.onopen = function() {
    const wsMsg = document.createElement('div');
    wsMsg.textContent = 'Connexion WebSocket établie';
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
    document.body.appendChild(wsMsg);
    setTimeout(() => wsMsg.remove(), 3500);
};



// Réception d'un message : déclenche la mise à jour en temps réel
ws.onmessage = function(event) {
    console.log('Received:', event.data);
    if (typeof window.displayAllIncidents === 'function' && window.map) {
        displayAllIncidents(window.map);
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
};


// Affiche un message si la connexion WebSocket est perdue
ws.onclose = function() {
    const wsErr = document.createElement('div');
    wsErr.textContent = 'Connexion WebSocket échouée : la mise à jour en temps réel est désactivée.';
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
    document.body.appendChild(wsErr);
    setTimeout(() => wsErr.remove(), 6000);
};
