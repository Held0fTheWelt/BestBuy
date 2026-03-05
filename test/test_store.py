import unittest

import products
from store import Store


class TestStore(unittest.TestCase):
    """Functionality tests for Store, including edge cases."""

    def test_order_quantity_too_large_raises_and_leaves_quantity_unchanged(self):
        """Ordering more than in stock raises; product quantity is not modified."""
        p = products.Product("Item", price=10, quantity=5)
        s = Store([p])
        with self.assertRaises(Exception):
            s.order([(p, 10)])
        self.assertEqual(p.quantity, 5)

    def test_product_runs_out_of_stock_after_order(self):
        """When an order exhausts stock, product becomes inactive and is excluded from get_all_products."""
        p = products.Product("Item", price=10, quantity=3)
        s = Store([p])
        self.assertEqual(s.total_quantity, 3)
        total = s.order([(p, 3)])
        self.assertEqual(total, 30.0)
        self.assertEqual(p.quantity, 0)
        self.assertFalse(p.is_active)
        self.assertEqual(s.all_products, [])
        self.assertEqual(s.total_quantity, 0)

    def test_order_mixed_success_second_item_too_large(self):
        """If second item in order has quantity too large, first is already bought; order raises."""
        p1 = products.Product("A", price=10, quantity=10)
        p2 = products.Product("B", price=20, quantity=2)
        s = Store([p1, p2])
        with self.assertRaises(Exception):
            s.order([(p1, 2), (p2, 5)])
        self.assertEqual(p1.quantity, 8)
        self.assertEqual(p2.quantity, 2)

    def test_product_in_store(self):
        """'product in store' works via __contains__."""
        p = products.Product("A", price=10, quantity=5)
        s = Store([p])
        self.assertIn(p, s)
        other = products.Product("B", price=20, quantity=5)
        self.assertNotIn(other, s)

    def test_store_add_combines_stores(self):
        """store1 + store2 returns new Store with products from both."""
        p1 = products.Product("A", price=10, quantity=10)
        p2 = products.Product("B", price=20, quantity=20)
        s1 = Store([p1])
        s2 = Store([p2])
        combined = s1 + s2
        self.assertEqual(combined.total_quantity, 30)
        self.assertEqual(len(combined.all_products), 2)
        self.assertIn(p1, combined)
        self.assertIn(p2, combined)


if __name__ == "__main__":
    unittest.main()
