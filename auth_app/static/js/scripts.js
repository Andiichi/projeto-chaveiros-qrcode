// Aguarda 5 segundos e depois esconde os alerts

setTimeout(function() {
    let alerts = document.querySelectorAll(".alert");
    alerts.forEach(function(alert) {
        alert.style.transition = "opacity 0.5s";
        alert.style.opacity = "0";
        setTimeout(() => alert.remove(), 500); // Remove a div após desaparecer
    });
}, 5000); // 5000ms = 5 segundos