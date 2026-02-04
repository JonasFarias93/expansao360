console.log("tipos_formset carregou - vTEST");


(function () {
  // ============================
  // 1) FORMSET: adicionar "Tipo" (cadastro de equipamentos/categorias)
  // ============================
  function initTiposCrudFormset() {
    const addBtn = document.getElementById("btn-add-tipo");
    const container = document.getElementById("tipos-container");
    const totalForms = document.getElementById("id_tipos-TOTAL_FORMS");
    const rowTemplate = document.getElementById("tipo-empty-form-template");

    if (!addBtn || !container || !totalForms || !rowTemplate) return;

    function addRow() {
      const index = parseInt(totalForms.value, 10);
      const html = rowTemplate.innerHTML.replaceAll("__prefix__", String(index));

      const wrapper = document.createElement("div");
      wrapper.className = "border-t border-slate-100 pt-3 tipo-row";
      wrapper.innerHTML = html;

      container.appendChild(wrapper);
      totalForms.value = String(index + 1);
    }

    addBtn.addEventListener("click", addRow);
  }

  // ============================
  // 2) KIT: "Tipo" dependente do "Equipamento" (AJAX)
  //    ✅ Delegação de eventos (resolve linhas novas)
  // ============================
  function getKitContainer() {
    return document.getElementById("itens-container");
  }

  function getTiposUrl() {
    const container = getKitContainer();
    return container?.dataset?.tiposUrl || "";
  }

  function resetTipoSelect(selectEl) {
    selectEl.innerHTML = "";
    const opt = document.createElement("option");
    opt.value = "";
    opt.textContent = "---------";
    selectEl.appendChild(opt);
  }

  async function fetchTiposPorEquipamento(equipamentoId) {
    const baseUrl = getTiposUrl();
    if (!baseUrl) {
      console.error(
        "data-tipos-url não encontrado em #itens-container. " +
          "Confirme o atributo no kits_update.html."
      );
      return [];
    }

    const url = `${baseUrl}?equipamento_id=${encodeURIComponent(equipamentoId)}`;

    let resp;
    try {
      resp = await fetch(url, {
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
    } catch (err) {
      console.error("Erro de rede ao buscar tipos:", err);
      return [];
    }

    if (!resp.ok) {
      console.error("Falha ao buscar tipos:", resp.status, url);
      return [];
    }

    try {
      return await resp.json();
    } catch (err) {
      console.error("JSON inválido em tipos-por-equipamento:", err);
      return [];
    }
  }

  async function loadTiposForRow(rowEl, equipamentoSelect) {
    const tipoSelect = rowEl.querySelector('select[name$="-tipo"]');
    if (!tipoSelect) return;

    resetTipoSelect(tipoSelect);

    const equipamentoId = (equipamentoSelect.value || "").trim();
    if (!equipamentoId) return;

    const tipos = await fetchTiposPorEquipamento(equipamentoId);

    for (const t of tipos) {
      const opt = document.createElement("option");
      opt.value = t.id;
      opt.textContent = t.nome;
      tipoSelect.appendChild(opt);
    }
  }

  function initKitTiposDelegation() {
    const container = getKitContainer();
    if (!container) return;

    // ✅ evita bind duplicado (importante pra testes e para páginas com re-init)
    if (container.dataset.tiposDelegationBound === "1") return;
    container.dataset.tiposDelegationBound = "1";

    // ✅ Delegação: pega change de qualquer linha, inclusive as adicionadas via JS
    container.addEventListener("change", (ev) => {
      const target = ev.target;
      if (!(target instanceof HTMLSelectElement)) return;

      // só interessa o select do equipamento
      if (!target.matches('select[name$="-equipamento"]')) return;

      const row = target.closest("div.border");
      if (!row) return;

      loadTiposForRow(row, target);
    });

    // ✅ opcional: se houver linhas já preenchidas (equipamento selecionado),
    // carrega tipos no load (sem depender de change)
    container.querySelectorAll('select[name$="-equipamento"]').forEach((sel) => {
      const row = sel.closest("div.border");
      if (!row) return;
      if ((sel.value || "").trim()) {
        loadTiposForRow(row, sel);
      } else {
        const tipoSelect = row.querySelector('select[name$="-tipo"]');
        if (tipoSelect) resetTipoSelect(tipoSelect);
      }
    });
  }

  // Mantém API pública (não atrapalha e é útil)
  window.TiposFormset = window.TiposFormset || {};
  window.TiposFormset.initRow = function (rowEl) {
    const equipamentoSelect = rowEl.querySelector('select[name$="-equipamento"]');
    if (!equipamentoSelect) return;

    // garante placeholder no tipo
    const tipoSelect = rowEl.querySelector('select[name$="-tipo"]');
    if (tipoSelect) resetTipoSelect(tipoSelect);

    // se já veio com valor, carrega
    if ((equipamentoSelect.value || "").trim()) {
      loadTiposForRow(rowEl, equipamentoSelect);
    }
  };

  window.TiposFormset.initAll = function () {
    initKitTiposDelegation();
  };

  function initAll() {
    initTiposCrudFormset();
    initKitTiposDelegation();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }

  // API interna só para testes / debug
window.__cadastro__ = window.__cadastro__ || {};
window.__cadastro__.initTiposFormset = function () {
  initAll();
};

})();



