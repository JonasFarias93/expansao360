from datetime import UTC, datetime

import pytest

from expansao360.infrastructure.repositories import InMemoryOperationRepository


def test_register_mount_creates_operationmount():
    from expansao360.application.use_cases import register_mount

    repo = InMemoryOperationRepository()

    op = register_mount(
        registry_location_id=" LOC-001 ",
        performed_by=" jonas ",
        performed_at=datetime(2026, 1, 20, 12, 0, tzinfo=UTC),
        repository=repo,
    )

    assert op.registry_location_id == "LOC-001"
    assert op.performed_by == "jonas"
    assert op.performed_at.tzinfo is not None


def test_register_mount_rejects_invalid_input():
    from expansao360.application.use_cases import register_mount

    repo = InMemoryOperationRepository()

    with pytest.raises(ValueError):
        register_mount(
            registry_location_id="",
            performed_by="jonas",
            performed_at=datetime.now(UTC),
            repository=repo,
        )
