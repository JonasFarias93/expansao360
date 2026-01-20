from __future__ import annotations

from expansao360.application.ports.location_repository import LocationRepository
from expansao360.domain.registry import Location
from expansao360.domain.value_objects import LocationId


class InMemoryLocationRepository(LocationRepository):
    def __init__(self) -> None:
        self._items: dict[str, Location] = {}

    def save(self, location: Location) -> None:
        self._items[str(location.id)] = location

    def get(self, location_id: LocationId) -> Location | None:
        return self._items.get(str(location_id))
