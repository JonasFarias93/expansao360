import pytest


def test_location_requires_id_and_name():
    from expansao360.domain.registry import Location
    from expansao360.domain.value_objects import LocationId

    with pytest.raises(ValueError):
        Location(id=LocationId("LOC-001"), name="")

    with pytest.raises(ValueError):
        Location(id=LocationId("LOC-001"), name="   ")


def test_location_keeps_normalized_id():
    from expansao360.domain.registry import Location
    from expansao360.domain.value_objects import LocationId

    loc = Location(id=LocationId("  LOC-001  "), name="Loja A")
    assert str(loc.id) == "LOC-001"
