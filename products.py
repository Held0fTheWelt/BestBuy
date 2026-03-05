class Product:
    """Represents a product in the store with name, price, and quantity."""

    def __init__(self, name: str, price: float, quantity: int):
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

    def get_quantity(self) -> int:
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity = quantity
        if self._quantity == 0:
            self.deactivate()

    def is_active(self) -> bool:
        return self._active

    def activate(self) -> None:
        self._active = True

    def deactivate(self) -> None:
        self._active = False

    def show(self) -> None:
        print(f"{self._name}, Price: {self._price}, Quantity: {self._quantity}")

    def buy(self, quantity: int) -> float:
        if not self._active:
            raise Exception("Cannot buy an inactive product")
        if quantity <= 0:
            raise Exception("Quantity to buy must be positive")
        if quantity > self._quantity:
            raise Exception("Not enough quantity in stock")

        self._quantity -= quantity
        if self._quantity == 0:
            self.deactivate()
        return self._price * quantity


def main():
    bose = Product("Bose QuietComfort Earbuds", price=250, quantity=500)
    mac = Product("MacBook Air M2", price=1450, quantity=100)

    print(bose.buy(50))
    print(mac.buy(100))
    print(mac.is_active())

    bose.show()
    mac.show()

    bose.set_quantity(1000)
    bose.show()


if __name__ == "__main__":
    main()
