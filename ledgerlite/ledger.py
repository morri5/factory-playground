"""The ledger: entries plus the queries the reports need."""

from collections.abc import Iterable

from ledgerlite.models import Entry


class Ledger:
    def __init__(self, entries: Iterable[Entry] = ()) -> None:
        self.entries: list[Entry] = sorted(entries, key=lambda e: e.date)

    def add(self, entry: Entry) -> None:
        self.entries.append(entry)
        self.entries.sort(key=lambda e: e.date)

    def categories(self) -> list[str]:
        return sorted({e.category for e in self.entries})

    def in_category(self, category: str) -> "Ledger":
        return Ledger(e for e in self.entries if e.category == category.lower())

    def in_month(self, month: str) -> "Ledger":
        return Ledger(e for e in self.entries if e.month == month)
