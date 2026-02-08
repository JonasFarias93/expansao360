from __future__ import annotations

from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone
from execucao.models import Chamado, ExecutionSession


class ActiveSessionConflictError(Exception):
    """Já existe sessão ativa para este chamado (ended_at NULL e expires_at > now)."""


@dataclass(frozen=True)
class ActiveSessionInfo:
    session: ExecutionSession


def get_active_session(*, chamado: Chamado) -> ExecutionSession | None:
    """
    Retorna a sessão ativa do chamado (se existir).
    Definição: ended_at IS NULL e expires_at > now().
    """
    return (
        ExecutionSession.objects.filter(
            chamado=chamado,
            ended_at__isnull=True,
            expires_at__gt=timezone.now(),
        )
        .order_by("-started_at")
        .first()
    )


@transaction.atomic
def create_active_session(*, chamado: Chamado, user) -> ExecutionSession:
    """
    Cria sessão para o chamado garantindo que não exista outra sessão ativa.
    Regra de domínio: não pode haver 2 sessões ativas para o mesmo chamado.
    """
    # trava a linha do chamado para evitar corrida (especialmente em Postgres)
    Chamado.objects.select_for_update().filter(id=chamado.id).exists()

    current_active = get_active_session(chamado=chamado)
    if current_active is not None:
        raise ActiveSessionConflictError()

    try:
        return ExecutionSession.objects.create(chamado=chamado, usuario=user)
    except IntegrityError:
        # Fallback: se duas transações tentarem criar ao mesmo tempo,
        # o constraint de "sessão aberta única" pode disparar.
        raise ActiveSessionConflictError() from None
