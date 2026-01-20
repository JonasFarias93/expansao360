from datetime import UTC, datetime

from expansao360.domain.registry import Location
from expansao360.domain.value_objects import LocationId
from expansao360.infrastructure.repositories import (
    InMemoryLocationRepository,
    InMemoryOperationRepository,
)


def test_register_mount_persists_operation():
    from expansao360.application.use_cases import register_mount

    op_repo = InMemoryOperationRepository()
    loc_repo = InMemoryLocationRepository()
    loc_repo.save(Location(id=LocationId("LOC-001"), name="Loja A"))

    op = register_mount(
        registry_location_id="LOC-001",
        performed_by="jonas",
        performed_at=datetime(2026, 1, 20, tzinfo=UTC),
        repository=op_repo,
        location_repository=loc_repo,
    )

    assert len(op_repo.list_all()) == 1
    assert op_repo.list_all()[0] == op
