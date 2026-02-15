// execution_state.js
// Responsibility: Centralized execution UI state manager
// Used in: chamado_execucao.html
// Scope: PR6 Extra — Execution UI consistency

(function () {
  "use strict";

  /**
   * Reads execution state from DOM dataset.
   * Source of truth: #execution-root data-* attributes
   */
  function getExecutionState() {
    const root = document.getElementById("execution-root");
    if (!root) return null;

    return {
      hasSession: root.dataset.hasSession === "1",
      canEdit: root.dataset.canEdit === "1",
      canFinalize: root.dataset.canFinalize === "1",
    };
  }

  // Stub only — logic will be implemented in next micro-task
  function initExecutionState() {
    const state = getExecutionState();
    if (!state) return;

    // TODO: applyExecutionState(state)
    console.debug("Execution state loaded:", state);
  }

  document.addEventListener("DOMContentLoaded", initExecutionState);
})();