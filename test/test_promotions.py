"""Pytest tests for promotion classes."""

import pytest

from products import Product
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree


def _product(price: float = 100.0, quantity: int = 1000):
    """Helper: product with given price and quantity for promotion tests."""
    return Product("TestProduct", price=price, quantity=quantity)


# --- PercentDiscount ---


def test_percent_discount_creation():
    """PercentDiscount has name and percent."""
    prom = PercentDiscount("20% off", percent=20)
    assert prom.name == "20% off", "Name should be set"


def test_percent_discount_apply_promotion():
    """apply_promotion returns price reduced by percent."""
    prom = PercentDiscount("30% off", percent=30)
    product = _product(price=100)
    assert prom.apply_promotion(product, 1) == 70.0, "1 item: 100 * 0.7 = 70"
    assert prom.apply_promotion(product, 2) == 140.0, "2 items: 200 * 0.7 = 140"
    assert prom.apply_promotion(product, 10) == 700.0, "10 items: 1000 * 0.7 = 700"


def test_percent_discount_100_percent():
    """100% off means free."""
    prom = PercentDiscount("Free", percent=100)
    product = _product(price=50)
    assert prom.apply_promotion(product, 3) == 0.0, "100% off should be 0"


def test_percent_discount_invalid_percent_raises():
    """Percent outside 0-100 raises ValueError."""
    with pytest.raises(ValueError, match="Percent must be between 0 and 100"):
        PercentDiscount("Bad", percent=0)
    with pytest.raises(ValueError, match="Percent must be between 0 and 100"):
        PercentDiscount("Bad", percent=101)
    with pytest.raises(ValueError, match="Percent must be between 0 and 100"):
        PercentDiscount("Bad", percent=-10)


# --- SecondHalfPrice ---


def test_second_half_price_creation():
    """SecondHalfPrice has name."""
    prom = SecondHalfPrice("Second Half price!")
    assert prom.name == "Second Half price!", "Name should be set"


def test_second_half_price_apply_one_item():
    """One item: full price."""
    prom = SecondHalfPrice("Second Half price!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 1) == 100.0, "1 item = full price"


def test_second_half_price_apply_two_items():
    """Two items: first full, second half = 1.5 * price."""
    prom = SecondHalfPrice("Second Half price!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 2) == 150.0, "2 items = 100 + 50 = 150"


def test_second_half_price_apply_four_items():
    """Four items: two pairs."""
    prom = SecondHalfPrice("Second Half price!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 4) == 300.0, "4 items = 2 * 150 = 300"


def test_second_half_price_apply_three_items():
    """Three items: one pair + one full."""
    prom = SecondHalfPrice("Second Half price!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 3) == 250.0, "3 items = 150 + 100 = 250"


# --- ThirdOneFree ---


def test_third_one_free_creation():
    """ThirdOneFree has name."""
    prom = ThirdOneFree("Third One Free!")
    assert prom.name == "Third One Free!", "Name should be set"


def test_third_one_free_apply_one_or_two():
    """One or two items: pay full for each."""
    prom = ThirdOneFree("Third One Free!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 1) == 100.0, "1 item = 100"
    assert prom.apply_promotion(product, 2) == 200.0, "2 items = 200"


def test_third_one_free_apply_three_items():
    """Three items: pay for two."""
    prom = ThirdOneFree("Third One Free!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 3) == 200.0, "3 items = pay for 2 = 200"


def test_third_one_free_apply_six_items():
    """Six items: two triplets, pay for four."""
    prom = ThirdOneFree("Third One Free!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 6) == 400.0, "6 items = 4 * 100 = 400"


def test_third_one_free_apply_four_items():
    """Four items: one triplet + one full."""
    prom = ThirdOneFree("Third One Free!")
    product = _product(price=100)
    assert prom.apply_promotion(product, 4) == 300.0, "4 items = 200 + 100 = 300"
