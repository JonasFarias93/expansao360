// execution_state.js
// Responsibility: Centralized execution UI state manager
// Used in: chamado_execucao.html

(function () {
  "use strict";

  function shouldSkipReadOnly(el) {
    return !!el?.closest?.("[data-skip-readonly]");
  }

  function isHiddenInput(el) {
    if (!el) return false;
    const tag = (el.tagName || "").toLowerCase();
    if (tag !== "input") return false;
    const type = (el.getAttribute("type") || "").toLowerCase();
    return type === "hidden";
  }

  function readExecutionState(root) {
    return {
      hasSession: root.dataset.hasSession === "1",
      canEdit: root.dataset.canEdit === "1",
      canFinalize: root.dataset.canFinalize === "1",
    };
  }

  function isFilledInput(el) {
    if (!el) return false;

    const tag = (el.tagName || "").toLowerCase();
    const type = (el.getAttribute("type") || "").toLowerCase();

    if (tag === "textarea") return (el.value || "").trim().length > 0;
    if (tag === "select") return (el.value || "").trim().length > 0;
    if (type === "checkbox" || type === "radio") return !!el.checked;

    return (el.value || "").trim().length > 0;
  }

  function applyPartialLock(root, state) {
    const isGlobalReadOnly = !state.hasSession || !state.canEdit;
    if (!isGlobalReadOnly) return;

    root.querySelectorAll("input, textarea, select").forEach((el) => {
      if (shouldSkipReadOnly(el)) return;
      // ✅ nunca mexer em hidden (CSRF e outros contratos)
      if (isHiddenInput(el)) return;

      const filled = isFilledInput(el);

      const tag = (el.tagName || "").toLowerCase();
      const type = (el.getAttribute("type") || "").toLowerCase();

      if (tag === "select" || type === "checkbox" || type === "radio") {
        el.disabled = filled;
      } else {
        el.readOnly = filled;
      }
    });

    // Botões sempre desabilitados sem sessão
    root.querySelectorAll("button").forEach((btn) => {
      if (shouldSkipReadOnly(btn)) return;
      btn.disabled = true;
    });
  }

  function applyFullLock(root, isReadOnly) {
    if (!isReadOnly) {
      root.querySelectorAll("input, textarea, select, button").forEach((el) => {
        if (shouldSkipReadOnly(el)) return;
        // ✅ hidden nunca deve ser alterado
        if (isHiddenInput(el)) return;

        el.disabled = false;
        el.readOnly = false;
      });
      return;
    }
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

    const isRastreavel = !!itemEl.querySelector(
      "input[name^='ativo_'], input[name^='serie_']",
    );

    itemEl.dataset.itemBipado =
      (isRastreavel ? hasAtivo || hasSerie : confirmado) ? "1" : "0";
  }

  function applyItemState(root, state) {
    if (!state.hasSession || !state.canEdit) return;

    root.querySelectorAll("[data-item-root='1']").forEach((itemEl) => {
      const isBipado = itemEl.dataset.itemBipado === "1";
      const isEditing = itemEl.dataset.itemEditing === "1";

      const itemReadOnly = isBipado && !isEditing;

      itemEl
        .querySelectorAll("input, select, textarea, button")
        .forEach((el) => {
          if (shouldSkipReadOnly(el)) return;
          if (isHiddenInput(el)) return; // ✅ proteger CSRF/hidden dentro de item
          if (el.matches("[data-item-edit-toggle]")) return;

          el.disabled = itemReadOnly;
        });

      const toggleBtn = itemEl.querySelector("[data-item-edit-toggle]");
      if (toggleBtn) {
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
    const isReadOnly = !state.hasSession || !state.canEdit;

    applyFullLock(root, isReadOnly);
    applyPartialLock(root, state);
    applyItemState(root, state);
  }

  document.addEventListener("DOMContentLoaded", applyExecutionState);
  document.addEventListener("execucao:apply-state", applyExecutionState);

  document.addEventListener("execucao:mark-items-bipado", () => {
    const root = document.getElementById("execution-root");
    if (!root) return;
    root.querySelectorAll("[data-item-root='1']").forEach((itemEl) => {
      refreshItemBipadoFromInputs(itemEl);
    });
  });

  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-item-edit-toggle]");
    if (!btn) return;

    const itemEl = btn.closest("[data-item-root='1']");
    if (!itemEl) return;

    if (itemEl.dataset.itemBipado !== "1") return;

    itemEl.dataset.itemEditing =
      itemEl.dataset.itemEditing === "1" ? "0" : "1";

    document.dispatchEvent(new CustomEvent("execucao:apply-state"));
  });

  if (
    typeof process !== "undefined" &&
    process.env &&
    process.env.NODE_ENV === "test"
  ) {
    window.__executionState = {
      applyExecutionState,
      readExecutionState,
    };
  }
})();