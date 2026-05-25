from __future__ import annotations

import argparse
import pathlib
import sys
from typing import Sequence

from .io import PolyConfigError, detect_format, dump_text, read_config, write_config


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="polyconfig",
        description="Format and convert JSON, YAML, and TOML files.",
    )
    parser.add_argument("source", help="Input config file path")
    parser.add_argument("destination", nargs="?", help="Optional output file path")
    parser.add_argument("--from-format", choices=["json", "yaml", "toml"], help="Override detected input format")
    parser.add_argument("--to-format", choices=["json", "yaml", "toml"], help="Override detected output format")
    parser.add_argument("--indent", type=int, default=2, help="Indent size for JSON/YAML output")
    parser.add_argument("--sort-keys", action="store_true", help="Sort object keys when supported")
    parser.add_argument(
        "--stdout",
        action="store_true",
        help="Write result to stdout instead of a file",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    source = pathlib.Path(args.source)

    try:
        data = read_config(source, args.from_format)
        out_fmt = args.to_format
        if args.stdout:
            if not out_fmt:
                out_fmt = args.from_format or detect_format(source)
            sys.stdout.write(dump_text(data, out_fmt, indent=args.indent, sort_keys=args.sort_keys))
            return 0

        if not args.destination:
            write_config(source, data, args.from_format or detect_format(source), indent=args.indent, sort_keys=args.sort_keys)
            return 0

        destination = pathlib.Path(args.destination)
        write_config(destination, data, out_fmt, indent=args.indent, sort_keys=args.sort_keys)
        return 0
    except (FileNotFoundError, PolyConfigError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
