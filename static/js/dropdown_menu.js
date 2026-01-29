
/**
 * dropdown_menu.js
 * Gestion des menus déroulants pour l'application Canmore Incident Management.
 */

document.addEventListener('DOMContentLoaded', function() {

    
    // Initialisation des événements sur les menus déroulants

    // Pour chaque déclencheur de menu déroulant
    document.querySelectorAll('.dropdown-toggle').forEach(function(trigger) {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            // Ferme tous les autres menus déroulants ouverts
            document.querySelectorAll('.dropdown-content').forEach(function(content) {
                if (content !== trigger.nextElementSibling) {
                    content.classList.remove('show');
                }
            });
            // Ouvre ou ferme ce menu déroulant
            var dropdown = trigger.nextElementSibling;
            if (dropdown) {
                dropdown.classList.toggle('show');
            }
        });
    });

    // Gestion du clic extérieur pour fermer les menus déroulants

    document.addEventListener('click', function(e) {
        // Si le clic n'est pas dans un menu déroulant, on ferme tous les menus
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-content').forEach(function(content) {
                content.classList.remove('show');
            });
        }
    });
});