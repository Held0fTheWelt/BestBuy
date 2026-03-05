"""Pytest tests for the Product class."""

import pytest

from products import Product, PurchaseError, NonStockedProduct, LimitedProduct


def test_create_normal_product_works():
    """Test that creating a normal product works."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    assert product.get_quantity() == 100, "Initial quantity should be 100"
    assert product.is_active() is True, "New product should be active"


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
    product.set_quantity(0)
    assert product.get_quantity() == 0, "Quantity should be 0 after set_quantity(0)"
    assert product.is_active() is False, "Product should be inactive when quantity is 0"


def test_product_buy_zero_quantity_becomes_inactive():
    """Test that buying all stock makes product inactive."""
    product = Product("MacBook Air M2", price=1450, quantity=5)
    product.buy(5)
    assert product.get_quantity() == 0, "Quantity should be 0 after buying all stock"
    assert product.is_active() is False, "Product should be inactive when stock is exhausted"


def test_product_purchase_modifies_quantity_and_returns_right_output():
    """Test that product purchase modifies the quantity and returns the right output."""
    product = Product("MacBook Air M2", price=10, quantity=100)
    total = product.buy(30)
    assert total == 300.0, "Total price should be 30 * 10 = 300.0"
    assert product.get_quantity() == 70, "Quantity should decrease from 100 to 70"


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
    product.set_quantity(10)
    assert product.get_quantity() == 10, "Quantity should be updated to 10"
    assert product.is_active() is True, "Product should stay active with positive quantity"


def test_set_quantity_negative_raises():
    """Test that set_quantity with negative value raises ValueError."""
    product = Product("MacBook", price=100, quantity=50)
    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        product.set_quantity(-1)


def test_activate_deactivate_toggle():
    """Test that deactivate/activate correctly change is_active."""
    product = Product("MacBook", price=100, quantity=50)
    product.deactivate()
    assert product.is_active() is False, "Product should be inactive after deactivate()"
    product.activate()
    assert product.is_active() is True, "Product should be active again after activate()"


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
    assert product.get_quantity() == 70, "Remaining quantity should be 70"


def test_show_prints_name_price_quantity(capsys):
    """Test that show() prints a string containing name, price and quantity."""
    product = Product("MacBook Air M2", price=1450, quantity=100)
    product.show()
    out = capsys.readouterr().out
    assert "MacBook Air M2" in out, "Product name should appear in show() output"
    assert "1450" in out, "Price should appear in show() output"
    assert "100" in out, "Quantity should appear in show() output"


def test_reactivate_then_restock_allows_buy():
    """Test that after sell-out, activate and set_quantity allow buying again."""
    product = Product("MacBook", price=10, quantity=2)
    product.buy(2)
    assert product.is_active() is False, "Product should be inactive after sell-out"
    product.activate()
    product.set_quantity(5)
    total = product.buy(3)
    assert total == 30.0, "Order total should be 30.0"
    assert product.get_quantity() == 2, "Remaining quantity should be 2"


# --- NonStockedProduct ---


def test_non_stocked_product_creation():
    """Test that creating a non-stocked product works; quantity is always 0."""
    product = NonStockedProduct("Windows License", price=125)
    assert product.get_quantity() == 0, "Non-stocked product quantity should be 0"
    assert product.is_active() is True, "Non-stocked product should be active"


def test_non_stocked_product_buy_returns_total_quantity_unchanged():
    """Test that buy() returns correct total and quantity stays 0."""
    product = NonStockedProduct("Windows License", price=125)
    total = product.buy(3)
    assert total == 375.0, "Total should be 125 * 3 = 375.0"
    assert product.get_quantity() == 0, "Quantity should still be 0 after buy"


def test_non_stocked_product_set_quantity_zero_allowed():
    """Test that set_quantity(0) is allowed (no-op)."""
    product = NonStockedProduct("Windows License", price=125)
    product.set_quantity(0)
    assert product.get_quantity() == 0, "Quantity should remain 0"


def test_non_stocked_product_set_quantity_non_zero_raises():
    """Test that set_quantity(non-zero) raises ValueError."""
    product = NonStockedProduct("Windows License", price=125)
    with pytest.raises(ValueError, match="Non-stocked product quantity must remain 0"):
        product.set_quantity(1)


def test_non_stocked_product_show_contains_non_stocked(capsys):
    """Test that show() indicates non-stocked."""
    product = NonStockedProduct("Windows License", price=125)
    product.show()
    out = capsys.readouterr().out
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
    assert product.get_quantity() == 250, "Quantity should be 250"
    assert product.is_active() is True, "Limited product should be active"


def test_limited_product_buy_within_maximum_works():
    """Test that buy(quantity <= maximum) works and reduces stock."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=2)
    total = product.buy(2)
    assert total == 20.0, "Total should be 10 * 2 = 20.0"
    assert product.get_quantity() == 248, "Quantity should decrease by 2"


def test_limited_product_buy_above_maximum_raises():
    """Test that buy(quantity > maximum) raises PurchaseError."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    with pytest.raises(PurchaseError, match="exceeds maximum per order"):
        product.buy(2)


def test_limited_product_show_contains_maximum(capsys):
    """Test that show() includes maximum per order."""
    product = LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
    product.show()
    out = capsys.readouterr().out
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
