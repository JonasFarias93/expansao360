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
   * Bootstraps state reading (no UI mutation yet).
   */
  function initExecutionState() {
    const root = document.getElementById("execution-root");
    if (!root) return;

    const state = readExecutionState(root);

    // MT-70.3: read only (no UI changes yet)
    console.debug("[execucao] execution state:", state);
  }

  document.addEventListener("DOMContentLoaded", initExecutionState);
})();