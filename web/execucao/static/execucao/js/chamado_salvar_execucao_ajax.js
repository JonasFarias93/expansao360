// web/execucao/static/execucao/js/execucao_salvar.js
/**
 * Usado em:
 * - web/chamados/templates/execucao/chamado_execucao.html
 *
 * Responsabilidade:
 * - Enviar POST de "Salvar execução" via AJAX e atualizar feedback de UI (status "Salvo...").
 * - NÃO deve gerenciar estado global de tela (centralizado pelo state manager).
 *
 * Pré-requisitos DOM:
 * - IDs: btn-salvar-execucao, salvar-status (opcional), abrir-para-continuar (opcional), execution-root
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

  function showAbrirParaContinuar() {
    const placeholder = document.getElementById("abrir-para-continuar");
    if (placeholder) placeholder.classList.remove("hidden");
  }

  function collectPayload() {
    // Contrato do payload:
    // - Sempre: contabilidade_numero, nf_saida_numero
    // - Quando existirem inputs de itens no DOM: ativo_<id>, serie_<id>, confirmado_<id> (se marcado)
    const cont =
      document.querySelector('input[name="contabilidade_numero"]')?.value ?? "";
    const nf =
      document.querySelector('input[name="nf_saida_numero"]')?.value ?? "";

    const formData = new FormData();
    formData.append("contabilidade_numero", cont);
    formData.append("nf_saida_numero", nf);

    // Itens rastreáveis (Ativo / Série)
    document.querySelectorAll('input[name^="ativo_"]').forEach((el) => {
      const name = el.getAttribute("name");
      if (!name) return;
      formData.append(name, el.value ?? "");
    });

    document.querySelectorAll('input[name^="serie_"]').forEach((el) => {
      const name = el.getAttribute("name");
      if (!name) return;
      formData.append(name, el.value ?? "");
    });

    // Itens contáveis (Confirmado) — enviar somente se marcado
    document.querySelectorAll('input[name^="confirmado_"]').forEach((el) => {
      const name = el.getAttribute("name");
      if (!name) return;

      if (el.type === "checkbox" || el.type === "radio") {
        if (!el.checked) return;
        formData.append(name, el.value || "on");
        return;
      }

      formData.append(name, el.value ?? "");
    });

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

    const data = await resp.json();
    if (!data || data.ok !== true) {
      throw new Error("Resposta inválida do servidor.");
    }
    return data;
  }

  function syncExecutionContractAfterSave() {
    // Após salvar, a sessão é encerrada -> UI deve virar read-only.
    const root = document.getElementById("execution-root");
    if (!root) return;

    root.dataset.hasSession = "0";
    root.dataset.canEdit = "0";
    // canFinalize mantém como está (gates podem permitir ações finais em próximas MTs)
  }

  function requestApplyState() {
    document.dispatchEvent(new CustomEvent("execucao:apply-state"));
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

      // Centralização (ISSUE #71): contrato + reaplicar estado via state manager
      syncExecutionContractAfterSave();
      document.dispatchEvent(new CustomEvent("execucao:mark-items-bipado"));
      requestApplyState();

      showAbrirParaContinuar();
    } catch (err) {
      btn.disabled = false;
      btn.textContent = LABEL_DEFAULT;
      setStatus("Erro ao salvar. Tente novamente.");
      // console.error(err);
    }
  });
})();