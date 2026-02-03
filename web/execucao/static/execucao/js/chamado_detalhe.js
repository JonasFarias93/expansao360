/* web/execucao/static/execucao/chamado_detalhe.js */


  function pedirMotivoEEnviar(formId, precisaMotivo) {
    if (precisaMotivo) {
      const motivo = prompt("Informe o motivo da mudança:");
      if (!motivo || !motivo.trim()) return false;

      const form = document.getElementById(formId);
      form.querySelector('input[name="motivo"]').value = motivo.trim();
      form.submit();
      return false;
    }

    if (!confirm("Confirmar alteração de status?")) return false;
    document.getElementById(formId).submit();
    return false;
  }

