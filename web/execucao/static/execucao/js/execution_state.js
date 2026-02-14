(function () {
  function getRoot() {
    return document.getElementById("execucao-container") || document;
  }

  function readState(root) {
    const el = root.getElementById
      ? root.getElementById("execucao-root")
      : document.getElementById("execucao-root");

    // fallback: se ainda não existe execucao-root, tenta no container
    const host = el || document.getElementById("execucao-container") || document.body;

    const ds = host?.dataset || {};
    return {
      hasSession: ds.hasSession === "1",
      canEdit: ds.canEdit === "1",
      canFinalize: ds.canFinalize === "1",
    };
  }

  function setReadOnly(root, isReadOnly) {
    const container = document.getElementById("execucao-container") || document;

    // regra: tudo que for "editável" precisa estar dentro de um wrapper identificável
    // se não tiver isso ainda, mantém o comportamento por seletor mas com allowlist.
    container
      .querySelectorAll("input, select, textarea")
      .forEach((el) => {
        if (el.closest("[data-skip-readonly]")) return;
        el.disabled = isReadOnly;
      });
  }

  function toggleActionButtons(state) {
    // Exemplo mínimo: botão salvar deve seguir canEdit
    const btnSave = document.getElementById("btn-salvar-execucao");
    if (btnSave) btnSave.disabled = !state.canEdit;

    // CTA abrir-para-continuar aparece quando NÃO tem sessão
    const abrir = document.getElementById("abrir-para-continuar");
    if (abrir) abrir.classList.toggle("hidden", state.hasSession);

    // (opcional) finalize button
    const btnFinalizar = document.getElementById("btn-finalizar");
    if (btnFinalizar) btnFinalizar.disabled = !state.canFinalize;
  }

  function applyExecutionState() {
    const root = getRoot();
    const state = readState(root);

    // idempotente: sempre recalcula
    setReadOnly(root, !state.canEdit);
    toggleActionButtons(state);
  }

  // expõe API global simples (sem bundler)
  window.ExecutionState = {
    apply: applyExecutionState,
    read: () => readState(getRoot()),
  };

  document.addEventListener("DOMContentLoaded", () => {
    applyExecutionState();
  });
})();