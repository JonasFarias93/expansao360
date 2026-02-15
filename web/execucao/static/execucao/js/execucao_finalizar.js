/**
 * Usado em:
 * - web/chamados/templates/execucao/chamado_execucao.html
 *
 * Responsabilidade:
 * - Ações de finalização do chamado/executar encerramento (ex: submit/fetch + UI de confirmação).
 *
 * Pré-requisitos DOM:
 * - (preencher) IDs/classes/data-* utilizados no script.
 *
 * Observações:
 * - Carregado via <script defer> no template de página.
 */

(function () {
  const btn = document.getElementById("btn-finalizar-chamado");
  if (!btn) return;

  const feedback = document.getElementById("finalizar-feedback");
  const url = btn.dataset.url;

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift() || null;
    return null;
  }

  function showError(html) {
    if (!feedback) return;
    feedback.innerHTML = html;
    feedback.classList.remove("hidden");
  }

  function clearError() {
    if (!feedback) return;
    feedback.innerHTML = "";
    feedback.classList.add("hidden");
  }

  btn.addEventListener("click", async () => {
    btn.disabled = true;
    btn.textContent = "Finalizando…";
    clearError();

    try {
      const csrf = getCookie("csrftoken");
      const resp = await fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrf,
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const data = await resp.json();

      if (!resp.ok) {
        // monta feedback por seção
        let html = "<strong>Pendências para finalizar:</strong><ul class='list-disc pl-5 mt-2'>";

        for (const p of data.pendencias?.fiscais || []) {
          html += `<li>Fiscal: ${p.message}</li>`;
        }
        for (const p of data.pendencias?.coleta || []) {
          html += `<li>Coleta: ${p.message}</li>`;
        }
        for (const p of data.pendencias?.itens || []) {
          html += `<li>Item ${p.item_id}: ${p.message}</li>`;
        }

        html += "</ul>";
        showError(html);

        btn.disabled = false;
        btn.textContent = "Finalizar chamado";
        return;
      }

      // sucesso → reload simples (tela read-only)
      window.location.reload();

    } catch (err) {
      showError("Erro inesperado ao finalizar. Tente novamente.");
      btn.disabled = false;
      btn.textContent = "Finalizar chamado";
    }
  });
})();