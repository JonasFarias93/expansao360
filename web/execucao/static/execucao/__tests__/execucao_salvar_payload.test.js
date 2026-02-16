/**
 * @jest-environment jsdom
 */

function formDataToObject(fd) {
  const obj = {};
  for (const [k, v] of fd.entries()) obj[k] = String(v);
  return obj;
}

describe("Salvar execução (AJAX) - contrato mínimo de payload", () => {
  beforeEach(() => {
    jest.resetModules();

    document.body.innerHTML = `
      <div id="execution-root" data-has-session="1" data-can-edit="1" data-can-finalize="0">
        <input name="contabilidade_numero" value="PED-001" />
        <input name="nf_saida_numero" value="" />

        <!-- Itens na tela -->
        <input name="ativo_101" value="ATV-999" />
        <input name="serie_101" value="SN-999" />
        <input type="checkbox" name="confirmado_202" checked />

        <button id="btn-salvar-execucao" data-url="/fake-url">Salvar execução</button>
        <div id="salvar-status"></div>
        <div id="abrir-para-continuar" class="hidden"></div>
      </div>
    `;

    // CSRF exigido pelo script
    document.cookie = "csrftoken=TESTTOKEN";

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true, saved_at: "10:10" }),
    });
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  test("deve incluir ativo_/serie_/confirmado_ no payload quando inputs existirem no DOM", async () => {
    // Importa o IIFE (bind do click acontece aqui)
    require("../js/chamado_salvar_execucao_ajax.js");

    document.getElementById("btn-salvar-execucao").click();

    // aguarda execução do handler async + fetch
    await Promise.resolve();

    expect(global.fetch).toHaveBeenCalledTimes(1);

    const [, options] = global.fetch.mock.calls[0];
    expect(options).toBeTruthy();
    expect(options.method).toBe("POST");

    const payload = formDataToObject(options.body);

    // fiscais (sempre)
    expect(payload.contabilidade_numero).toBe("PED-001");
    expect(payload).toHaveProperty("nf_saida_numero");

    // itens (contrato mínimo)
    expect(payload.ativo_101).toBe("ATV-999");
    expect(payload.serie_101).toBe("SN-999");

    // checkbox: se checked, deve enviar confirmado_<id> (valor pode variar)
    expect(payload).toHaveProperty("confirmado_202");
  });
});