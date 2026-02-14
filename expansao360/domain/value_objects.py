# expansao360/domain/value_objects.py
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


def _require_non_empty(value: str, field_name: str) -> str:
    if value is None:
        raise ValueError(f"{field_name} is required")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} is required")
    return normalized


@dataclass(frozen=True)
class LocationId:
    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _require_non_empty(self.value, "location_id"))

    def __str__(self) -> str:
        return self.value


@dataclass(frozen=True)
class ActorId:
    value: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "value", _require_non_empty(self.value, "actor_id"))

    def __str__(self) -> str:
        return self.value


class MountStatus(str, Enum):
    EM_SEPARACAO = "em_separacao"
    EM_PROCESSO = "em_processo"
    CONCLUIDO = "concluido"

    @property
    def label(self) -> str:
        return {
            MountStatus.EM_SEPARACAO: "Em Separação",
            MountStatus.EM_PROCESSO: "Em Execução",
            MountStatus.CONCLUIDO: "Concluído",
        }[self]

    @property
    def can_execute(self) -> bool:
        return self in (MountStatus.EM_SEPARACAO, MountStatus.EM_PROCESSO)
