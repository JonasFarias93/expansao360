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