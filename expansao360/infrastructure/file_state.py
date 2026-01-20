from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from typing import Any

from expansao360.domain.models import OperationMount
from expansao360.domain.registry import Location
from expansao360.domain.value_objects import ActorId, LocationId


def _default_state() -> dict[str, Any]:
    return {"locations": {}, "operations": []}


def load_state(path: Path) -> dict[str, Any]:
    if not path.exists():
        return _default_state()
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(path: Path, state: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")


def serialize_location(loc: Location) -> dict[str, Any]:
    return {"id": str(loc.id), "name": loc.name}


def deserialize_location(data: dict[str, Any]) -> Location:
    return Location(id=LocationId(data["id"]), name=data["name"])


def serialize_operation(op: OperationMount) -> dict[str, Any]:
    return {
        "registry_location_id": op.registry_location_id,
        "performed_by": op.performed_by,
        "performed_at": op.performed_at.isoformat(),
    }


def deserialize_operation(data: dict[str, Any]) -> OperationMount:
    return OperationMount(
        registry_location_id=str(LocationId(data["registry_location_id"])),
        performed_by=str(ActorId(data["performed_by"])),
        performed_at=datetime.fromisoformat(data["performed_at"]),
    )
