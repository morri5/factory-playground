"""Writing a ledger back to CSV."""

import csv
from pathlib import Path

from ledgerlite.ledger import Ledger


def write_csv(ledger: Ledger, path: Path) -> int:
    """Write the entries to `path`; returns how many were written."""
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        for entry in ledger.entries:
            writer.writerow(
                [entry.date.isoformat(), str(entry.amount), entry.category, entry.description]
            )
    return len(ledger.entries)
