from __future__ import annotations

from abc import ABC, abstractmethod

from ...domain.registry import Location
from ...domain.value_objects import LocationId


class LocationRepository(ABC):
    @abstractmethod
    def save(self, location: Location) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, location_id: LocationId) -> Location | None:
        raise NotImplementedError
