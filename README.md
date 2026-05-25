# polyconfig

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-30363d?logo=GitHub-Sponsors)](https://github.com/sponsors/duongynhi000005-oss)

`polyconfig` is a Python CLI for developers who keep bouncing between JSON, YAML, and TOML.
It formats files in place, converts between config formats, and can print normalized output to stdout for shell pipelines.

## Why it exists

- Clean up ugly `package.json`, `docker-compose.yaml`, or `pyproject.toml` style fixtures quickly
- Convert configs between tools without writing one-off scripts
- Use it in CI or shell pipelines with `--stdout`

## Install

```bash
pip install polyconfig
```

## Usage

Format a file in place:

```bash
polyconfig config.json --sort-keys --indent 2
```

Convert YAML to TOML:

```bash
polyconfig config.yaml config.toml
```

Print normalized JSON to stdout:

```bash
polyconfig settings.yaml --to-format json --stdout
```

Force input/output formats when extensions are missing or misleading:

```bash
polyconfig raw.data result.json --from-format yaml --to-format json
```

## Features

- JSON, YAML, and TOML support
- In-place formatting for existing files
- File-to-file conversion based on extension or explicit flags
- Stdout mode for piping into other tools
- Minimal dependencies and Python 3.11+

## Development

```bash
python -m pip install -e .[dev]
pytest
python -m build
```

## Sponsorship

If `polyconfig` saves you time, sponsor more small developer tools here:
<https://github.com/sponsors/duongynhi000005-oss>

## License

MIT
