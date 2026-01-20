from expansao360.infrastructure.repositories import InMemoryLocationRepository


def test_register_location_creates_and_persists_location():
    from expansao360.application.use_cases import register_location

    repo = InMemoryLocationRepository()

    loc = register_location(
        location_id="LOC-001",
        name="Loja A",
        repository=repo,
    )

    stored = repo.get(loc.id)

    assert stored is not None
    assert stored.id == loc.id
    assert stored.name == "Loja A"
