from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "polyconfig.cli", *args],
        cwd=cwd or ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_format_json_in_place(tmp_path: Path) -> None:
    source = tmp_path / "sample.json"
    source.write_text('{"z":1,"a":2}', encoding="utf-8")

    result = run_cli(str(source), "--sort-keys", "--indent", "4")

    assert result.returncode == 0
    assert json.loads(source.read_text(encoding="utf-8")) == {"a": 2, "z": 1}
    assert '\n    "a": 2' in source.read_text(encoding="utf-8")


def test_convert_yaml_to_toml(tmp_path: Path) -> None:
    source = tmp_path / "sample.yaml"
    destination = tmp_path / "sample.toml"
    source.write_text("name: polyconfig\nitems:\n  - 1\n  - 2\n", encoding="utf-8")

    result = run_cli(str(source), str(destination))

    assert result.returncode == 0
    content = destination.read_text(encoding="utf-8")
    assert 'name = "polyconfig"' in content
    assert "items = [" in content
    assert "1" in content
    assert "2" in content


def test_emit_json_to_stdout(tmp_path: Path) -> None:
    source = tmp_path / "sample.yaml"
    source.write_text("name: polyconfig\n", encoding="utf-8")

    result = run_cli(str(source), "--to-format", "json", "--stdout")

    assert result.returncode == 0
    assert json.loads(result.stdout) == {"name": "polyconfig"}


def test_reject_unknown_extension(tmp_path: Path) -> None:
    source = tmp_path / "sample.txt"
    source.write_text("hello", encoding="utf-8")

    result = run_cli(str(source))

    assert result.returncode == 1
    assert "Unsupported file extension" in result.stderr
