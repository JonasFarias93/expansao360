from __future__ import annotations

from dataclasses import dataclass


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
