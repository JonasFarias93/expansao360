from pathlib import Path

from typer.testing import CliRunner

from expansao360.cli import app


def test_cli_location_add_and_mount_register(tmp_path: Path, monkeypatch) -> None:
    state = tmp_path / "state.json"
    monkeypatch.setenv("EXP360_STATE", str(state))

    runner = CliRunner()

    r1 = runner.invoke(app, ["location", "add", "LOC-001", "Loja A"])
    assert r1.exit_code == 0
    assert "OK" in r1.stdout

    r2 = runner.invoke(app, ["mount", "register", "LOC-001", "jonas"])
    assert r2.exit_code == 0
    assert "OK" in r2.stdout

    r3 = runner.invoke(app, ["mount", "list"])
    assert r3.exit_code == 0
    assert "LOC-001" in r3.stdout
