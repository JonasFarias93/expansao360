// web/execucao/static/execucao/js/chamado_salvar_execucao_ajax.js
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
 *
 * Contrato (ATUALIZADO):
 * - Salvar execução NÃO encerra sessão.
 * - Portanto este arquivo não deve forçar data-has-session/data-can-edit para "0".
 * - O state manager é o único responsável por aplicar read-only/global lock baseado no contrato real do DOM.
 */
(function () {
  const btn = document.getElementById("btn-salvar-execucao");
  if (!btn) return;

  const statusEl = document.getElementById("salvar-status");
  const url = btn.dataset.url;
  if (!url) return;

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
    if (!csrf) throw new Error("CSRF token ausente.");

    const resp = await fetch(url, {
      method: "POST",
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": csrf,
      },
      body: collectPayload(),
    });

    if (!resp.ok) {
      throw new Error(`Falha ao salvar (${resp.status})`);
    }

    const data = await resp.json();
    if (!data || data.ok !== true) {
      throw new Error("Resposta inválida do servidor.");
    }
    return data;
  }

  function syncExecutionContractAfterSave(data) {
    void data;
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
      btn.disabled = false; // ✅ permite salvar múltiplas vezes
      setStatus(hhmm ? `Salvo às ${hhmm}` : "Salvo");

      syncExecutionContractAfterSave(data);
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