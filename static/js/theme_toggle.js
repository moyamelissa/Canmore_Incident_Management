
/**
 * theme_toggle.js
 * Gestion universelle du mode sombre (dark mode) et des préférences utilisateur.
 */

function initThemeToggle({darkCss, storageKey, icon, iconClass, defaultMode = 'light'}) {
    // Création du bouton paramètres et du modal si absents
    storageKey = 'darkModeGlobal';
    document.addEventListener('DOMContentLoaded', function() {
        let settingsBtn = document.getElementById('settings-btn');
        if (!settingsBtn) {
            settingsBtn = document.createElement('button');
            settingsBtn.id = 'settings-btn';
            settingsBtn.title = 'Paramètres';
            settingsBtn.style.background = 'none';
            settingsBtn.style.border = 'none';
            settingsBtn.style.cursor = 'pointer';
            settingsBtn.style.marginLeft = '18px';
            settingsBtn.style.verticalAlign = 'middle';
            settingsBtn.style.position = 'absolute';
            settingsBtn.style.top = '22px';
            settingsBtn.style.right = '24px';
            settingsBtn.style.zIndex = '10001';
            let img = document.createElement('img');
            img.src = icon;
            img.alt = 'Paramètres';
            img.className = iconClass;
            img.style.width = '28px';
            img.style.height = '28px';
            function updateIconColor() {
                if (document.body.classList.contains('dark-mode')) {
                    img.style.filter = 'invert(1)';
                } else {
                    img.style.filter = 'invert(0)';
                }
            }
            updateIconColor();
            settingsBtn.appendChild(img);
            document.body.appendChild(settingsBtn);
            const observer = new MutationObserver(updateIconColor);
            observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
        }
        let settingsModal = document.getElementById('settings-modal');
        if (!settingsModal) {
            settingsModal = document.createElement('div');
            settingsModal.id = 'settings-modal';
            settingsModal.style.display = 'none';
            settingsModal.style.position = 'fixed';
            settingsModal.style.top = '0';
            settingsModal.style.left = '0';
            settingsModal.style.right = '0';
            settingsModal.style.bottom = '0';
            settingsModal.style.background = 'rgba(0,0,0,0.35)';
            settingsModal.style.zIndex = '9999';
            settingsModal.style.alignItems = 'center';
            settingsModal.style.justifyContent = 'center';
            let modalContent = document.createElement('div');
            modalContent.id = 'settings-modal-content';
            modalContent.style.background = '#ffffff';
            modalContent.style.color = '#333333';
            modalContent.style.borderRadius = '10px';
            modalContent.style.padding = '32px 28px 24px 28px';
            modalContent.style.minWidth = '320px';
            modalContent.style.boxShadow = '0 4px 24px #0005';
            modalContent.style.position = 'relative';
            let closeBtn = document.createElement('button');
            closeBtn.id = 'close-settings';
            closeBtn.innerHTML = '&times;';
            closeBtn.style.position = 'absolute';
            closeBtn.style.top = '10px';
            closeBtn.style.right = '14px';
            closeBtn.style.background = 'none';
            closeBtn.style.border = 'none';
            closeBtn.style.color = '#333333';
            closeBtn.style.fontSize = '1.5em';
            closeBtn.style.cursor = 'pointer';
            modalContent.appendChild(closeBtn);
            let h2 = document.createElement('h2');
            h2.textContent = 'Paramètres';
            h2.style.marginTop = '0';
            modalContent.appendChild(h2);
            let label = document.createElement('label');
            label.style.display = 'flex';
            label.style.alignItems = 'center';
            label.style.marginBottom = '18px';
            label.style.fontSize = '1.1em';
            let darkToggle = document.createElement('input');
            darkToggle.type = 'checkbox';
            darkToggle.id = 'darkmode-toggle';
            darkToggle.style.marginRight = '12px';
            darkToggle.style.transform = 'scale(1.2)';
            label.appendChild(darkToggle);
            label.appendChild(document.createTextNode(' Mode sombre'));
            modalContent.appendChild(label);
            settingsModal.appendChild(modalContent);
            document.body.appendChild(settingsModal);
        }
        var closeSettings = document.getElementById('close-settings');
        var darkToggle = document.getElementById('darkmode-toggle');
        var darkLink = null;

        // Gestion du mode sombre (activation/désactivation)
        function setDarkMode(on) {
            let modalContent = document.getElementById('settings-modal-content');
            let closeBtn = document.getElementById('close-settings');
            if (on) {
                if (!darkLink) {
                    darkLink = document.createElement('link');
                    darkLink.rel = 'stylesheet';
                    darkLink.href = darkCss;
                    document.head.appendChild(darkLink);
                }
                document.body.classList.add('dark-mode');
                // Update modal colors for dark mode
                if (modalContent) {
                    modalContent.style.background = '#23272a';
                    modalContent.style.color = '#e0e0e0';
                }
                if (closeBtn) closeBtn.style.color = '#e0e0e0';
                localStorage.setItem(storageKey, 'true');
                fetch('/save_user_settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ [storageKey]: true })
                });
            } else {
                if (darkLink) {
                    darkLink.remove();
                    darkLink = null;
                } else {
                    var links = document.querySelectorAll('link[href$="' + darkCss.split('/').pop() + '"]');
                    links.forEach(l => l.remove());
                }
                document.body.classList.remove('dark-mode');
                // Update modal colors for light mode
                if (modalContent) {
                    modalContent.style.background = '#ffffff';
                    modalContent.style.color = '#333333';
                }
                if (closeBtn) closeBtn.style.color = '#333333';
                localStorage.setItem(storageKey, 'false');
                fetch('/save_user_settings', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ [storageKey]: false })
                });
            }
        }}

        // Initialisation de l'état du mode sombre
        if (localStorage.getItem(storageKey) === 'true') {
            darkToggle.checked = true;
            setDarkMode(true);
        } else if (defaultMode === 'dark') {
            darkToggle.checked = true;
            setDarkMode(true);
        } else {
            darkToggle.checked = false;
            setDarkMode(false);
        }

        // Gestion des interactions utilisateur
        settingsBtn.addEventListener('click', function() {
            settingsModal.style.display = 'flex';
        });
        closeSettings.addEventListener('click', function() {
            settingsModal.style.display = 'none';
        });
        settingsModal.addEventListener('click', function(e) {
            if (e.target === settingsModal) settingsModal.style.display = 'none';
        });
        darkToggle.addEventListener('change', function() {
            setDarkMode(darkToggle.checked);
        });
    });
}
