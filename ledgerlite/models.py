"""The ledger entry."""

import datetime
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Entry:
    """One line of the ledger. A negative amount is a refund."""

    date: datetime.date
    amount: Decimal
    category: str
    description: str = ""

    @property
    def month(self) -> str:
        """The entry's month as YYYY-MM."""
        return self.date.strftime("%Y-%m")
