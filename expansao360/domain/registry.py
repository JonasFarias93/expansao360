from __future__ import annotations

from dataclasses import dataclass

from .value_objects import LocationId


@dataclass(frozen=True)
class Location:
    """
    Entidade do Registry (Cadastro Mestre).
    Define o que existe e como deve ser.

    Regras mínimas:
    - id obrigatório (LocationId)
    - name obrigatório (não vazio)
    """

    id: LocationId
    name: str

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("name is required")

        # Normaliza name (sem mexer em maiúsculas/minúsculas por enquanto)
        object.__setattr__(self, "name", self.name.strip())
