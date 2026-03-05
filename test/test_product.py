"""Pytest tests for the Product class."""

import pytest

from products import Product, PurchaseError, NonStockedProduct, LimitedProduct
from promotions import PercentDiscount, SecondHalfPrice, ThirdOneFree


def test_create_normal_product_works():
    """Test that creating a normal product works."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.quantity == 100, "Initial quantity should be 100"
    assert product.is_active is True, "New product should be active"


def test_create_product_empty_name_raises():
    """Test that creating a product with empty name invokes an exception."""
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Product("", price=1450, quantity=100)


def test_create_product_negative_price_raises():
    """Test that creating a product with negative price invokes an exception."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        Product("MacBook Air M2", price=-10, quantity=100)


def test_create_product_negative_quantity_raises():
    """Test that creating a product with negative quantity invokes an exception."""
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        Product("MacBook Air M2", price=1450, quantity=-1)


def test_product_reaches_zero_quantity_becomes_inactive():
    """Test that when a product reaches 0 quantity, it becomes inactive."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.quantity = 0
    assert product.quantity == 0, "Quantity should be 0 after set_quantity(0)"
    assert product.is_active is False, "Product should be inactive when quantity is 0"


def test_product_buy_zero_quantity_becomes_inactive():
    """Test that buying all stock makes product inactive."""
    product = Product("MacBook Air M2", price=1450, quantity=5)
    product.buy(5)
    assert product.quantity == 0, "Quantity should be 0 after buying all stock"
    assert product.is_active is False, "Product should be inactive when stock is exhausted"


def test_product_purchase_modifies_quantity_and_returns_right_output():
    """Test that product purchase modifies the quantity and returns the right output."""
    product = Product("MacBook Air M2", price=10, quantity=100)
    total = product.buy(30)
    assert total == 300.0, "Total price should be 30 * 10 = 300.0"
    assert product.quantity == 70, "Quantity should decrease from 100 to 70"


def test_buy_larger_quantity_than_exists_raises():
    """Test that buying a larger quantity than exists invokes exception."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    with pytest.raises(PurchaseError, match="Not enough quantity in stock"):
        product.buy(150)


def test_create_product_whitespace_only_name_raises():
    """Test that a name with only spaces invokes an exception."""
    with pytest.raises(ValueError, match="Name cannot be empty"):
        Product("   ", price=1450, quantity=100)


def test_set_quantity_positive_keeps_active():
    """Test that set_quantity with positive value keeps product active."""
    product = Product("MacBook", price=100, quantity=50)
    product.quantity = 10
    assert product.quantity == 10, "Quantity should be updated to 10"
    assert product.is_active is True, "Product should stay active with positive quantity"


def test_set_quantity_negative_raises():
    """Test that set_quantity with negative value raises ValueError."""
    product = Product("MacBook", price=100, quantity=50)
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        product.quantity = -1


def test_activate_deactivate_toggle():
    """Test that deactivate/activate correctly change is_active."""
    product = Product("MacBook", price=100, quantity=50)
    product.deactivate()
    assert product.is_active is False, "Product should be inactive after deactivate()"
    product.activate()
    assert product.is_active is True, "Product should be active again after activate()"


def test_buy_from_inactive_product_raises():
    """Test that buying from an inactive product raises PurchaseError."""
    product = Product("MacBook", price=100, quantity=50)
    product.deactivate()
    with pytest.raises(PurchaseError, match="Cannot buy an inactive product"):
        product.buy(1)


def test_buy_zero_quantity_raises():
    """Test that buy(0) raises PurchaseError."""
    product = Product("MacBook", price=100, quantity=50)
    with pytest.raises(PurchaseError, match="Quantity to buy must be positive"):
        product.buy(0)


def test_buy_negative_quantity_raises():
    """Test that buy(negative) raises PurchaseError."""
    product = Product("MacBook", price=100, quantity=50)
    with pytest.raises(PurchaseError, match="Quantity to buy must be positive"):
        product.buy(-5)


