from __future__ import annotations

import json
import pathlib
import tomllib
from typing import Any

import tomli_w
import yaml

SUPPORTED_SUFFIXES = {
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
}


class PolyConfigError(ValueError):
    """Raised when an input or output format is unsupported."""


def detect_format(path: pathlib.Path) -> str:
    fmt = SUPPORTED_SUFFIXES.get(path.suffix.lower())
    if not fmt:
        raise PolyConfigError(f"Unsupported file extension: {path.suffix or '<none>'}")
    return fmt


def load_text(text: str, fmt: str) -> Any:
    if fmt == "json":
        return json.loads(text)
    if fmt == "yaml":
        return yaml.safe_load(text)
    if fmt == "toml":
        return tomllib.loads(text)
    raise PolyConfigError(f"Unsupported format: {fmt}")


def dump_text(data: Any, fmt: str, *, indent: int = 2, sort_keys: bool = False) -> str:
    if fmt == "json":
        return json.dumps(data, indent=indent, sort_keys=sort_keys) + "\n"
    if fmt == "yaml":
        return yaml.safe_dump(data, sort_keys=sort_keys, indent=indent)
    if fmt == "toml":
        return tomli_w.dumps(data)
    raise PolyConfigError(f"Unsupported format: {fmt}")


def read_config(path: pathlib.Path, fmt: str | None = None) -> Any:
    selected = fmt or detect_format(path)
    return load_text(path.read_text(encoding="utf-8"), selected)


def write_config(
    path: pathlib.Path,
    data: Any,
    fmt: str | None = None,
    *,
    indent: int = 2,
    sort_keys: bool = False,
) -> None:
    selected = fmt or detect_format(path)
    path.write_text(dump_text(data, selected, indent=indent, sort_keys=sort_keys), encoding="utf-8")
