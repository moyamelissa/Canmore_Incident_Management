/**
 * map_incidents_admin.js
 * Gestion du mode administrateur : authentification, session, timer et interface
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
        alert('Mode administrateur activé! Vous avez 10 minutes avant d\'être automatiquement déconnecté.');
        // Rafraîchit la page pour afficher les contrôles admin
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
            var txt = min + 'm ' + (sec < 10 ? '0' : '') + sec + 's';
            if (!timerSpan) {
                timerSpan = document.createElement('span');
                timerSpan.id = 'admin-timer';
                timerSpan.style.marginRight = '8px';
                timerSpan.style.fontWeight = '500';
                timerSpan.style.fontSize = '0.9em';
                timerSpan.style.color = '#c62828';
                var rightMenu = document.querySelector('.menu-right-modern');
                if (rightMenu) {
                    rightMenu.insertBefore(timerSpan, rightMenu.firstChild);
                }
            }
            timerSpan.textContent = txt;
        }
        if (adminBtn) {
            if (window.isAdmin) {
                adminBtn.textContent = 'Mode Administrateur';
                adminBtn.style.color = 'green';
                // Ajoute le bouton de déconnexion admin si absent
                if (!document.getElementById('admin-logout-btn')) {
                    var li = document.createElement('li');
                    var logoutBtn = document.createElement('button');
                    logoutBtn.id = 'admin-logout-btn';
                    logoutBtn.className = 'btn-unified';
                    logoutBtn.textContent = 'Déconnexion Admin';
                    li.appendChild(logoutBtn);
                    var adminLi = adminBtn.parentNode;
                    adminLi.parentNode.insertBefore(li, adminLi.nextSibling);
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
                if (logoutBtn && logoutBtn.parentNode) logoutBtn.parentNode.remove();
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
