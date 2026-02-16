/**
 * @jest-environment jsdom
 */

describe("execution_state - lock parcial (readonly apenas em campos preenchidos)", () => {
  beforeEach(() => {
    jest.resetModules();

    document.body.innerHTML = `
      <div
        id="execution-root"
        data-has-session="0"
        data-can-edit="0"
        data-can-finalize="0"
      >
        <!-- Itens -->
        <div data-item-root="1" data-item-id="101">
          <input name="ativo_101" value="ATV-999" />
          <input name="serie_101" value="" />
          <input type="checkbox" name="confirmado_101" />
        </div>

        <div data-item-root="1" data-item-id="202">
          <input name="ativo_202" value="" />
          <input name="serie_202" value="SN-202" />
          <input type="checkbox" name="confirmado_202" checked />
        </div>

        <!-- fiscais -->
        <input id="contab" name="contabilidade_numero" value="PED-001" />
        <input id="nf" name="nf_saida_numero" value="" />

        <button id="btn-a">A</button>
      </div>
    `;
  });

  test("sem sessão: preenchidos travam; vazios permanecem editáveis", () => {
    require("../js/execution_state.js");

    // aplica estado via evento (contrato do PR6 Extra)
    document.dispatchEvent(new CustomEvent("execucao:apply-state"));

    const ativo101 = document.querySelector('input[name="ativo_101"]');
    const serie101 = document.querySelector('input[name="serie_101"]');
    const conf101 = document.querySelector('input[name="confirmado_101"]');

    const ativo202 = document.querySelector('input[name="ativo_202"]');
    const serie202 = document.querySelector('input[name="serie_202"]');
    const conf202 = document.querySelector('input[name="confirmado_202"]');

    const contab = document.getElementById("contab");
    const nf = document.getElementById("nf");

    // preenchidos -> travados
    expect(ativo101.readOnly).toBe(true);
    expect(serie202.readOnly).toBe(true);
    expect(conf202.disabled).toBe(true);

    // vazios -> editáveis
    expect(serie101.readOnly).toBe(false);
    expect(ativo202.readOnly).toBe(false);
    expect(conf101.disabled).toBe(false);

    // fiscais: preenchido trava, vazio libera
    expect(contab.readOnly).toBe(true);
    expect(nf.readOnly).toBe(false);
  });
});