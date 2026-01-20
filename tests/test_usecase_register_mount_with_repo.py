from datetime import UTC, datetime


def test_register_mount_persists_operation():
    from expansao360.application.use_cases import register_mount
    from expansao360.infrastructure.repositories import InMemoryOperationRepository

    repo = InMemoryOperationRepository()

    op = register_mount(
        registry_location_id="LOC-001",
        performed_by="jonas",
        performed_at=datetime(2026, 1, 20, tzinfo=UTC),
        repository=repo,
    )

    assert len(repo.list_all()) == 1
    assert repo.list_all()[0] == op
