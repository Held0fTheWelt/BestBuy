from typing import List

import products
from products import Product


class Store:
    """Holds products and allows ordering multiple products at once."""

    def __init__(self, product_list: List[Product]):
        self._products = list(product_list)

    def add_product(self, product: Product) -> None:
        self._products.append(product)

    def remove_product(self, product: Product) -> None:
        self._products.remove(product)

    def get_total_quantity(self) -> int:
        return sum(p.get_quantity() for p in self._products)

    def get_all_products(self) -> List[Product]:
        return [p for p in self._products if p.is_active()]

    def order(self, shopping_list: List[tuple]) -> float:
        total = 0.0
        for product, quantity in shopping_list:
            total += product.buy(quantity)
        return total


def main():
    product_list = [
        products.Product("MacBook Air M2", price=1450, quantity=100),
        products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        products.Product("Google Pixel 7", price=500, quantity=250),
    ]

    best_buy = Store(product_list)
    products_list = best_buy.get_all_products()
    print(best_buy.get_total_quantity())
    print(best_buy.order([(products_list[0], 1), (products_list[1], 2)]))


if __name__ == "__main__":
    main()
