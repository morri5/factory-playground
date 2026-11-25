import unittest
from decimal import Decimal

from ledgerlite.ledger import Ledger
from ledgerlite.reports import category_counts, category_totals, grand_total, monthly_totals
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

    def test_monthly_totals_include_refunds(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12", "food"),
                entry("2026-01-15", "30", "clothing"),
                entry("2026-01-20", "-60", "clothing"),
                entry("2026-02-01", "5.25", "food"),
                entry("2026-03-01", "-7.50", "clothing"),
            ]
        )
        self.assertEqual(
            monthly_totals(ledger),
            {
                "2026-01": Decimal("-18"),
                "2026-02": Decimal("5.25"),
                "2026-03": Decimal("-7.50"),
            },
        )

    def test_monthly_and_category_totals_agree(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12", "food"),
                entry("2026-01-15", "30", "clothing"),
                entry("2026-01-20", "-60", "clothing"),
                entry("2026-02-01", "5.25", "food"),
            ]
        )
        self.assertEqual(
            sum(monthly_totals(ledger).values(), Decimal("0")),
            sum(category_totals(ledger).values(), Decimal("0")),
        )

    def test_grand_total(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12", "food"),
                entry("2026-01-15", "30", "clothing"),
                entry("2026-01-20", "-60", "clothing"),
                entry("2026-02-01", "5.25", "food"),
            ]
        )
        self.assertEqual(grand_total(ledger), Decimal("-12.75"))

    def test_grand_total_of_empty_ledger(self) -> None:
        self.assertEqual(grand_total(Ledger()), Decimal("0"))

    def test_grand_total_matches_monthly_totals(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12", "food"),
                entry("2026-01-15", "30", "clothing"),
                entry("2026-01-20", "-60", "clothing"),
                entry("2026-02-01", "5.25", "food"),
            ]
        )
        self.assertEqual(
            grand_total(ledger),
            sum(monthly_totals(ledger).values(), Decimal("0")),
        )

    def test_monthly_totals_keep_zero_amounts(self) -> None:
        ledger = Ledger([entry("2026-04-01", "0", "misc")])
        self.assertEqual(monthly_totals(ledger), {"2026-04": Decimal("0")})
        self.assertEqual(category_totals(ledger), {"misc": Decimal("0")})

    def test_category_counts(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12", "food"),
                entry("2026-01-15", "30", "transport"),
                entry("2026-02-01", "5.25", "food"),
            ]
        )
        self.assertEqual(category_counts(ledger), {"food": 2, "transport": 1})
        self.assertEqual(list(category_counts(ledger)), ["food", "transport"])

    def test_category_counts_include_refunds(self) -> None:
        ledger = Ledger(
            [
                entry("2026-01-02", "12", "food"),
                entry("2026-01-15", "30", "clothing"),
                entry("2026-01-20", "-60", "clothing"),
                entry("2026-02-01", "5.25", "food"),
                entry("2026-03-01", "-7.50", "clothing"),
            ]
        )
        self.assertEqual(category_counts(ledger), {"clothing": 3, "food": 2})

    def test_category_counts_of_empty_ledger(self) -> None:
        self.assertEqual(category_counts(Ledger()), {})

    def test_empty_ledger(self) -> None:
        self.assertEqual(monthly_totals(Ledger()), {})
        self.assertEqual(category_totals(Ledger()), {})


if __name__ == "__main__":
    unittest.main()
