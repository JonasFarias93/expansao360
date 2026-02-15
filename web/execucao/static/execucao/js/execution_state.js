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

  function applyExecutionState() {
    const root = document.getElementById("execution-root");
    if (!root) return;

    const state = readExecutionState(root);

    // Regra global: sem sessão OU sem permissão de editar => read-only
    const isReadOnly = !state.hasSession || !state.canEdit;

    setReadOnly(root, isReadOnly);

    // TODO(PR6): ações finais e toggles específicos virão depois
    // (sem lógica espalhada em outros JS)
  }

  function initExecutionState() {
    applyExecutionState();
  }

  document.addEventListener("DOMContentLoaded", initExecutionState);

  // Permite que outros scripts disparem reaplicação sem acoplamento direto
  document.addEventListener("execucao:apply-state", applyExecutionState);
})();