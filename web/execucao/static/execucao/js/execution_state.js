// execution_state.js
// Responsibility: Centralized execution UI state manager
// Used in: chamado_execucao.html
// Scope: PR6 Extra — Execution UI consistency

(function () {
  "use strict";

  /**
   * Reads execution state from DOM dataset.
   * Contract source: #execution-root data-* attributes
   */
  function readExecutionState(root) {
    return {
      hasSession: root.dataset.hasSession === "1",
      canEdit: root.dataset.canEdit === "1",
      canFinalize: root.dataset.canFinalize === "1",
    };
  }

  /**
   * Idempotent state applier (no UI mutation yet).
   * Safe to call multiple times.
   */
  function applyExecutionState() {
    const root = document.getElementById("execution-root");
    if (!root) return;

    const state = readExecutionState(root);

    // Intentionally no DOM mutations in MT-70.4
    console.debug("[execucao] applyExecutionState (skeleton):", state);
  }

  /**
   * Bootstrap
   */
  function initExecutionState() {
    applyExecutionState();
  }

  document.addEventListener("DOMContentLoaded", initExecutionState);
})();