import unittest

from ledgerlite.ledger import Ledger
from tests.helpers import entry


class LedgerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.ledger = Ledger(
            [
                entry("2026-02-01", "5", "food"),
                entry("2026-01-15", "30", "transport"),
                entry("2026-01-02", "12", "food"),
            ]
        )

    def test_sorted_by_date(self) -> None:
        days = [e.date.isoformat() for e in self.ledger.entries]
        self.assertEqual(days, ["2026-01-02", "2026-01-15", "2026-02-01"])

    def test_add_keeps_order(self) -> None:
        self.ledger.add(entry("2026-01-01", "1", "misc"))
        self.assertEqual(self.ledger.entries[0].category, "misc")

    def test_categories(self) -> None:
        self.assertEqual(self.ledger.categories(), ["food", "transport"])

    def test_in_category_ignores_case(self) -> None:
        self.assertEqual(len(self.ledger.in_category("FOOD").entries), 2)

    def test_in_month(self) -> None:
        self.assertEqual(len(self.ledger.in_month("2026-01").entries), 2)


if __name__ == "__main__":
    unittest.main()
