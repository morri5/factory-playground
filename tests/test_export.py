import datetime
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from ledgerlite.export import write_csv
from ledgerlite.ledger import Ledger
from ledgerlite.parser import read_entries
from tests.helpers import entry


class ExportTest(unittest.TestCase):
    def test_writes_one_row_per_entry(self) -> None:
        ledger = Ledger([entry("2026-01-02", "12.50", "food", "lunch")])
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.csv"
            self.assertEqual(write_csv(ledger, out), 1)
            lines = out.read_text().splitlines()
            self.assertEqual(lines[0], "date,amount,category,description")
            self.assertEqual(len(lines), 2)
            self.assertIn("2026-01-02,12.50,food,lunch", out.read_text())

    def test_round_trips_through_parser(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-15", "30", "transport", "train"),
                entry("2026-01-02", "12.50", "food", "lunch, with comma"),
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.csv"
            self.assertEqual(write_csv(ledger, out), 2)
            self.assertEqual(
                [
                    (e.date, e.amount, e.category, e.description)
                    for e in read_entries(out)
                ],
                [
                    (datetime.date(2026, 1, 2), Decimal("12.50"), "food", "lunch, with comma"),
                    (datetime.date(2026, 1, 15), Decimal("30"), "transport", "train"),
                ],
            )

    def test_empty_ledger_exports_readable_header(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.csv"
            self.assertEqual(write_csv(Ledger(), out), 0)
            self.assertEqual(
                out.read_text().splitlines(), ["date,amount,category,description"]
            )
            self.assertEqual(read_entries(out), [])


if __name__ == "__main__":
    unittest.main()
