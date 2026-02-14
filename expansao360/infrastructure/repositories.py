from __future__ import annotations

from ..application.ports.location_repository import LocationRepository
from ..application.ports.operation_repository import OperationRepository
from ..domain.models import OperationMount
from ..domain.registry import Location
from ..domain.value_objects import LocationId


class InMemoryOperationRepository(OperationRepository):
    def __init__(self) -> None:
        self._items: list[OperationMount] = []

    def save(self, operation: OperationMount) -> None:
        self._items.append(operation)

    def list_all(self) -> list[OperationMount]:
        return list(self._items)


class InMemoryLocationRepository(LocationRepository):
    def __init__(self) -> None:
        self._items: dict[str, Location] = {}

    def save(self, location: Location) -> None:
        self._items[str(location.id)] = location

    def get(self, location_id: LocationId) -> Location | None:
        return self._items.get(str(location_id))
