from __future__ import annotations

from pathlib import Path

from expansao360.application.ports.location_repository import LocationRepository
from expansao360.application.ports.operation_repository import OperationRepository
from expansao360.domain.models import OperationMount
from expansao360.domain.registry import Location
from expansao360.domain.value_objects import LocationId

from .file_state import (
    deserialize_location,
    deserialize_operation,
    load_state,
    save_state,
    serialize_location,
    serialize_operation,
)


class FileLocationRepository(LocationRepository):
    def __init__(self, state_path: Path) -> None:
        self._path = state_path

    def save(self, location: Location) -> None:
        state = load_state(self._path)
        state["locations"][str(location.id)] = serialize_location(location)
        save_state(self._path, state)

    def get(self, location_id: LocationId) -> Location | None:
        state = load_state(self._path)
        raw = state["locations"].get(str(location_id))
        return None if raw is None else deserialize_location(raw)

    def list_all(self) -> list[Location]:
        state = load_state(self._path)
        return [deserialize_location(v) for v in state["locations"].values()]


class FileOperationRepository(OperationRepository):
    def __init__(self, state_path: Path) -> None:
        self._path = state_path

    def save(self, operation: OperationMount) -> None:
        state = load_state(self._path)
        state["operations"].append(serialize_operation(operation))
        save_state(self._path, state)

    def list_all(self) -> list[OperationMount]:
        state = load_state(self._path)
        return [deserialize_operation(v) for v in state["operations"]]
