// Aguarda 5 segundos e depois esconde os alerts

setTimeout(function() {
    let alerts = document.querySelectorAll(".alerta");
    alerts.forEach(function(alert) {
        alert.style.transition = "opacity 0.5s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 500); // Remove a div após desaparecer
    });
}, 5000); // 5000ms = 5 segundos

// Toggle sidebar
document.getElementById('sidebarToggle').addEventListener('click', function() {
    document.getElementById('accordionSidebar').classList.toggle('collapsed');
    document.getElementById('sidebarToggle').classList.toggle('collapsed');
});

// Mobile sidebar toggle
document.getElementById('sidebarToggleTop').addEventListener('click', function() {
    document.getElementById('accordionSidebar').classList.toggle('mobile-show');
});

document.addEventListener("DOMContentLoaded", function () {
    const toggler = document.getElementById('sidebar');
    const sidebarCard = document.querySelector('.alerta_compra-card');

    toggler.addEventListener('click', function () {
      // Alterna uma classe para esconder ou mostrar a sidebar-card
      sidebarCard.classList.toggle('d-none');
    });
  });