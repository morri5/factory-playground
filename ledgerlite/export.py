"""Writing a ledger back to CSV."""

import csv
from pathlib import Path

from ledgerlite.ledger import Ledger
from ledgerlite.parser import COLUMNS


def write_csv(ledger: Ledger, path: Path) -> int:
    """Write the entries to `path`; returns how many were written.

    The header row is written first, so the file is a valid ledger that
    `read_entries` can read back.
    """
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(COLUMNS)
        for entry in ledger.entries:
            writer.writerow(
                [entry.date.isoformat(), str(entry.amount), entry.category, entry.description]
            )
    return len(ledger.entries)
