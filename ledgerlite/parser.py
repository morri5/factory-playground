"""Reading a ledger CSV file (columns: date, amount, category, description)."""

import csv
import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

from ledgerlite.models import Entry

COLUMNS = ["date", "amount", "category", "description"]


class ParseError(ValueError):
    """A line of the CSV file could not be read."""


def parse_line(row: dict[str, str], line: int) -> Entry:
    try:
        date = datetime.date.fromisoformat(row["date"].strip())
    except ValueError as exc:
        raise ParseError(f"line {line}: bad date {row['date']!r}") from exc
    try:
        amount = Decimal(row["amount"].strip())
    except InvalidOperation as exc:
        raise ParseError(f"line {line}: bad amount {row['amount']!r}") from exc
    category = row["category"].strip().lower()
    if not category:
        raise ParseError(f"line {line}: missing category")
    return Entry(date, amount, category, (row.get("description") or "").strip())


def read_entries(path: Path) -> list[Entry]:
    with path.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        if [h.strip().lower() for h in header] != COLUMNS:
            raise ParseError(f"expected header {','.join(COLUMNS)}, got {','.join(header)}")
        return [
            parse_line(dict(zip(COLUMNS, row, strict=False)), number)
            for number, row in enumerate(reader, start=2)
            if row
        ]
