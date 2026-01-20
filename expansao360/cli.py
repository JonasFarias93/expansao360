from __future__ import annotations

from datetime import UTC, datetime
import os
from pathlib import Path

from rich import print
import typer

from expansao360.application.use_cases import register_location, register_mount
from expansao360.infrastructure.file_repositories import (
    FileLocationRepository,
    FileOperationRepository,
)

app = typer.Typer(help="EXPANSÃO360 — CLI")


def _state_path() -> Path:
    raw = os.getenv("EXP360_STATE", ".expansao360-state.json")
    return Path(raw).expanduser().resolve()


def _repos() -> tuple[FileLocationRepository, FileOperationRepository]:
    path = _state_path()
    return (FileLocationRepository(path), FileOperationRepository(path))


location_app = typer.Typer(help="Comandos de Registry (Location)")
mount_app = typer.Typer(help="Comandos de Operation (Mount)")
app.add_typer(location_app, name="location")
app.add_typer(mount_app, name="mount")


@location_app.command("add")
def location_add(location_id: str, name: str) -> None:
    loc_repo, _ = _repos()
    loc = register_location(location_id=location_id, name=name, repository=loc_repo)
    print(f"[green]OK[/green] location criada: {loc.id} — {loc.name}")


@location_app.command("list")
def location_list() -> None:
    loc_repo, _ = _repos()
    items = loc_repo.list_all()
    if not items:
        print("[yellow]Nenhuma location cadastrada.[/yellow]")
        raise typer.Exit(code=0)

    for loc in items:
        print(f"- {loc.id}: {loc.name}")


@mount_app.command("register")
def mount_register(registry_location_id: str, performed_by: str) -> None:
    loc_repo, op_repo = _repos()
    op = register_mount(
        registry_location_id=registry_location_id,
        performed_by=performed_by,
        performed_at=datetime.now(UTC),
        repository=op_repo,
        location_repository=loc_repo,
    )
    print(
        f"[green]OK[/green] mount registrado: "
        f"location={op.registry_location_id} by={op.performed_by}"
    )


@mount_app.command("list")
def mount_list() -> None:
    _, op_repo = _repos()
    items = op_repo.list_all()
    if not items:
        print("[yellow]Nenhuma operação registrada.[/yellow]")
        raise typer.Exit(code=0)

    for op in items:
        print(f"- {op.registry_location_id} | {op.performed_by} | {op.performed_at.isoformat()}")
