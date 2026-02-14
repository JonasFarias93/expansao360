// web/execucao/static/execucao/js/fila_operacional.js
(function () {
  function initDetailsAccordion() {
    const toggles = document.querySelectorAll("[data-details-toggle]");
    if (!toggles.length) return;

    toggles.forEach((btn) => {
      const id = btn.getAttribute("data-details-toggle");
      if (!id) return;

      const panel = document.querySelector(`[data-details-panel="${id}"]`);
      if (!panel) return;

      btn.addEventListener("click", () => {
        const isOpen = !panel.classList.contains("hidden");

        if (isOpen) {
          panel.classList.add("hidden");
          btn.setAttribute("aria-expanded", "false");
        } else {
          panel.classList.remove("hidden");
          btn.setAttribute("aria-expanded", "true");
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", initDetailsAccordion);
})();