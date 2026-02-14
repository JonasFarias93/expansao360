from datetime import UTC, datetime

import pytest

from expansao360.domain.registry import Location
from expansao360.domain.value_objects import LocationId
from expansao360.infrastructure.repositories import (
    InMemoryLocationRepository,
    InMemoryOperationRepository,
)


def test_register_mount_creates_operationmount():
    from expansao360.application.use_cases import register_mount

    op_repo = InMemoryOperationRepository()
    loc_repo = InMemoryLocationRepository()
    loc_repo.save(Location(id=LocationId("LOC-001"), name="Loja A"))

    op = register_mount(
        registry_location_id=" LOC-001 ",
        performed_by=" jonas ",
        performed_at=datetime(2026, 1, 20, 12, 0, tzinfo=UTC),
        repository=op_repo,
        location_repository=loc_repo,
    )

    assert op.registry_location_id == "LOC-001"
    assert op.performed_by == "jonas"
    assert op.performed_at.tzinfo is not None


def test_register_mount_rejects_invalid_input():
    from expansao360.application.use_cases import register_mount

    op_repo = InMemoryOperationRepository()
    loc_repo = InMemoryLocationRepository()
    loc_repo.save(Location(id=LocationId("LOC-001"), name="Loja A"))

    with pytest.raises(ValueError):
        register_mount(
            registry_location_id="",
            performed_by="jonas",
            performed_at=datetime.now(UTC),
            repository=op_repo,
            location_repository=loc_repo,
        )
