// web/cadastro/static/cadastro/js/tipos_formset.js
(function () {
  // =========================
  // Helpers
  // =========================

  // jsdom pode não ter CSS.escape dependendo da versão/config
  const cssEscape =
    (typeof CSS !== "undefined" && typeof CSS.escape === "function")
      ? CSS.escape
      : (s) => String(s).replace(/["\\]/g, "\\$&");

  function buildOptions(items, selectedValue) {
    const opts = ['<option value="">---------</option>'];

    for (const it of items) {
      const id = String(it.id);
      const nome = String(it.nome ?? "");
      const selected = selectedValue && String(selectedValue) === id ? " selected" : "";
      opts.push(`<option value="${id}"${selected}>${nome}</option>`);
    }
    return opts.join("");
  }

  async function fetchTipos(tiposUrl, equipamentoId) {
    const url = `${tiposUrl}?equipamento_id=${encodeURIComponent(equipamentoId)}`;
    const resp = await fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    return await resp.json(); // endpoint atual retorna JSON
  }

  function getTipoSelectFromEquipSelect(equipSelect) {
    // mesmo prefix do formset: troca "-equipamento" por "-tipo"
    const tipoName = equipSelect.name.replace("-equipamento", "-tipo");
    return document.querySelector(`select[name="${cssEscape(tipoName)}"]`);
  }

  async function hydrateTipoForRow(equipSelect, tiposUrl) {
    const equipamentoId = equipSelect.value;
    const tipoSelect = getTipoSelectFromEquipSelect(equipSelect);
    if (!tipoSelect) return;

    // guarda seleção atual (Django já seta value mesmo sem options)
    const currentTipoValue = tipoSelect.value;

    if (!equipamentoId) {
      tipoSelect.innerHTML = '<option value="">---------</option>';
      tipoSelect.value = "";
      return;
    }

    try {
      const tipos = await fetchTipos(tiposUrl, equipamentoId);
      tipoSelect.innerHTML = buildOptions(tipos, currentTipoValue);

      // garante re-seleção (caso o option selected não bastou)
      if (currentTipoValue) tipoSelect.value = String(currentTipoValue);
    } catch (e) {
      // fallback seguro
      tipoSelect.innerHTML = '<option value="">---------</option>';
    }
  }

  // =========================
  // Public init (test-friendly)
  // =========================

  function initTiposFormset(opts = {}) {
    const container =
      opts.container || document.getElementById("itens-container");
    if (!container) return;

    const tiposUrl =
      opts.tiposUrl || container.getAttribute("data-tipos-url");
    if (!tiposUrl) return;

    // evita duplicar listeners se init for chamado mais de 1 vez
    if (container.dataset.tiposFormsetBound === "1") return;
    container.dataset.tiposFormsetBound = "1";

    // 1) no load: hidrata todas as linhas que já possuem equipamento
    const equips = container.querySelectorAll('select[name$="-equipamento"]');
    equips.forEach((equipSelect) => {
      if (equipSelect.value) hydrateTipoForRow(equipSelect, tiposUrl);
    });

    // 2) on change: hidrata a linha atual
    container.addEventListener("change", (ev) => {
      const target = ev.target;
      if (!(target instanceof HTMLSelectElement)) return;
      if (!target.name.endsWith("-equipamento")) return;

      hydrateTipoForRow(target, tiposUrl);
    });
  }

  // expõe no window pra testes
  window.__cadastro__ = window.__cadastro__ || {};
  window.__cadastro__.initTiposFormset = initTiposFormset;

  // mantém comportamento atual no browser
  document.addEventListener("DOMContentLoaded", () => {
    initTiposFormset();
  });
})();