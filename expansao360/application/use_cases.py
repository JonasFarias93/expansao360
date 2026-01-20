from __future__ import annotations

from datetime import datetime

from expansao360.application.ports.location_repository import LocationRepository
from expansao360.application.ports.operation_repository import OperationRepository
from expansao360.domain.models import OperationMount
from expansao360.domain.registry import Location
from expansao360.domain.value_objects import LocationId


def register_mount(
    *,
    registry_location_id: str,
    performed_by: str,
    performed_at: datetime,
    repository: OperationRepository,
    location_repository: LocationRepository,
) -> OperationMount:
    """
    Caso de uso: registrar uma montagem/executação em campo.

    Regras:
    - A Location (Registry) deve existir antes de registrar a Operation.
    - Persiste a operação via OperationRepository.
    """
    location_id = LocationId(registry_location_id)

    if location_repository.get(location_id) is None:
        raise ValueError("location does not exist")

    op = OperationMount(
        registry_location_id=str(location_id),
        performed_by=performed_by,
        performed_at=performed_at,
    )

    repository.save(op)
    return op


def register_location(
    *,
    location_id: str,
    name: str,
    repository: LocationRepository,
) -> Location:
    """
    Caso de uso: registrar uma Location no Registry.
    """
    loc = Location(
        id=LocationId(location_id),
        name=name,
    )

    repository.save(loc)
    return loc
