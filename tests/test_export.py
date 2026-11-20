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

    def test_writes_amounts_with_two_decimals(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12.5", "food", "lunch"),
                entry("2026-01-03", "7", "transport", "bus"),
                entry("2026-01-04", "-3.2", "food", "refund"),
                entry("2026-01-05", "0", "other", "zero"),
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.csv"
            write_csv(ledger, out)
            self.assertEqual(
                out.read_text().splitlines()[1:],
                [
                    "2026-01-02,12.50,food,lunch",
                    "2026-01-03,7.00,transport,bus",
                    "2026-01-04,-3.20,food,refund",
                    "2026-01-05,0.00,other,zero",
                ],
            )

    def test_writes_no_thousands_separators(self) -> None:
        ledger = Ledger([entry("2026-01-02", "1234.5", "food", "lunch")])
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.csv"
            write_csv(ledger, out)
            self.assertEqual(
                out.read_text().splitlines()[1], "2026-01-02,1234.50,food,lunch"
            )
            # A grouped amount would be quoted by csv.writer and rejected by
            # Decimal, so the exported text must remain readable input.
            self.assertEqual(read_entries(out)[0].amount, Decimal("1234.50"))

    def test_rounds_amounts_with_more_than_two_decimals(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "1.006", "food", "rounds up"),
                entry("2026-01-03", "1.005", "food", "half to even"),
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.csv"
            write_csv(ledger, out)
            self.assertEqual(
                out.read_text().splitlines()[1:],
                [
                    "2026-01-02,1.01,food,rounds up",
                    "2026-01-03,1.00,food,half to even",
                ],
            )

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
            self.assertIn("2026-01-15,30.00,transport,train", out.read_text())
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