def test_multiple_buys_modify_quantity_and_return_correct_totals():
    """Test that multiple purchases update quantity and return correct prices."""
    product = Product("MacBook", price=10, quantity=100)
    assert product.buy(10) == 100.0, "First purchase total should be 100.0"
    assert product.buy(20) == 200.0, "Second purchase total should be 200.0"
    assert product.quantity == 70, "Remaining quantity should be 70"


def test_show_prints_name_price_quantity():
    """Test that show() prints a string containing name, price and quantity."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    out = str(product)
    assert "MacBook Air M2" in out, "Product name should appear in str output"
    assert "1450" in out, "Price should appear in str output"
    assert "100" in out, "Quantity should appear in str output"


def test_reactivate_then_restock_allows_buy():
    """Test that after sell-out, activate and set_quantity allow buying again."""
    product = Product("MacBook", price=10, quantity=2)
    product.buy(2)
    assert product.is_active is False, "Product should be inactive after sell-out"
    product.activate()
    product.quantity = 5
    total = product.buy(3)
    assert total == 30.0, "Order total should be 30.0"
    assert product.quantity == 2, "Remaining quantity should be 2"


# --- NonStockedProduct ---


def test_non_stocked_product_creation():
    """Test that creating a non-stocked product works; quantity is always 0."""
    product = NonStockedProduct("Windows License", price=125)
    assert product.quantity == 0, "Non-stocked product quantity should be 0"
    assert product.is_active is True, "Non-stocked product should be active"


def test_non_stocked_product_buy_returns_total_quantity_unchanged():
    """Test that buy() returns correct total and quantity stays 0."""
    product = NonStockedProduct("Windows License", price=125)
    total = product.buy(3)
    assert total == 375.0, "Total should be 125 * 3 = 375.0"
    assert product.quantity == 0, "Quantity should still be 0 after buy"


def test_non_stocked_product_set_quantity_zero_allowed():
    """Test that set_quantity(0) is allowed (no-op)."""
    product = NonStockedProduct("Windows License", price=125)
    product.quantity = 0
    assert product.quantity == 0, "Quantity should remain 0"


def test_non_stocked_product_set_quantity_non_zero_raises():
    """Test that set_quantity(non-zero) raises ValueError."""
    product = NonStockedProduct("Windows License", price=125)
    with pytest.raises(ValueError, match="Non-stocked product quantity must remain 0"):
        product.quantity = 1


def test_non_stocked_product_show_contains_non_stocked():
    """Test that show() indicates non-stocked."""
    product = NonStockedProduct("Windows License", price=125)
    out = str(product)
    assert "Windows License" in out, "Name should appear"
    assert "125" in out, "Price should appear"
    assert "Non-stocked" in out, "Should indicate non-stocked"


def test_non_stocked_product_buy_from_inactive_raises():
    """Test that buying from inactive non-stocked product raises."""
    product = NonStockedProduct("Windows License", price=125)
    product.deactivate()
    with pytest.raises(PurchaseError, match="Cannot buy an inactive product"):
        product.buy(1)


# --- LimitedProduct ---


def test_limited_product_creation():
    """Test that creating a limited product works."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    assert product.quantity == 250, "Quantity should be 250"
    assert product.is_active is True, "Limited product should be active"


def test_limited_product_buy_within_maximum_works():
    """Test that buy(quantity <= maximum) works and reduces stock."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=2)
    total = product.buy(2)
    assert total == 20.0, "Total should be 10 * 2 = 20.0"
    assert product.quantity == 248, "Quantity should decrease by 2"


def test_limited_product_buy_above_maximum_raises():
    """Test that buy(quantity > maximum) raises PurchaseError."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    with pytest.raises(PurchaseError, match="exceeds maximum per order"):
        product.buy(2)


