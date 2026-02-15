// web/execucao/static/execucao/js/execucao_fila_operacional.js
/**
 * Usado em:
 * - web/chamados/templates/execucao/fila_operacional.html
 *
 * Responsabilidade:
 * - Comportamentos da fila operacional (ações de fila, interações do operador, navegação/atualização da lista).
 *
 * Pré-requisitos DOM:
 * - (preencher conforme o arquivo) IDs/classes usados no script.
 *
 * Observações:
 * - Carregado via <script defer> no template de página.
 * - Não deve ser importado por componentes/parciais.
 */
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