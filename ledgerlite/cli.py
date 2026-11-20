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
    summary.add_argument(
        "--category",
        metavar="CATEGORY",
        help="only include entries in this category (case-insensitive)",
    )
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
        shown = ledger.in_category(args.category) if args.category else ledger
        print(formatting.table(reports.monthly_totals(shown), "Per month"))
        print()
        print(formatting.table(reports.category_totals(shown), "Per category"))
    elif args.command == "categories":
        print("\n".join(ledger.categories()))
    elif args.command == "export":
        count = export.write_csv(ledger, args.out)
        print(f"wrote {count} entries to {args.out}")
    return 0
