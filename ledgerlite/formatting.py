"""Plain-text tables for the CLI."""

from decimal import Decimal


def money(amount: Decimal) -> str:
    return f"{amount:,.2f}"


def table(
    rows: dict[str, Decimal], title: str, total: Decimal | None = None
) -> str:
    width = max((len(key) for key in rows), default=0)
    if total is not None:
        width = max(width, len("Total"))
    if rows:
        lines = [title] + [
            f"{key.ljust(width)}  {money(value):>12}" for key, value in rows.items()
        ]
    else:
        lines = [title, "(no entries)"]
    if total is not None:
        lines.append(f"{'Total'.ljust(width)}  {money(total):>12}")
    return "\n".join(lines)


def counts(rows: dict[str, int]) -> str:
    """One `name  count` line per row, with both columns aligned."""
    width = max((len(key) for key in rows), default=0)
    count_width = max((len(str(value)) for value in rows.values()), default=0)
    return "\n".join(
        f"{key.ljust(width)}  {str(value).rjust(count_width)}"
        for key, value in rows.items()
    )
