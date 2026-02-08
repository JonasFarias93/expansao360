from __future__ import annotations

from dataclasses import dataclass

from django.db import transaction
from execucao.models import Chamado, ExecutionSession
from execucao.services.execution_session import get_active_session


class SessionBlockedError(Exception):
    pass


@dataclass(frozen=True)
class OpenSessionResult:
    session: ExecutionSession
    created: bool
    reentered: bool


@transaction.atomic
def open_session(*, chamado: Chamado, user) -> OpenSessionResult:
    Chamado.objects.select_for_update().filter(id=chamado.id).exists()

    current = get_active_session(chamado=chamado)

    if current is None:
        session = ExecutionSession.objects.create(chamado=chamado, usuario=user)
        return OpenSessionResult(session=session, created=True, reentered=False)

    if current.usuario_id == user.id:
        return OpenSessionResult(session=current, created=False, reentered=True)

    raise SessionBlockedError()
