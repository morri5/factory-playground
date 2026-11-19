import tempfile
import unittest
from pathlib import Path

from ledgerlite.export import write_csv
from ledgerlite.ledger import Ledger
from tests.helpers import entry


class ExportTest(unittest.TestCase):
    def test_writes_one_row_per_entry(self) -> None:
        ledger = Ledger([entry("2026-01-02", "12.50", "food", "lunch")])
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.csv"
            self.assertEqual(write_csv(ledger, out), 1)
            self.assertIn("2026-01-02,12.50,food,lunch", out.read_text())


if __name__ == "__main__":
    unittest.main()
