"""Totals per month, per category, and overall."""

from collections import Counter, defaultdict
from decimal import Decimal

from ledgerlite.ledger import Ledger


def monthly_totals(ledger: Ledger) -> dict[str, Decimal]:
    """Net total per month (YYYY-MM), oldest first."""
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for entry in ledger.entries:
        totals[entry.month] += entry.amount
    return dict(sorted(totals.items()))


def category_totals(ledger: Ledger) -> dict[str, Decimal]:
    """Net total per category, largest first."""
    totals: dict[str, Decimal] = defaultdict(Decimal)
    for entry in ledger.entries:
        totals[entry.category] += entry.amount
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def category_counts(ledger: Ledger) -> dict[str, int]:
    """Number of entries per category, alphabetically by category."""
    counts = Counter(entry.category for entry in ledger.entries)
    return dict(sorted(counts.items()))


def grand_total(ledger: Ledger) -> Decimal:
    """Net total across every entry, refunds included."""
    return sum((entry.amount for entry in ledger.entries), Decimal("0"))
