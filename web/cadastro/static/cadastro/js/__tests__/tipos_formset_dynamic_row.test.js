/**
 * @jest-environment jsdom
 */

describe("tipos_formset (kit) - funciona em linha adicionada depois", () => {
  let jsonMock;

  beforeEach(() => {
    jest.resetModules();

    document.body.innerHTML = `
      <div id="itens-container" data-tipos-url="/cadastro/ajax/tipos-por-equipamento/"></div>
    `;

    jsonMock = jest.fn().mockResolvedValue([{ id: 10, nome: "LCD" }]);
    global.fetch = jest.fn().mockResolvedValue({ ok: true, json: jsonMock });

    jest.spyOn(console, "log").mockImplementation(() => {});
    jest.spyOn(console, "error").mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it("popula tipo ao trocar equipamento em linha adicionada dinamicamente", async () => {
    require("../tipos_formset.js");
    window.__cadastro__.initTiposFormset();

    const container = document.getElementById("itens-container");

    // adiciona linha "depois" (simulando o kits_formset)
    container.innerHTML = `
      <div class="border">
        <select name="form-1-equipamento">
          <option value="">---------</option>
          <option value="1">Equip 1</option>
        </select>
        <select name="form-1-tipo"></select>
      </div>
    `;

    const equipamento = container.querySelector('select[name="form-1-equipamento"]');
    const tipo = container.querySelector('select[name="form-1-tipo"]');

    equipamento.value = "1";
    equipamento.dispatchEvent(new Event("change", { bubbles: true }));

    const flush = () => new Promise((r) => setTimeout(r, 0));
    await flush();
    await flush();

    const opts = [...tipo.querySelectorAll("option")].map((o) => o.textContent);
    expect(opts).toEqual(["---------", "LCD"]);
  });
});
