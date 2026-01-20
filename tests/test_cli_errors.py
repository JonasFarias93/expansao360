from pathlib import Path

from typer.testing import CliRunner

from expansao360.cli import app


def test_mount_register_fails_when_location_missing(tmp_path: Path, monkeypatch) -> None:
    state = tmp_path / "state.json"
    monkeypatch.setenv("EXP360_STATE", str(state))

    runner = CliRunner()
    result = runner.invoke(app, ["mount", "register", "LOC-404", "jonas"])

    assert result.exit_code != 0
    assert "ERRO" in result.stdout
