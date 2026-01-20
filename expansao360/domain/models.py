from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OperationMount:
    """
    Registro transacional de execução em campo (Operation).

    Regras mínimas:
    - Deve referenciar um item do Registry (registry_location_id).
    - Deve registrar quem executou (performed_by).
    - Deve registrar quando ocorreu (performed_at).
    """

    registry_location_id: str
    performed_by: str
    performed_at: datetime

    def __post_init__(self) -> None:
        if not self.registry_location_id or not self.registry_location_id.strip():
            raise ValueError("registry_location_id is required")

        if not self.performed_by or not self.performed_by.strip():
            raise ValueError("performed_by is required")

        if not isinstance(self.performed_at, datetime):
            raise ValueError("performed_at must be a datetime")
