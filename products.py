class PurchaseError(Exception):
    """Raised when a purchase cannot be completed (inactive, invalid or insufficient quantity)."""


class Product:
    """Represents a product in the store with name, price, and quantity."""

    def __init__(self, name: str, price: float, quantity: int):
        """Create a product. Raises ValueError for empty name, negative price or quantity."""
        if not name or not name.strip():
            raise ValueError("Name cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")

        self._name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._promotion = None

    @property
    def name(self) -> str:
        """Product name."""
        return self._name

    @property
    def price(self) -> float:
        """Product unit price."""
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """Set unit price. Raises ValueError if negative."""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = value

    @property
    def quantity(self) -> int:
        """Current quantity in stock."""
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Set quantity; deactivates product if quantity becomes 0."""
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = value
        if self._quantity == 0:
            self.deactivate()

    @property
    def promotion(self):
        """Current promotion, or None."""
        return self._promotion

    @promotion.setter
    def promotion(self, value) -> None:
        """Set promotion. Pass None to remove."""
        self._promotion = value

    @property
    def is_active(self) -> bool:
        """True if the product is active."""
        return self._active

    def activate(self) -> None:
        """Activate the product."""
        self._active = True

    def deactivate(self) -> None:
        """Deactivate the product."""
        self._active = False

    def __str__(self) -> str:
        """String representation: Name, Price: $X Quantity:Y."""
        line = f"{self._name}, Price: ${self._price} Quantity:{self._quantity}"
        if self._promotion is not None:
            line += f", Promotion: {self._promotion.name}"
        return line

    def show(self) -> None:
        """Print a string representation of the product."""
        print(self)

    def __gt__(self, other) -> bool:
        """Compare by price: self > other."""
        if not isinstance(other, Product):
            return NotImplemented
        return self._price > other._price

    def __lt__(self, other) -> bool:
        """Compare by price: self < other."""
        if not isinstance(other, Product):
            return NotImplemented
        return self._price < other._price

    def buy(self, quantity: int) -> float:
        """Buy the given quantity. Returns total price. Raises PurchaseError if invalid."""
        if not self._active:
            raise PurchaseError("Cannot buy an inactive product")
        if quantity <= 0:
            raise PurchaseError("Quantity to buy must be positive")
        if quantity > self._quantity:
            raise PurchaseError("Not enough quantity in stock")

        self._quantity -= quantity
        if self._quantity == 0:
            self.deactivate()
        if self._promotion is not None:
            return self._promotion.apply_promotion(self, quantity)
        return self._price * quantity


class NonStockedProduct(Product):
    """Product with no physical stock; quantity is always 0."""

    def __init__(self, name: str, price: float):
        """Create a non-stocked product. Quantity is always 0."""
        super().__init__(name, price, 0)

    @property
    def quantity(self) -> int:
        """Non-stocked products always have quantity 0."""
        return 0

    @quantity.setter
    def quantity(self, value: int) -> None:
        """Non-stocked products: quantity must remain 0."""
        if value != 0:
            raise ValueError("Non-stocked product quantity must remain 0")

    def buy(self, quantity: int) -> float:
        """Buy the given quantity. Does not reduce stock (always 0)."""
        if not self._active:
            raise PurchaseError("Cannot buy an inactive product")
        if quantity <= 0:
            raise PurchaseError("Quantity to buy must be positive")
        if self._promotion is not None:
            return self._promotion.apply_promotion(self, quantity)
        return self._price * quantity

    def __str__(self) -> str:
        """String representation; indicates non-stocked."""
        line = f"{self._name}, Price: ${self._price} Quantity: 0 (Non-stocked)"
        if self._promotion is not None:
            line += f", Promotion: {self._promotion.name}"
        return line


class LimitedProduct(Product):
    """Product that can only be purchased up to a maximum quantity per order."""

    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """Create a limited product. maximum is the max quantity per order."""
        super().__init__(name, price, quantity)
        if maximum <= 0:
            raise ValueError("Maximum must be positive")
        self._maximum = maximum

    def buy(self, quantity: int) -> float:
        """Buy the given quantity. Raises if quantity exceeds maximum per order."""
        if quantity > self._maximum:
            raise PurchaseError(
                f"Quantity {quantity} exceeds maximum per order ({self._maximum})"
            )
        return super().buy(quantity)

    def __str__(self) -> str:
        """String representation; indicates maximum per order."""
        line = (
            f"{self._name}, Price: ${self._price} Quantity: {self._quantity}, "
            f"Maximum per order: {self._maximum}"
        )
        if self._promotion is not None:
            line += f", Promotion: {self._promotion.name}"
        return line


def main():
    """Demo: create products, buy, show, set quantity."""
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active)

    print(bose)
    print(mac)

    bose.quantity = 1000
    print(bose)


if __name__ == "__main__":
    main()
