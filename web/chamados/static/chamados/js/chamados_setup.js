// web/execucao/static/execucao/js/execucao_setup.js
/**
 * Usado em:
 * - web/chamados/templates/execucao/chamado_setup.html
 *
 * Responsabilidade:
 * - Interações da página de setup do chamado (pré-execução).
 *
 * Pré-requisitos DOM:
 * - (preencher) IDs/classes/data-* utilizados no script.
 *
 * Observações:
 * - Carregado via <script defer> no template de página.
 */
(function () {
  function toggleBox(itemId, isChecked) {
    const box = document.getElementById(`cfg-box-${itemId}`);
    const badge = document.getElementById(`cfg-badge-${itemId}`);

    if (!box || !badge) return;

    if (isChecked) {
      box.classList.remove("hidden");
      badge.classList.add("hidden");
      const ipInput = box.querySelector(`input[name="ip_${itemId}"]`);
      if (ipInput) ipInput.focus();
    } else {
      box.classList.add("hidden");
      badge.classList.remove("hidden");
      const ipInput = box.querySelector(`input[name="ip_${itemId}"]`);
      if (ipInput) ipInput.value = "";
    }
  }

  document.addEventListener("change", function (evt) {
    const el = evt.target;
    if (!(el instanceof HTMLInputElement)) return;
    if (!el.classList.contains("js-toggle-config")) return;

    const itemId = el.getAttribute("data-item-id");
    if (!itemId) return;

    toggleBox(itemId, el.checked);
  });
})();