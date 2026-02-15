/**
 * @jest-environment jsdom
 */

describe("execution_state per-item edit mode", () => {
  function mountDOM() {
    document.body.innerHTML = `
      <div id="execution-root"
           data-has-session="1"
           data-can-edit="1"
           data-can-finalize="0">

        <div data-item-root="1" data-item-id="1" data-item-bipado="1" data-item-editing="0">
          <button type="button" data-item-edit-toggle="1">Editar item</button>
          <input id="item1-field" />
        </div>

        <div data-item-root="1" data-item-id="2" data-item-bipado="1" data-item-editing="0">
          <button type="button" data-item-edit-toggle="1">Editar item</button>
          <input id="item2-field" />
        </div>

      </div>
    `;
  }

  beforeEach(() => {
    jest.resetModules();
    document.body.innerHTML = "";
    delete window.__executionState;
  });

  test("Bipado → read-only; clique editar → libera só aquele; outro permanece travado", () => {
    mountDOM();

    // Carrega o state manager (IIFE registra listeners + test hook)
    require("../js/execution_state.js");

    // Estado inicial: ambos bipados e editing=0 => travados
    window.__executionState.applyExecutionState();

    expect(document.getElementById("item1-field").disabled).toBe(true);
    expect(document.getElementById("item2-field").disabled).toBe(true);

    // Toggle item 1
    const item1Toggle = document
      .querySelector("[data-item-id='1']")
      .querySelector("[data-item-edit-toggle]");

    item1Toggle.click(); // click handler no execution_state deve alternar editing e reaplicar

    // Item 1 liberado, item 2 continua travado
    expect(document.getElementById("item1-field").disabled).toBe(false);
    expect(document.getElementById("item2-field").disabled).toBe(true);
  });
});