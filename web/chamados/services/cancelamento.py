# web/chamados/services/cancelamento.py
from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils import timezone

from chamados.models import Chamado

STATUS_CANCELAVEIS = {
    Chamado.Status.EM_ABERTURA,
    Chamado.Status.ABERTO,
    Chamado.Status.EM_EXECUCAO,
    Chamado.Status.AGUARDANDO_NF,
    Chamado.Status.AGUARDANDO_COLETA,
}


def cancelar_chamado(chamado: Chamado, user, motivo: str) -> None:
    """
    Cancela um chamado com motivo obrigatório.
    - Não cancela FINALIZADO nem já CANCELADO.
    - Registra quem cancelou, quando e por quê.
    """
    if chamado.status == Chamado.Status.FINALIZADO:
        raise ValidationError("Chamado finalizado não pode ser cancelado.")

    if chamado.status == Chamado.Status.CANCELADO:
        raise ValidationError("Chamado já está cancelado.")

    if chamado.status not in STATUS_CANCELAVEIS:
        raise ValidationError(
            f"Chamado com status '{chamado.get_status_display()}' não pode ser cancelado."
        )

    motivo = (motivo or "").strip()
    if not motivo:
        raise ValidationError("Informe o motivo do cancelamento.")

    chamado.status = Chamado.Status.CANCELADO
    chamado.cancelado_em = timezone.now()
    chamado.cancelado_por = user
    chamado.motivo_cancelamento = motivo
    chamado.save(update_fields=[
        "status",
        "cancelado_em",
        "cancelado_por",
        "motivo_cancelamento",
    ])