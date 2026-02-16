/**
 * @jest-environment jsdom
 */

describe("execution_state DOM transitions", () => {
  beforeEach(() => {
    jest.resetModules();

    document.body.innerHTML = `
      <div id="execution-root" data-has-session="0" data-can-edit="0" data-can-finalize="0">
        <button id="btn-a">A</button>
        <button id="btn-b">B</button>
        <input id="field-x" value="X" />
      </div>
    `;
  });

  test("Sem sessão → botões desabilitados e campos preenchidos travados", () => {
    require("../js/execution_state.js");
    document.dispatchEvent(new CustomEvent("execucao:apply-state"));

    expect(document.getElementById("btn-a").disabled).toBe(true);
    expect(document.getElementById("btn-b").disabled).toBe(true);

    // lock parcial: input preenchido => readOnly (não necessariamente disabled)
    expect(document.getElementById("field-x").readOnly).toBe(true);
  });

  test("Com sessão → botões habilitados e campos liberados", () => {
    // atualiza contrato
    const root = document.getElementById("execution-root");
    root.dataset.hasSession = "1";
    root.dataset.canEdit = "1";

    require("../js/execution_state.js");
    document.dispatchEvent(new CustomEvent("execucao:apply-state"));

    expect(document.getElementById("btn-a").disabled).toBe(false);
    expect(document.getElementById("btn-b").disabled).toBe(false);

    expect(document.getElementById("field-x").readOnly).toBe(false);
    expect(document.getElementById("field-x").disabled).toBe(false);
  });
});