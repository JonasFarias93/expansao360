import pytest


def test_location_id_rejects_blank():
    from expansao360.domain.value_objects import LocationId

    with pytest.raises(ValueError):
        LocationId("")

    with pytest.raises(ValueError):
        LocationId("   ")


def test_location_id_strips_whitespace():
    from expansao360.domain.value_objects import LocationId

    loc = LocationId("  LOC-001  ")
    assert str(loc) == "LOC-001"


def test_actor_id_rejects_blank():
    from expansao360.domain.value_objects import ActorId

    with pytest.raises(ValueError):
        ActorId("")

    with pytest.raises(ValueError):
        ActorId("   ")


def test_actor_id_strips_whitespace():
    from expansao360.domain.value_objects import ActorId

    actor = ActorId("  jonas  ")
    assert str(actor) == "jonas"
