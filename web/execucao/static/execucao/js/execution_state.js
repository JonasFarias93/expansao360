// execution_state.js
// Responsibility: Centralized execution UI state manager
// Used in: chamado_execucao.html
// Scope: PR6 Extra — Execution UI consistency

(function () {
  "use strict";

  const ROOT_ID = "execution-root";

  function _root() {
    return document.getElementById(ROOT_ID);
  }

  function _asBool(value) {
    // Contract today: "1" | "0"
    // Accept some future-safe variants too
    return value === "1" || value === "true" || value === "True";
  }

  /**
   * Reads execution state from DOM dataset.
   * Source of truth: #execution-root data-* attributes
   */
  function getExecutionState() {
    const root = _root();
    if (!root) return null;

    return {
      hasSession: _asBool(root.dataset.hasSession),
      canEdit: _asBool(root.dataset.canEdit),
      canFinalize: _asBool(root.dataset.canFinalize),
    };
  }

  // Stub only — logic will be implemented in next micro-task
  function initExecutionState() {
    const state = getExecutionState();
    if (!state) return;

    // TODO(MT-71): applyExecutionState(state)
    if (window.DEBUG_EXECUCAO_STATE === true) {
      console.debug("[execucao] execution state loaded:", state);
    }
  }

  // Optional: expose for tests / next tasks
  window.ExecutionState = {
    get: getExecutionState,
    init: initExecutionState,
  };

  document.addEventListener("DOMContentLoaded", initExecutionState);
})();