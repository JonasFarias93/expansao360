from __future__ import annotations

from dataclasses import dataclass

from django.db import IntegrityError, transaction
from django.utils import timezone
from execucao.models import Chamado, ExecutionSession


class SessionBlockedError(Exception):
    pass


@dataclass(frozen=True)
class OpenSessionResult:
    session: ExecutionSession
    created: bool
    reentered: bool


@transaction.atomic
def open_session(*, chamado: Chamado, user) -> ExecutionSession:
    """
    Abre (ou reentra) uma sessão exclusiva por chamado.

    Regras:
    - Se já existe sessão aberta do mesmo usuário e ainda válida -> reentra (retorna a mesma).
    - Se existe sessão aberta de outro usuário e ainda válida -> bloqueia (SessionBlockedError).
    - Se existe sessão aberta mas expirada (expires_at <= now) -> encerra como TIMEOUT e cria nova.
    - Sempre evita IntegrityError por constraint (uniq_open_execution_session_per_chamado).
    """
    now = timezone.now()

    # Pega qualquer sessão "aberta" (ended_at is null) e trava a linha
    existing = (
        ExecutionSession.objects.select_for_update()
        .filter(chamado=chamado, ended_at__isnull=True)
        .order_by("-started_at")
        .first()
    )

    if existing is not None:
        # Sessão aberta porém expirada: encerra para liberar o constraint
        if existing.expires_at <= now:
            existing.ended_at = now
            existing.ended_reason = ExecutionSession.EndReason.TIMEOUT
            existing.save(update_fields=["ended_at", "ended_reason"])
            existing = None
        else:
            # Ainda válida
            if existing.usuario_id == user.id:
                return existing
            raise SessionBlockedError

    # Cria nova sessão
    try:
        return ExecutionSession.objects.create(chamado=chamado, usuario=user)
    except IntegrityError as err:
        current = (
            ExecutionSession.objects.select_for_update()
            .filter(chamado=chamado, ended_at__isnull=True)
            .order_by("-started_at")
            .first()
        )
        if current is not None and current.expires_at > now and current.usuario_id == user.id:
            return current
        raise SessionBlockedError from err
