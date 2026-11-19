"""Plain-text tables for the CLI."""

from decimal import Decimal


def money(amount: Decimal) -> str:
    return f"{amount:,.2f}"


def table(rows: dict[str, Decimal], title: str) -> str:
    if not rows:
        return f"{title}\n(no entries)"
    width = max(len(key) for key in rows)
    lines = [title] + [f"{key.ljust(width)}  {money(value):>12}" for key, value in rows.items()]
    return "\n".join(lines)
