(function () {
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  function setLoading(btn, isLoading) {
    if (isLoading) {
      btn.dataset.originalText = btn.textContent;
      btn.disabled = true;
      btn.classList.add("opacity-70", "cursor-not-allowed");
      btn.textContent = "Salvando...";
    } else {
      btn.disabled = btn.getAttribute("aria-disabled") === "true";
      btn.classList.remove("opacity-70", "cursor-not-allowed");
      btn.textContent = btn.dataset.originalText || btn.textContent;
    }
  }

  function showError(itemId, msg) {
    const el = document.querySelector(`.js-configurar-erro[data-item-id="${itemId}"]`);
    if (!el) return;
    el.textContent = msg;
    el.classList.remove("hidden");
  }

  function clearError(itemId) {
    const el = document.querySelector(`.js-configurar-erro[data-item-id="${itemId}"]`);
    if (!el) return;
    el.textContent = "";
    el.classList.add("hidden");
  }

  function updateUI(btn, payload) {
    // botão
    btn.textContent = "Configurado ✅";
    btn.setAttribute("aria-disabled", "true");
    btn.disabled = true;

    // meta (por/às)
    const itemId = btn.dataset.itemId;
    const meta = document.querySelector(`.js-configurado-meta[data-item-id="${itemId}"]`);
    if (meta) {
      const por = payload.configurado_por ? `por ${payload.configurado_por}` : "";
      let as = "";
      if (payload.configurado_em) {
        try {
          const d = new Date(payload.configurado_em);
          const hh = String(d.getHours()).padStart(2, "0");
          const mm = String(d.getMinutes()).padStart(2, "0");
          as = `às ${hh}:${mm}`;
        } catch (e) {
          // fallback sem quebrar
        }
      }
      const txt = [por, as].filter(Boolean).join(" ");
      meta.textContent = txt;
    }
  }

  async function onClick(e) {
    const btn = e.target.closest(".js-configurar-item");
    if (!btn) return;

    const itemId = btn.dataset.itemId;
    const url = btn.dataset.url;

    if (!url || !itemId) return;
    if (btn.disabled) return;

    clearError(itemId);
    setLoading(btn, true);

    try {
      const resp = await fetch(url, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
      });

      const data = await resp.json().catch(() => null);

      if (!resp.ok) {
        // 403 (sessão/permissão) ou outros
        const code = data && data.error ? data.error : "ERRO";
        if (resp.status === 403 && code === "SESSAO_INATIVA") {
          showError(itemId, "Sessão inativa. Abra o chamado para iniciar a sessão.");
        } else if (resp.status === 403) {
          showError(itemId, "Sem permissão para marcar como configurado.");
        } else {
          showError(itemId, "Erro ao marcar configurado. Tente novamente.");
        }
        return;
      }

      if (!data || data.ok !== true) {
        showError(itemId, "Resposta inválida do servidor.");
        return;
      }

      // idempotente: já configurado ou configurou agora -> sempre atualiza UI
      updateUI(btn, data);
    } catch (err) {
      showError(itemId, "Falha de rede. Verifique sua conexão.");
    } finally {
      setLoading(btn, false);
    }
  }

  document.addEventListener("click", onClick);
})();