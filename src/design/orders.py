import abc
from dataclasses import dataclass
from typing import Type

__all__ = (
    "Order",
    "DefaultDiscountGetter",
    "DiscountApplier",
)


@dataclass
class Order:
    """There is no need to describe anything here."""


class Discount(abc.ABC):
    """
    Maybe it's better manipulate with only prices instead of order.
    Maybe discount don't need know anything about order  and cat get only price, return final price.
    """

    def __init__(self, order: Order):
        self.order = order

    @abc.abstractmethod
    def apply(self):
        pass


class PercentDiscount(Discount):
    def apply(self):
        pass


class FixDiscount(Discount):
    def apply(self):
        pass


class LoyaltyDiscount(Discount):
    def apply(self):
        pass


class DiscountGetter(abc.ABC):
    def __init__(self, order: Order):
        self.order = order

    @abc.abstractmethod
    def get_discount_classes(self) -> list[Discount]:
        pass


class DefaultDiscountGetter(DiscountGetter):
    def get_discount_classes(self) -> list[Discount]:
        pass


class DiscountApplier:
    def __init__(self, order: Order, discount_classes: list[Type[Discount]]):
        self.order = order
        self.discount_classes = discount_classes

    def apply(self):
        for cls in self.discount_classes:
            discount = cls(self.order)
            discount.apply()
