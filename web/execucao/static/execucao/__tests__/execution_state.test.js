/**
 * @jest-environment jsdom
 */

/**
 * DOM tests for execution_state.js (ISSUE #74)
 *
 * These tests validate execution UI state transitions via data-* contract.
 * They use jsdom and the test hook window.__executionState.
 */

describe("execution_state DOM transitions", () => {
  function mountDOM({ hasSession, canEdit, canFinalize }) {
    document.body.innerHTML = `
      <div id="execution-root"
           data-has-session="${hasSession}"
           data-can-edit="${canEdit}"
           data-can-finalize="${canFinalize}">
        <button id="btn-a">A</button>
        <button id="btn-b">B</button>
        <input id="field-x" />
      </div>
    `;
  }

  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = "";
  });

  test("Sem sessão → botões desabilitados", () => {
    mountDOM({ hasSession: "0", canEdit: "0", canFinalize: "0" });

    // Load script (executes IIFE and registers window.__executionState in test env)
    require("../js/execution_state");

    window.__executionState.applyExecutionState();

    expect(document.getElementById("btn-a").disabled).toBe(true);
    expect(document.getElementById("btn-b").disabled).toBe(true);
    expect(document.getElementById("field-x").disabled).toBe(true);
  });

  test("Com sessão → botões habilitados", () => {
    mountDOM({ hasSession: "1", canEdit: "1", canFinalize: "0" });

    require("../js/execution_state");

    window.__executionState.applyExecutionState();

    expect(document.getElementById("btn-a").disabled).toBe(false);
    expect(document.getElementById("btn-b").disabled).toBe(false);
    expect(document.getElementById("field-x").disabled).toBe(false);
  });

  test("Reabrir sessão → habilita novamente", () => {
    mountDOM({ hasSession: "0", canEdit: "0", canFinalize: "0" });

    require("../js/execution_state");

    // 1) sem sessão => read-only
    window.__executionState.applyExecutionState();
    expect(document.getElementById("btn-a").disabled).toBe(true);

    // 2) "reabrir sessão" => atualizar contrato data-* e reaplicar
    const root = document.getElementById("execution-root");
    root.dataset.hasSession = "1";
    root.dataset.canEdit = "1";

    // Via evento (forma oficial do app)
    document.dispatchEvent(new CustomEvent("execucao:apply-state"));

    expect(document.getElementById("btn-a").disabled).toBe(false);
    expect(document.getElementById("btn-b").disabled).toBe(false);
    expect(document.getElementById("field-x").disabled).toBe(false);
  });
});