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
    jest.resetModules(); // importante: script é IIFE, precisa reexecutar a cada teste

    document.body.innerHTML = `
      <div id="execution-root" data-has-session="1" data-can-edit="1"></div>

      <input name="contabilidade_numero" value="PED-001" />
      <input name="nf_saida_numero" value="" />

      <!-- Itens na tela (contrato esperado) -->
      <input name="ativo_101" value="ATV-999" />
      <input name="serie_101" value="SN-999" />
      <input type="checkbox" name="confirmado_202" checked />

      <button id="btn-salvar-execucao" data-url="/fake-url">Salvar execução</button>
      <div id="salvar-status"></div>
      <div id="abrir-para-continuar" class="hidden"></div>
    `;

    // CSRF exigido pelo script
    document.cookie = "csrftoken=TESTTOKEN";

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true, saved_at: "10:10" }),
    });
  });

  test("deve incluir ativo_/serie_/confirmado_ no payload quando inputs existirem no DOM", async () => {
    // Importa o IIFE (bind do click acontece aqui)
    require("../js/execucao_salvar.js"); // ajuste se seu path do jest for diferente

    document.getElementById("btn-salvar-execucao").click();

    // aguarda o microtask da promise do click handler
    await Promise.resolve();

    expect(global.fetch).toHaveBeenCalledTimes(1);

    const [, options] = global.fetch.mock.calls[0];
    const payload = formDataToObject(options.body);

    // fiscais (sempre)
    expect(payload.contabilidade_numero).toBe("PED-001");
    expect(payload).toHaveProperty("nf_saida_numero");

    // contrato mínimo: itens presentes na tela => devem ir no payload
    expect(payload.ativo_101).toBe("ATV-999"); // <-- FALHA HOJE (bug reproduzido)
    expect(payload.serie_101).toBe("SN-999");  // <-- FALHA HOJE

    // checkbox: se checked, deve enviar confirmado_<id> (valor pode variar)
    expect(payload).toHaveProperty("confirmado_202"); // <-- FALHA HOJE
  });
});