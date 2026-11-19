"""Command line: `python -m ledgerlite summary|categories|export ...`."""

import argparse
import sys
from pathlib import Path

from ledgerlite import export, formatting, reports
from ledgerlite.ledger import Ledger
from ledgerlite.parser import ParseError, read_entries


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="ledgerlite", description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    summary = commands.add_parser("summary", help="totals per month and per category")
    summary.add_argument("file", type=Path)
    categories = commands.add_parser("categories", help="list the categories in use")
    categories.add_argument("file", type=Path)
    exporter = commands.add_parser("export", help="write the ledger, sorted by date, to CSV")
    exporter.add_argument("file", type=Path)
    exporter.add_argument("out", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        ledger = Ledger(read_entries(args.file))
    except (OSError, ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if args.command == "summary":
        print(formatting.table(reports.monthly_totals(ledger), "Per month"))
        print()
        print(formatting.table(reports.category_totals(ledger), "Per category"))
    elif args.command == "categories":
        print("\n".join(ledger.categories()))
    elif args.command == "export":
        count = export.write_csv(ledger, args.out)
        print(f"wrote {count} entries to {args.out}")
    return 0
