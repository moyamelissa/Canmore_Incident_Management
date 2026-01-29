
// =========================
// Titre : Gestion du menu déroulant
// Explication : Script réutilisable pour ouvrir/fermer un menu déroulant au clic et le fermer en cliquant ailleurs.
// =========================

document.addEventListener('DOMContentLoaded', function() {
    // Pour chaque déclencheur de menu déroulant
    document.querySelectorAll('.dropdown-toggle').forEach(function(trigger) {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            // Ferme tous les autres menus déroulants
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

    // Ferme les menus déroulants en cliquant à l'extérieur
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-content').forEach(function(content) {
                content.classList.remove('show');
            });
        }
    });
});
