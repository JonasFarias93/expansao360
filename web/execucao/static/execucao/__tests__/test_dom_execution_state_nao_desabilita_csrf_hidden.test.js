/** @jest-environment jsdom */
/**
 * Contrato: applyExecutionState() nunca pode desabilitar inputs hidden.
 * Motivo: CSRF token é hidden e deve ser enviado sempre no submit.
 */

// garante que o guard do execution_state exponha window.__executionState
process.env.NODE_ENV = "test";

// IMPORTANT: carregar o script (IIFE) que registra handlers e expõe __executionState
require("../js/execution_state.js");

function mountDOM({ hasSession = "0", canEdit = "0" } = {}) {
  document.body.innerHTML = `
    <div id="execution-root"
         data-has-session="${hasSession}"
         data-can-edit="${canEdit}"
         data-can-finalize="0">
      <form id="form-evidencias" method="post" enctype="multipart/form-data">
        <input type="hidden" name="csrfmiddlewaretoken" value="TOKEN123" />
        <select name="tipo">
          <option value="OUTRO">Outro</option>
        </select>
        <input type="file" name="arquivo" />
        <button type="submit">Enviar Evidência</button>
      </form>
    </div>
  `;
}

describe("execution_state - CSRF hidden", () => {
  test("test_dado_readonly_quando_applyExecutionState_entao_nao_desabilita_csrf_hidden", () => {
    mountDOM({ hasSession: "0", canEdit: "0" });

    expect(window.__executionState).toBeTruthy();
    window.__executionState.applyExecutionState();

    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
    expect(csrf).toBeTruthy();
    expect(csrf.disabled).toBe(false);

    const select = document.querySelector('select[name="tipo"]');
    expect(select.disabled).toBe(true);
  });

  test("test_dado_editavel_quando_applyExecutionState_entao_nao_desabilita_csrf_hidden", () => {
    mountDOM({ hasSession: "1", canEdit: "1" });

    expect(window.__executionState).toBeTruthy();
    window.__executionState.applyExecutionState();

    const csrf = document.querySelector('input[name="csrfmiddlewaretoken"]');
    expect(csrf).toBeTruthy();
    expect(csrf.disabled).toBe(false);
  });
});