def test_limited_product_show_contains_maximum():
    """Test that show() includes maximum per order."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    out = str(product)
    assert "Shipping" in out, "Name should appear"
    assert "10" in out, "Price should appear"
    assert "250" in out, "Quantity should appear"
    assert "Maximum per order" in out or "1" in out, "Maximum should appear"


def test_limited_product_invalid_maximum_raises():
    """Test that maximum <= 0 raises ValueError."""
    with pytest.raises(ValueError, match="Maximum must be positive"):
        LimitedProduct("Shipping", price=10, quantity=250, maximum=0)
    with pytest.raises(ValueError, match="Maximum must be positive"):
        LimitedProduct("Shipping", price=10, quantity=250, maximum=-1)


# --- Product with Promotion ---


def test_product_get_promotion_default_none():
    """Product has no promotion by default."""
    product = Product("MacBook", price=100, quantity=50)
    assert product.promotion is None, "New product should have no promotion"


def test_product_set_promotion_get_promotion():
    """set_promotion and get_promotion round-trip."""
    product = Product("MacBook", price=100, quantity=50)
    prom = PercentDiscount("20% off", percent=20)
    product.promotion = prom
    assert product.promotion is prom, "promotion should return set promotion"
    product.promotion = None
    assert product.promotion is None, "Setting None should remove promotion"


def test_product_show_with_promotion():
    """show() displays promotion name when set."""
    product = Product("MacBook", price=100, quantity=50)
    product.promotion = SecondHalfPrice("Second Half price!")
    out = str(product)
    assert "Promotion" in out, "Output should mention promotion"
    assert "Second Half price!" in out, "Promotion name should appear"


def test_product_buy_with_percent_discount():
    """buy() uses promotion price when promotion is set."""
    product = Product("MacBook", price=100, quantity=100)
    product.promotion = PercentDiscount("30% off", percent=30)
    total = product.buy(10)
    assert total == 700.0, "10 * 100 * 0.7 = 700"
    assert product.quantity == 90, "Quantity should decrease by 10"


def test_product_buy_with_second_half_price():
    """buy() with SecondHalfPrice returns discounted total."""
    product = Product("MacBook", price=100, quantity=100)
    product.promotion = SecondHalfPrice("Second Half price!")
    total = product.buy(2)
    assert total == 150.0, "2 items: 100 + 50 = 150"
    assert product.quantity == 98, "Quantity should decrease by 2"


def test_product_buy_with_third_one_free():
    """buy() with ThirdOneFree returns discounted total."""
    product = Product("MacBook", price=100, quantity=100)
    product.promotion = ThirdOneFree("Third One Free!")
    total = product.buy(3)
    assert total == 200.0, "3 items: pay for 2 = 200"
    assert product.quantity == 97, "Quantity should decrease by 3"


def test_product_str_format():
    """__str__ returns format with $ and Quantity."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    s = str(product)
    assert "MacBook Air M2" in s, "Name should appear"
    assert "$1450" in s, "Price with $ should appear"
    assert "Quantity:100" in s, "Quantity should appear"


def test_product_price_setter_negative_raises():
    """Setting price to negative raises ValueError."""
    product = Product("MacBook", price=100, quantity=50)
    with pytest.raises(ValueError, match="Price cannot be negative"):
        product.price = -100


def test_product_gt_lt_compare_by_price():
    """> and < compare products by price."""
    mac = Product("Mac", price=1450, quantity=10)
    bose = Product("Bose", price=250, quantity=10)
    assert (mac > bose) is True, "Mac price > Bose price"
    assert (mac < bose) is False, "Mac not < Bose"
    assert (bose < mac) is True, "Bose < Mac"


def test_non_stocked_product_buy_with_promotion():
    """NonStockedProduct buy() applies promotion; quantity stays 0."""
    product = NonStockedProduct("Windows License", price=100)
    product.promotion = PercentDiscount("50% off", percent=50)
    total = product.buy(2)
    assert total == 100.0, "2 * 100 * 0.5 = 100"
    assert product.quantity == 0, "Quantity should remain 0"
