import pytest

from expansao360.domain.value_objects import MountStatus


@pytest.mark.parametrize(
    "status, expected",
    [
        (MountStatus.EM_SEPARACAO, "Em Separação"),
        (MountStatus.EM_PROCESSO, "Em Execução"),
        (MountStatus.CONCLUIDO, "Concluído"),
    ],
)
def test_mount_status_label(status: MountStatus, expected: str) -> None:
    assert status.label == expected


@pytest.mark.parametrize(
    "status, expected",
    [
        (MountStatus.EM_SEPARACAO, True),
        (MountStatus.EM_PROCESSO, True),
        (MountStatus.CONCLUIDO, False),
    ],
)
def test_mount_status_can_execute(status: MountStatus, expected: bool) -> None:
    assert status.can_execute is expected
