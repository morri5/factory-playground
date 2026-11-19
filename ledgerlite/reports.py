"""Totals per month and per category."""

from collections import defaultdict
from decimal import Decimal

from ledgerlite.ledger import Ledger


def monthly_totals(ledger: Ledger) -> dict[str, Decimal]:
    """Spending per month (YYYY-MM), oldest first."""
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for entry in ledger.entries:
        if entry.amount > 0:
            totals[entry.month] += entry.amount
    return dict(sorted(totals.items()))


def category_totals(ledger: Ledger) -> dict[str, Decimal]:
    """Spending per category, largest first."""
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for entry in ledger.entries:
        totals[entry.category] += entry.amount
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))
