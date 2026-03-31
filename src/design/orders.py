from abc import ABC, abstractmethod
from dataclasses import dataclass, field


class Discount(ABC):
    """Абстрактная скидка"""

    @abstractmethod
    def apply(self, amount: float) -> float:
        """Применяет скидку к заданной сумме и возвращает новую сумму"""


class FixedDiscount(Discount):
    """Фиксированная скидка"""

    def __init__(self, amount_off: float):
        self.amount_off = amount_off

    def apply(self, amount: float) -> float:
        return max(0, amount - self.amount_off)


class PercentageDiscount(Discount):
    """Процентная скидка"""

    def __init__(self, percent: float):
        self.percent = percent

    def apply(self, amount: float) -> float:
        return amount * (1 - self.percent / 100)


class LoyaltyDiscount(Discount):
    """Скидка за лояльность"""

    def __init__(self, percent: float = 5):
        self.percent = percent

    def apply(self, amount: float) -> float:
        return amount * (1 - self.percent / 100)


@dataclass
class Order:
    order_id: int
    customer_name: str
    items: list[dict]
    is_loyal: bool = field(default=False)

    @property
    def total_amount(self) -> float:
        """Исходная сумма заказа без скидок"""
        return sum(item["price"] for item in self.items)

    def get_applicable_discounts(self) -> list[Discount]:
        """Формирует список скидок"""
        discounts = []
        total = self.total_amount

        # Пример: если сумма заказа больше 5000, даём фиксированную скидку 300
        if total > 5000:
            discounts.append(FixedDiscount(300))

        # Пример: если постоянный покупатель, даём скидку за лояльность 5%
        if self.is_loyal:
            discounts.append(LoyaltyDiscount(5))

        # Пример: скидка 10%, если есть товар с именем "Laptop"
        if any(item["name"].lower() == "laptop" for item in self.items):
            discounts.append(PercentageDiscount(10))

        return discounts

    def apply_discounts(self, discounts: list[Discount] | None = None) -> float:
        """
        Применяет переданный список скидок к заказу.
        """
        if discounts is None:
            discounts = self.get_applicable_discounts()

        final_amount = self.total_amount
        for discount in discounts:
            final_amount = discount.apply(final_amount)
        return final_amount


if __name__ == "__main__":
    order1 = Order(
        order_id=1,
        customer_name="Иван Петров",
        items=[{"name": "Телефон", "price": 15000}, {"name": "Чехол", "price": 500}],
        is_loyal=True,  # постоянный покупатель
    )

    print(f"Исходная сумма: {order1.total_amount} руб.")
    print("Автоматически выбранные скидки:")
    for d in order1.get_applicable_discounts():
        print(f"  {d.__class__.__name__}")

    final = order1.apply_discounts()
    print(f"Итоговая сумма после всех скидок: {final:.2f} руб.")

    # Пример ручного применения конкретного набора скидок
    manual_discounts = [FixedDiscount(200), PercentageDiscount(10)]
    final_manual = order1.apply_discounts(manual_discounts)
    print(f"После фикс. 200 руб. + 10%: {final_manual:.2f} руб.")
