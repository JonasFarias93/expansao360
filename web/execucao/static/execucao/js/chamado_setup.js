// web/execucao/static/execucao/js/chamado_setup.js

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