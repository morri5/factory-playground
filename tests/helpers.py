import datetime
from decimal import Decimal

from ledgerlite.models import Entry


def entry(day: str, amount: str, category: str, description: str = "") -> Entry:
    return Entry(datetime.date.fromisoformat(day), Decimal(amount), category, description)
