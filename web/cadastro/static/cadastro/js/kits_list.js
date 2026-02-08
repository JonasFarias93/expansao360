(function () {
  function qs(root, sel) {
    return root.querySelector(sel);
  }

  function setHidden(el, hidden) {
    if (!el) return;
    el.classList.toggle("hidden", hidden);
  }

  function closeAll(exceptKitId) {
    document.querySelectorAll('button[data-kit-id]').forEach((btn) => {
      const kitId = btn.getAttribute("data-kit-id");
      if (kitId === String(exceptKitId)) return;

      btn.setAttribute("aria-expanded", "false");
      const row = document.getElementById(`kit-itens-row-${kitId}`);
      if (row) row.classList.add("hidden");
    });
  }

  async function loadItens(btn) {
    const url = btn.getAttribute("data-kit-itens-url");
    const kitId = btn.getAttribute("data-kit-id");

    const row = document.getElementById(`kit-itens-row-${kitId}`);
    const region = document.getElementById(`kit-itens-${kitId}`);
    if (!row || !region || !url) return;

    const state = qs(region, "[data-kit-itens-state]");
    const errBox = qs(region, "[data-kit-itens-error]");
    const emptyBox = qs(region, "[data-kit-itens-empty]");
    const listBox = qs(region, "[data-kit-itens-list]");
    const tbody = qs(region, "[data-kit-itens-tbody]");

    // cache: se já carregou uma vez, não busca novamente
    if (region.dataset.loaded === "1") return;

    // reset UI
    setHidden(errBox, true);
    setHidden(emptyBox, true);
    setHidden(listBox, true);
    setHidden(state, false);
    if (state) state.textContent = "Carregando itens…";

    try {
      const resp = await fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } });
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const data = await resp.json();

      const itens = Array.isArray(data.itens) ? data.itens : [];
      if (tbody) tbody.innerHTML = "";

      if (itens.length === 0) {
        setHidden(state, true);
        setHidden(emptyBox, false);
        region.dataset.loaded = "1";
        return;
      }

      const rowsHtml = itens.map((i) => {
        const cfg = i.requer_configuracao ? "Sim" : "Não";
        const nome = i.nome ?? "";
        const tipo = i.tipo ?? "";
        const qtd = (i.quantidade ?? "").toString();
        return `
          <tr class="border-t border-slate-200">
            <td class="py-2 pr-4 text-slate-900">${escapeHtml(nome)}</td>
            <td class="py-2 pr-4 text-slate-700">${escapeHtml(tipo)}</td>
            <td class="py-2 pr-4 text-slate-700">${escapeHtml(qtd)}</td>
            <td class="py-2 pr-4 text-slate-700">${cfg}</td>
          </tr>
        `;
      }).join("");

      if (tbody) tbody.innerHTML = rowsHtml;

      setHidden(state, true);
      setHidden(listBox, false);
      region.dataset.loaded = "1";
    } catch (e) {
      setHidden(state, true);
      setHidden(errBox, false);
    }
  }

  function escapeHtml(s) {
    return String(s)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function toggle(btn) {
    const kitId = btn.getAttribute("data-kit-id");
    const row = document.getElementById(`kit-itens-row-${kitId}`);
    if (!row) return;

    const isOpen = btn.getAttribute("aria-expanded") === "true";

    if (isOpen) {
      btn.setAttribute("aria-expanded", "false");
      row.classList.add("hidden");
      return;
    }

    // mantém no máximo 1 aberto por vez
    closeAll(kitId);

    btn.setAttribute("aria-expanded", "true");
    row.classList.remove("hidden");

    // mantém foco no botão (não “salta”)
    // se você quiser focar a região por acessibilidade, descomente:
    // const region = document.getElementById(`kit-itens-${kitId}`);
    // if (region) region.focus();

    // lazy-load
    loadItens(btn);
  }

  function init() {
    document.querySelectorAll('button[data-kit-id][data-kit-itens-url]').forEach((btn) => {
      btn.addEventListener("click", (ev) => {
        ev.preventDefault();
        toggle(btn);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", init);
})();