from __future__ import annotations

from datetime import datetime

from expansao360.domain.models import OperationMount


def register_mount(
    *,
    registry_location_id: str,
    performed_by: str,
    performed_at: datetime,
) -> OperationMount:
    """
    Caso de uso: registrar uma montagem/executação em campo.

    Recebe dados simples (strings/datetime), valida e retorna o registro de operação.
    Persistência e integrações são responsabilidade de camadas futuras.
    """
    return OperationMount(
        registry_location_id=registry_location_id,
        performed_by=performed_by,
        performed_at=performed_at,
    )
