from datetime import UTC, datetime

import pytest


def test_operation_requires_registry_reference_and_actor():
    # import dentro do teste para garantir que falha se o módulo não existir ainda
    from expansao360.domain.models import OperationMount

    with pytest.raises(ValueError):
        OperationMount(
            registry_location_id="",
            performed_by="jonas",
            performed_at=datetime.now(UTC),
        )

    with pytest.raises(ValueError):
        OperationMount(
            registry_location_id="LOC-001",
            performed_by="",
            performed_at=datetime.now(UTC),
        )
