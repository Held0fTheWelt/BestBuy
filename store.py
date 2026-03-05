from typing import List

import products
from products import Product


class Store:
    """Holds products and allows ordering multiple products at once."""

    def __init__(self, product_list: List[Product]):
        """Create a store with the given list of products."""
        self._products = list(product_list)

    def add_product(self, product: Product) -> None:
        """Add a product to the store."""
        self._products.append(product)

    def remove_product(self, product: Product) -> None:
        """Remove a product from the store."""
        self._products.remove(product)

    @property
    def total_quantity(self) -> int:
        """Total number of items in the store."""
        return sum(p.quantity for p in self._products)

    @property
    def all_products(self) -> List[Product]:
        """All active products."""
        return [p for p in self._products if p.is_active]

    def __contains__(self, product: Product) -> bool:
        """Support 'product in store'."""
        return product in self._products

    def __add__(self, other: "Store") -> "Store":
        """Combine two stores; returns a new Store with products from both."""
        if not isinstance(other, Store):
            return NotImplemented
        combined = list(self._products) + list(other._products)
        return Store(combined)

    def order(self, shopping_list: List[tuple]) -> float:
        """Process order (list of (product, quantity)) and return total price."""
        total = 0.0
        for product, quantity in shopping_list:
            if product not in self._products:
                raise ValueError("Product not in store")
            total += product.buy(quantity)
        return total


def main():
    """Demo: create store, get products, place order."""
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
    ]

    best_buy = Store(product_list)
    products_list = best_buy.all_products
    print(best_buy.total_quantity)
    print(best_buy.order([(products_list[0], 1), (products_list[1], 2)]))


if __name__ == "__main__":
    main()
