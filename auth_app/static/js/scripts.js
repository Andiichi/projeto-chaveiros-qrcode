// Aguarda 5 segundos e depois esconde os alerts

setTimeout(function() {
    let alerts = document.querySelectorAll(".alert");
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

// // popovers do modal criacao de chaveiros
// document.querySelectorAll('[data-bs-toggle="popover"]').forEach((popover) => {
//     new bootstrap.Popover(popover);
//   });


const formsetDiv = document.getElementById('phones-formset');
    const addBtn = document.getElementById('add-phone');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');

    addBtn.addEventListener('click', function () {
        const formCount = parseInt(totalForms.value);
        const firstForm = formsetDiv.querySelector('.phone-form');

        if (!firstForm) return;

        const newForm = firstForm.cloneNode(true);

        // Limpa os valores e atualiza os atributos name/id
        newForm.querySelectorAll('input').forEach((input) => {
            const name = input.getAttribute('name');
            const id = input.getAttribute('id');

            if (name) {
                const newName = name.replace(/form-\d+-/, `form-${formCount}-`);
                input.setAttribute('name', newName);
            }

            if (id) {
                const newId = id.replace(/form-\d+-/, `form-${formCount}-`);
                input.setAttribute('id', newId);
            }

            if (input.type === 'text') {
                input.value = '';
            }

            if (input.type === 'checkbox') {
                input.checked = false;
            }
        });

        formsetDiv.appendChild(newForm);
        totalForms.value = formCount + 1;
    });