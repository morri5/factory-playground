import unittest
from decimal import Decimal

from ledgerlite.ledger import Ledger
from ledgerlite.reports import category_totals, monthly_totals
from tests.helpers import entry


class ReportsTest(unittest.TestCase):
    def test_monthly_totals(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12", "food"),
                entry("2026-01-15", "30", "transport"),
                entry("2026-02-01", "5.25", "food"),
            ]
        )
        self.assertEqual(
            monthly_totals(ledger), {"2026-01": Decimal("42"), "2026-02": Decimal("5.25")}
        )

    def test_category_totals_largest_first(self) -> None:
        ledger = Ledger([entry("2026-01-02", "12", "food"), entry("2026-01-15", "30", "rent")])
        self.assertEqual(list(category_totals(ledger)), ["rent", "food"])

    def test_empty_ledger(self) -> None:
        self.assertEqual(monthly_totals(Ledger()), {})
        self.assertEqual(category_totals(Ledger()), {})


if __name__ == "__main__":
    unittest.main()
