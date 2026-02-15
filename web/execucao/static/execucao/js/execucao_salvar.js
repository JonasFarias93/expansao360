// web/execucao/static/execucao/js/execucao_salvar.js
/**
 * Usado em:
 * - web/chamados/templates/execucao/chamado_execucao.html
 *
 * Responsabilidade:
 * - Enviar POST de "Salvar execução" via AJAX e atualizar feedback de UI (status "Salvo...").
 * - NÃO deve gerenciar estado global de tela (isso será centralizado pelo state manager na PR6).
 *
 * Pré-requisitos DOM:
 * - IDs: btn-salvar-execucao, salvar-status (opcional), execucao-container (opcional), abrir-para-continuar (opcional)
 * - data-attrs: data-url em #btn-salvar-execucao
 * - Cookie: csrftoken
 *
 * Observações:
 * - Carregado via <script defer> no template de página.
 * - Não deve ser importado por componentes/parciais.
 */
(function () {
  const btn = document.getElementById("btn-salvar-execucao");
  if (!btn) return;

  const statusEl = document.getElementById("salvar-status");
  const url = btn.dataset.url;

  const LABEL_DEFAULT = btn.textContent?.trim() || "Salvar execução";

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift() || null;
    return null;
  }

  function setStatus(text) {
    if (!statusEl) return;
    statusEl.textContent = text;
  }

  function setReadOnly() {
    // Deixa a tela read-only desabilitando inputs do fluxo de execução.
    const container = document.getElementById("execucao-container") || document;

    container
      .querySelectorAll("input, select, textarea, button")
      .forEach((el) => {
        // manter CTA de abrir e o próprio botão de salvar
        if (el.id === "btn-abrir-para-continuar") return;
        if (el.id === "btn-salvar-execucao") return;

        if (el.closest("[data-skip-readonly]")) return;

        el.disabled = true;
      });
  }

  function showAbrirParaContinuar() {
    const placeholder = document.getElementById("abrir-para-continuar");
    if (placeholder) placeholder.classList.remove("hidden");
  }

  function collectPayload() {
    // Persistimos fiscais aqui porque o endpoint aceita isso.
    // Itens já são persistidos no fluxo atual (inputs salvam em endpoints próprios),
    // então o "Salvar execução" consolida status + encerra sessão.
    const cont =
      document.querySelector('input[name="contabilidade_numero"]')?.value ?? "";
    const nf =
      document.querySelector('input[name="nf_saida_numero"]')?.value ?? "";

    const formData = new FormData();
    formData.append("contabilidade_numero", cont);
    formData.append("nf_saida_numero", nf);
    return formData;
  }

  async function doSave() {
    const csrf = getCookie("csrftoken");
    if (!csrf) {
      throw new Error("CSRF token ausente.");
    }

    const resp = await fetch(url, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf,
      },
      body: collectPayload(),
    });

    if (!resp.ok) {
      // 403 => sem sessão/cap, 400 => form inválido etc.
      throw new Error(`Falha ao salvar (${resp.status})`);
    }

    // endpoint retorna JSON no modo AJAX
    const data = await resp.json();
    if (!data || data.ok !== true) {
      throw new Error("Resposta inválida do servidor.");
    }
    return data;
  }

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Salvando…";
    setStatus("");

    try {
      const data = await doSave();

      const hhmm = data.saved_at || "";
      btn.textContent = LABEL_DEFAULT;
      setStatus(hhmm ? `Salvo às ${hhmm}` : "Salvo");

      // entra em read-only SEM bloquear ações finais
      setReadOnly();
      showAbrirParaContinuar();
    } catch (err) {
      btn.disabled = false;
      btn.textContent = LABEL_DEFAULT;
      setStatus("Erro ao salvar. Tente novamente.");
      // console.error(err);
    }
  });
})();