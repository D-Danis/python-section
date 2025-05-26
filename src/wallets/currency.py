import enum
from dataclasses import dataclass

__all__ = ("AvailableCurrency", "Currency", "rub", "usd")


class AvailableCurrency(enum.Enum):
    RUB = enum.auto()
    USD = enum.auto()


@dataclass(slots=True, frozen=True, eq=True, repr=True)
class Currency:
    code: AvailableCurrency


rub = RUB(code=AvailableCurrency.RUB)
usd = USD(code=AvailableCurrency.USD)

