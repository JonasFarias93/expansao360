from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .value_objects import ActorId, LocationId


@dataclass(frozen=True)
class OperationMount:
    """
    Registro transacional de execução em campo (Operation).

    Regras mínimas:
    - Deve referenciar um item do Registry (registry_location_id).
    - Deve registrar quem executou (performed_by).
    - Deve registrar quando ocorreu (performed_at).

    Observação:
    - A API recebe strings por simplicidade, mas converte internamente para Value Objects.
    """

    registry_location_id: str
    performed_by: str
    performed_at: datetime

    def __post_init__(self) -> None:
        # Normaliza e valida via Value Objects
        loc = LocationId(self.registry_location_id)
        actor = ActorId(self.performed_by)

        object.__setattr__(self, "registry_location_id", str(loc))
        object.__setattr__(self, "performed_by", str(actor))

        if not isinstance(self.performed_at, datetime):
            raise ValueError("performed_at must be a datetime")
