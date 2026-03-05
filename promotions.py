"""Promotion types for store products."""

from abc import ABC, abstractmethod


class Promotion(ABC):
    """Abstract base class for product promotions."""

    def __init__(self, name: str):
        """Create a promotion with the given name."""
        self._name = name

    @property
    def name(self) -> str:
        """Return the promotion name."""
        return self._name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        """
        Return the discounted total price for the given product and quantity.
        product: a Product instance (or subclass); use product._price for unit price.
        quantity: number of units.
        """
        pass


class PercentDiscount(Promotion):
    """Percentage discount (e.g. 20% off)."""

    def __init__(self, name: str, percent: float):
        """Create a percent discount. percent is e.g. 30 for 30% off."""
        super().__init__(name)
        if not 0 < percent <= 100:
            raise ValueError("Percent must be between 0 and 100")
        self._percent = percent

    def apply_promotion(self, product, quantity: int) -> float:
        """Return price after percentage discount."""
        total = product._price * quantity
        return total * (1 - self._percent / 100)


class SecondHalfPrice(Promotion):
    """Second item at half price (per pair)."""

    def apply_promotion(self, product, quantity: int) -> float:
        """For every two items, first full price, second half price."""
        price = product._price
        pairs = quantity // 2
        remainder = quantity % 2
        return pairs * (price + price * 0.5) + remainder * price


class ThirdOneFree(Promotion):
    """Buy 2, get 1 free (pay for 2 out of every 3)."""

    def apply_promotion(self, product, quantity: int) -> float:
        """For every three items, pay for two."""
        price = product._price
        triplets = quantity // 3
        remainder = quantity % 3
        return triplets * (2 * price) + remainder * price
