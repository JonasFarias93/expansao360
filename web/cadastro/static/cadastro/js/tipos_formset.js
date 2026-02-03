(function () {
  function initTiposFormset() {
    const addBtn = document.getElementById("btn-add-tipo");
    const container = document.getElementById("tipos-container");
    const totalForms = document.getElementById("id_tipos-TOTAL_FORMS");
    const rowTemplate = document.getElementById("tipo-empty-form-template");

    if (!addBtn || !container || !totalForms || !rowTemplate) return;

    function addRow() {
      const index = parseInt(totalForms.value, 10);

      // Clona o template e substitui __prefix__ pelo índice real
      const html = rowTemplate.innerHTML.replaceAll("__prefix__", String(index));

      const wrapper = document.createElement("div");
      wrapper.className = "border-t border-slate-100 pt-3 tipo-row";
      wrapper.innerHTML = html;

      container.appendChild(wrapper);
      totalForms.value = String(index + 1);
    }

    addBtn.addEventListener("click", addRow);
  }

  // garante que roda após o DOM carregar
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initTiposFormset);
  } else {
    initTiposFormset();
  }
})();
