/**
 * @jest-environment jsdom
 */
describe("chamado_salvar_execucao_ajax.js lifecycle", () => {
  const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));

  beforeEach(() => {
    document.body.innerHTML = `
      <div id="execution-root" data-has-session="1" data-can-edit="1"></div>
      <button id="btn-salvar-execucao" data-url="/fake/save">Salvar execução</button>
      <div id="salvar-status"></div>
    `;

    Object.defineProperty(document, "cookie", {
      writable: true,
      value: "csrftoken=abc123",
    });

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ ok: true, saved_at: "10:10" }),
    });

    jest.resetModules();
    require("../js/chamado_salvar_execucao_ajax.js");
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test("apos salvar, nao deve zerar data-has-session nem data-can-edit", async () => {
    const root = document.getElementById("execution-root");
    const btn = document.getElementById("btn-salvar-execucao");

    expect(root.dataset.hasSession).toBe("1");
    expect(root.dataset.canEdit).toBe("1");

    btn.click();
    await flushPromises();
    await flushPromises(); // ✅ garante fetch + json + handler concluídos

    expect(root.dataset.hasSession).toBe("1");
    expect(root.dataset.canEdit).toBe("1");
  });

  test("apos salvar, botao volta a habilitar", async () => {
    const btn = document.getElementById("btn-salvar-execucao");

    btn.click();
    await flushPromises();
    await flushPromises(); // ✅ idem

    expect(btn.disabled).toBe(false);
    expect(btn.textContent).toBe("Salvar execução");
  });
});