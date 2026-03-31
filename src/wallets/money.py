from dataclasses import dataclass, field
from decimal import Decimal
from typing import Self

from src.wallets.exceptions import NegativeValueException, NotComparisonException


@dataclass(slots=True)
class Money:
    value: Decimal
    currency: str = field(default="USD")

    def __post_init__(self) -> None:
        if self.value < 0:
            raise NegativeValueException

        self.value = Decimal(str(self.value))

    def __eq__(self, other: "Money") -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self.currency == other.currency and self.value == other.value

    def __add__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise NotComparisonException
        return Money(self.value + other.value, self.currency)

    def __sub__(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise NotComparisonException
        return Money(self.value - other.value, self.currency)


@dataclass
class Wallet:
    _balances: dict[str, Money] = field(default_factory=dict, init=False, repr=False)

    def __init__(self, *moneys: Money) -> None:
        self._balances = {}
        for money in moneys:
            self._balances[money.currency] = money

    def __getitem__(self, currency: str) -> Money:
        if currency in self._balances:
            return self._balances[currency]
        return Money(value=0.0, currency=currency)

    def __delitem__(self, currency: str) -> None:
        if currency in self._balances:
            del self._balances[currency]

    @property
    def currencies(self) -> list[str]:
        return list(self._balances.keys())

    def __len__(self) -> int:
        return len(self._balances)

    def __contains__(self, currency: str) -> bool:
        return currency in self._balances

    def add(self, money: Money) -> Self:
        cur = money.currency
        if cur in self._balances:
            new_value = self._balances[cur].value + money.value
            self._balances[cur] = Money(value=new_value, currency=cur)
        else:
            self._balances[cur] = Money(value=money.value, currency=cur)
        return self

    def sub(self, money: Money) -> Self:
        cur = money.currency
        current = self[cur].value
        new_value = current - money.value
        if new_value < 0:
            raise NegativeValueException
        self._balances[cur] = Money(value=new_value, currency=cur)
        return self
