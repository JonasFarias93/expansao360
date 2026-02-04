/**
 * @jest-environment jsdom
 */

describe("tipos_formset (kit) - equipamento -> tipos", () => {
  let jsonMock;

  beforeEach(() => {
    jest.resetModules();

    document.body.innerHTML = `
      <div id="itens-container" data-tipos-url="/cadastro/ajax/tipos-por-equipamento/">
        <div class="border">
          <select name="form-0-equipamento">
            <option value="">---------</option>
            <option value="1">Equip 1</option>
          </select>
          <select name="form-0-tipo"></select>
        </div>
      </div>
    `;

    jsonMock = jest.fn().mockResolvedValue([{ id: 10, nome: "LCD" }]);

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: jsonMock,
    });

    jest.spyOn(console, "log").mockImplementation(() => {});
    jest.spyOn(console, "error").mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it("popula o select de tipo quando muda o equipamento", async () => {
    require("../tipos_formset.js");

    expect(window.__cadastro__?.initTiposFormset).toBeDefined();
    window.__cadastro__.initTiposFormset();

    const equipamento = document.querySelector('select[name="form-0-equipamento"]');
    const tipo = document.querySelector('select[name="form-0-tipo"]');

    equipamento.value = "1";
    equipamento.dispatchEvent(new Event("change", { bubbles: true }));

    expect(global.fetch).toHaveBeenCalled();

    // flush macrotasks (fetch -> await resp.json -> append options)
    const flush = () => new Promise((r) => setTimeout(r, 0));
    await flush();
    await flush();

    expect(jsonMock).toHaveBeenCalled();

    const opts = [...tipo.querySelectorAll("option")].map((o) => o.textContent);
    expect(opts).toEqual(["---------", "LCD"]);
  });
});
