(function () {
  function initKitsFormset() {
    const addBtn = document.getElementById("btn-add-item");
    const container = document.getElementById("itens-container");
    const template = document.getElementById("empty-form-template");

    if (!addBtn || !container || !template) return;

    const prefix = addBtn.dataset.formsetPrefix || "form";
    const totalFormsInput = document.querySelector(`input[name="${prefix}-TOTAL_FORMS"]`);
    if (!totalFormsInput) return;

    function wireRemoveButtons(scope) {
      scope.querySelectorAll(".btn-remove-new").forEach((btn) => {
        if (btn.dataset.bound === "1") return;
        btn.dataset.bound = "1";

        btn.addEventListener("click", () => {
          const card = btn.closest("div.border");
          if (card) card.remove();
          // MVP: não decrementa TOTAL_FORMS para não bagunçar índices.
        });
      });
    }

    function initDependenciasNovaLinha(rowEl) {
      // chama o JS do "tipo por equipamento" se estiver carregado
      if (
        window.TiposFormset &&
        typeof window.TiposFormset.initRow === "function"
      ) {
        window.TiposFormset.initRow(rowEl);
      }

      // Se a linha nasceu com equipamento já preenchido,
      // forçamos um "change" para garantir carregamento.
      const equipamentoSelect = rowEl.querySelector('select[name$="-equipamento"]');
      if (equipamentoSelect && (equipamentoSelect.value || "").trim()) {
        equipamentoSelect.dispatchEvent(new Event("change", { bubbles: true }));
      }
    }

    function addRow() {
      const index = parseInt(totalFormsInput.value, 10);
      const html = template.innerHTML.replaceAll("__prefix__", String(index));

      const wrapper = document.createElement("div");
      wrapper.innerHTML = html.trim();

      const el = wrapper.firstElementChild;
      if (!el) return;

      container.appendChild(el);
      totalFormsInput.value = String(index + 1);

      wireRemoveButtons(container);

      // ✅ ponto crítico: inicializa dependências da linha nova
      initDependenciasNovaLinha(el);
    }

    addBtn.addEventListener("click", addRow);

    // rewire initial
    wireRemoveButtons(container);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initKitsFormset);
  } else {
    initKitsFormset();
  }
})();
