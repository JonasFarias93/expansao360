// execution_state.js
// Responsibility: Centralized execution UI state manager
// Used in: chamado_execucao.html
// Scope: PR6 Extra — Execution UI consistency

(function () {
  "use strict";

  function readExecutionState(root) {
    return {
      hasSession: root.dataset.hasSession === "1",
      canEdit: root.dataset.canEdit === "1",
      canFinalize: root.dataset.canFinalize === "1",
    };
  }

  function setReadOnly(root, isReadOnly) {
    // Escopo: somente área de execução (root) — consistente com data-skip-readonly
    root.querySelectorAll("input, select, textarea, button").forEach((el) => {
      if (el.closest("[data-skip-readonly]")) return;
      el.disabled = isReadOnly;
    });
  }

  function refreshItemBipadoFromInputs(itemEl) {
    const hasAtivo = !!itemEl
      .querySelector("input[name^='ativo_']")
      ?.value?.trim();
    const hasSerie = !!itemEl
      .querySelector("input[name^='serie_']")
      ?.value?.trim();
    const confirmado = !!itemEl.querySelector(
      "input[type='checkbox'][name^='confirmado_']",
    )?.checked;

    // Heurística: se tiver inputs de ativo/serie, é item rastreável
    const isRastreavel = !!itemEl.querySelector(
      "input[name^='ativo_'], input[name^='serie_']",
    );

    itemEl.dataset.itemBipado =
      (isRastreavel ? hasAtivo || hasSerie : confirmado) ? "1" : "0";
  }

  function applyItemState(root, state) {
    const isGlobalReadOnly = !state.hasSession || !state.canEdit;

    root.querySelectorAll("[data-item-root='1']").forEach((itemEl) => {
      const isBipado = itemEl.dataset.itemBipado === "1";
      const isEditing = itemEl.dataset.itemEditing === "1";

      // Item read-only quando:
      // - global read-only OU
      // - item está bipado e não está em modo editar
      const itemReadOnly = isGlobalReadOnly || (isBipado && !isEditing);

      itemEl.querySelectorAll("input, select, textarea, button").forEach((el) => {
        if (el.closest("[data-skip-readonly]")) return;

        // botão de toggle precisa ficar clicável
        if (el.matches("[data-item-edit-toggle]")) return;

        el.disabled = itemReadOnly;
      });

      // UI helpers (opcional)
      itemEl.classList.toggle("is-item-readonly", itemReadOnly);
      itemEl.classList.toggle("is-item-editing", isEditing);

      const toggleBtn = itemEl.querySelector("[data-item-edit-toggle]");
      if (toggleBtn) {
        // só faz sentido quando bipado
        toggleBtn.hidden = !isBipado;
        toggleBtn.setAttribute("aria-pressed", isEditing ? "true" : "false");
        toggleBtn.textContent = isEditing ? "Bloquear item" : "Editar item";
      }
    });
  }

  function applyExecutionState() {
    const root = document.getElementById("execution-root");
    if (!root) return;

    const state = readExecutionState(root);

    // Regra global: sem sessão OU sem permissão de editar => read-only
    const isReadOnly = !state.hasSession || !state.canEdit;

    // Global
    setReadOnly(root, isReadOnly);

    // Per-item (ISSUE #73)
    applyItemState(root, state);
  }

  function initExecutionState() {
    applyExecutionState();
  }

  // Boot
  document.addEventListener("DOMContentLoaded", initExecutionState);

  // Permite que outros scripts disparem reaplicação sem acoplamento direto
  document.addEventListener("execucao:apply-state", applyExecutionState);

  // Atualiza "bipado" dinamicamente quando usuário clica em salvar execução
  function markItemsBipadoFromInputs(root) {
    root.querySelectorAll("[data-item-root='1']").forEach((itemEl) => {
      refreshItemBipadoFromInputs(itemEl);
    });
  }

    // Chamado apenas quando salvar execução (ISSUE #73 fix)
    document.addEventListener("execucao:mark-items-bipado", () => {
      const root = document.getElementById("execution-root");
      if (!root) return;
      markItemsBipadoFromInputs(root);
    });
  // Toggle de modo editar por item
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-item-edit-toggle]");
    if (!btn) return;

    const itemEl = btn.closest("[data-item-root='1']");
    if (!itemEl) return;

    // Só alterna se item estiver bipado
    if (itemEl.dataset.itemBipado !== "1") return;

    itemEl.dataset.itemEditing = itemEl.dataset.itemEditing === "1" ? "0" : "1";
    document.dispatchEvent(new CustomEvent("execucao:apply-state"));
  });
})();