/* web/execucao/static/execucao/js/chamado_abertura.js */

(function () {
  function initLojaLookup() {
    const inputCodigo = document.getElementById("id_loja_codigo");
    const hiddenLojaId = document.getElementById("id_loja"); // name="loja"
    const statusEl = document.getElementById("loja-status");
    const btnValidar = document.getElementById("btn-loja-validar");
    const form = document.getElementById("form-chamado-abertura");

    if (!inputCodigo || !hiddenLojaId || !statusEl || !btnValidar || !form) return;

    // endpoint vem do template via data-attribute (evita hardcode e mantém js reutilizável)
    const endpoint = inputCodigo.dataset.lookupUrl;
    if (!endpoint) return;

    // Evita concorrência: só aplica o resultado da última validação solicitada
    let requestSeq = 0;

    function setStatus(text, kind) {
      statusEl.textContent = text || "";
      statusEl.className =
        "text-sm " +
        (kind === "ok"
          ? "text-green-700"
          : kind === "err"
          ? "text-red-700"
          : "text-slate-600");
    }

    function isValidCodigo(codigo) {
      return /^\d+$/.test(codigo);
    }

    async function validarLoja() {
      const codigo = (inputCodigo.value || "").trim();

      // invalida seleção anterior sempre que valida novamente
      hiddenLojaId.value = "";

      if (!codigo) {
        setStatus("Informe o código da loja.", "err");
        return;
      }
      if (!isValidCodigo(codigo)) {
        setStatus("Código inválido. Use apenas números.", "err");
        return;
      }

      const mySeq = ++requestSeq;
      setStatus("Validando...", "idle");

      try {
        const url = `${endpoint}?codigo=${encodeURIComponent(codigo)}`;
        const resp = await fetch(url, {
          method: "GET",
          headers: { Accept: "application/json" },
          credentials: "same-origin",
        });

        // Se já houve outra validação depois desta, ignora o resultado
        if (mySeq !== requestSeq) return;

        if (resp.status === 404) {
          setStatus("Loja não encontrada.", "err");
          return;
        }
        if (resp.status === 400) {
          setStatus("Código inválido.", "err");
          return;
        }
        if (!resp.ok) {
          setStatus("Erro ao validar loja. Tente novamente.", "err");
          return;
        }

        const data = await resp.json();
        if (
          !data ||
          data.id === undefined ||
          data.codigo === undefined ||
          data.nome === undefined
        ) {
          setStatus("Resposta inválida do servidor.", "err");
          return;
        }

        hiddenLojaId.value = String(data.id);
        setStatus(`Loja encontrada: ${data.codigo} - ${data.nome}`, "ok");
      } catch (_e) {
        // Se já houve outra validação depois desta, ignora erro antigo
        if (mySeq !== requestSeq) return;
        setStatus("Falha de rede ao validar loja.", "err");
      }
    }

    btnValidar.addEventListener("click", function () {
      void validarLoja();
    });

    inputCodigo.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter") {
        ev.preventDefault();
        void validarLoja();
      }
    });

    inputCodigo.addEventListener("input", function () {
      hiddenLojaId.value = "";
      setStatus("", "idle");
    });

    form.addEventListener("submit", function (ev) {
      // Este JS só deve interferir no form de ABERTURA.
      // Não intercepta outros forms da aplicação (ex.: "Abrir" na fila).
      if (!hiddenLojaId.value) {
        ev.preventDefault();
        setStatus("Valide a loja antes de salvar.", "err");
        inputCodigo.focus();
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initLojaLookup);
  } else {
    initLojaLookup();
  }
})();