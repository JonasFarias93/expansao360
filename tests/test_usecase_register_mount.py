from datetime import UTC, datetime

import pytest


def test_register_mount_creates_operationmount():
    from expansao360.application.use_cases import register_mount

    op = register_mount(
        registry_location_id=" LOC-001 ",
        performed_by=" jonas ",
        performed_at=datetime(2026, 1, 20, 12, 0, tzinfo=UTC),
    )

    assert op.registry_location_id == "LOC-001"
    assert op.performed_by == "jonas"
    assert op.performed_at.tzinfo is not None


def test_register_mount_rejects_invalid_input():
    from expansao360.application.use_cases import register_mount

    with pytest.raises(ValueError):
        register_mount(
            registry_location_id="",
            performed_by="jonas",
            performed_at=datetime.now(UTC),
        )
