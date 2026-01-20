from __future__ import annotations

from expansao360.application.ports.operation_repository import OperationRepository
from expansao360.domain.models import OperationMount


class InMemoryOperationRepository(OperationRepository):
    def __init__(self) -> None:
        self._items: list[OperationMount] = []

    def save(self, operation: OperationMount) -> None:
        self._items.append(operation)

    def list_all(self) -> list[OperationMount]:
        return list(self._items)
