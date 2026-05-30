/**
 * Usado em:
 * - web/chamados/templates/execucao/chamado_execucao.html
 *
 * Responsabilidade:
 * - Comportamentos da tela de execução/detalhe (UI de detalhe, inicialização da página, binds principais).
 *
 * Pré-requisitos DOM:
 * - (preencher) IDs/classes/data-* utilizados no script.
 *
 * Observações:
 * - Carregado via <script defer> no template de página.
 */

// =====================================
// Itens de Execução — UI helpers
// (sem dependências)
// =====================================
(function () {
  // Progress bar (data-progress-bar)
  document.querySelectorAll("[data-progress-bar]").forEach((bar) => {
    const raw = bar.getAttribute("data-progress");
    const pct = Math.max(0, Math.min(100, Number(raw || 0)));
    bar.style.width = `${pct}%`;
  });

  // IP edit toggle (item a item)
  document.querySelectorAll("[data-ip-edit-btn]").forEach((btn) => {
    const id = btn.getAttribute("data-ip-edit-btn");
    if (!id) return;

    const readBox = document.querySelector(`[data-ip-read="${id}"]`);
    const editBox = document.querySelector(`[data-ip-edit="${id}"]`);
    const input = document.querySelector(`[data-ip-input="${id}"]`);
    const hidden = document.querySelector(`[data-ip-hidden="${id}"]`);
    const cancelBtn = document.querySelector(`[data-ip-cancel-btn="${id}"]`);

    if (!readBox || !editBox || !hidden) return;

    btn.addEventListener("click", () => {
      readBox.classList.add("hidden");
      editBox.classList.remove("hidden");
      hidden.disabled = true; // evita enviar dois ip_<id> no POST
      if (input) input.focus();
    });

    if (cancelBtn) {
      cancelBtn.addEventListener("click", () => {
        editBox.classList.add("hidden");
        readBox.classList.remove("hidden");
        hidden.disabled = false;
        if (input) input.value = hidden.value || "";
      });
    }
  });
})();


// =====================================
// TAB behavior — leitor de código de barras
// serie -> próximo ativo
// =====================================
(function () {
  const items = Array.from(document.querySelectorAll("[data-item-root]"));

  items.forEach((itemEl, idx) => {
    const id = itemEl.getAttribute("data-item-id");
    const serieInput = itemEl.querySelector(`[name="serie_${id}"]`);
    if (!serieInput) return;

    serieInput.addEventListener("keydown", (e) => {
      if (e.key !== "Tab" || e.shiftKey) return;

      // próximo item com campo ativo
      for (let i = idx + 1; i < items.length; i++) {
        const nextId = items[i].getAttribute("data-item-id");
        const nextAtivo = items[i].querySelector(`[name="ativo_${nextId}"]`);
        if (nextAtivo) {
          e.preventDefault();
          nextAtivo.focus();
          return;
        }
      }
      // se não tem próximo, deixa TAB natural
    });
  });
})();