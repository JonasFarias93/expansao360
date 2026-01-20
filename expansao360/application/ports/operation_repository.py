from __future__ import annotations

from abc import ABC, abstractmethod

from expansao360.domain.models import OperationMount


class OperationRepository(ABC):
    @abstractmethod
    def save(self, operation: OperationMount) -> None:
        raise NotImplementedError

    @abstractmethod
    def list_all(self) -> list[OperationMount]:
        raise NotImplementedError
