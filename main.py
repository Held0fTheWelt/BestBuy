4import products
import store

# setup initial stock of inventory
product_list = [
    products.Product("MacBook Air M2", price=1450, quantity=100),
    products.Product("Bose QuietComfort Earbuds", price=250, quantity=500),
    products.Product("Google Pixel 7", price=500, quantity=250),
]
best_buy = store.Store(product_list)


def menu():
    """Display the menu and return the user's choice."""
    print("\n1. List all products in store")
    print("2. Show total amount in store")
    print("3. Make an order")
    print("4. Quit")
    return input("Please choose a number: ").strip()


def _do_make_order(store_obj):
    """Collect order lines and place order; print total or error."""
    products_available = store_obj.get_all_products()
    if not products_available:
        print("No products available.")
        return
    for i, product in enumerate(products_available):
        print(f"{i}. ", end="")
        product.show()
    shopping_list = []
    while True:
        try:
            idx = input("Enter product number (or empty to finish): ").strip()
            if idx == "":
                break
            idx = int(idx)
            if idx < 0 or idx >= len(products_available):
                print("Invalid product number.")
                continue
            qty = input("Enter quantity: ").strip()
            qty = int(qty)
            if qty <= 0:
                print("Quantity must be positive.")
                continue
            shopping_list.append((products_available[idx], qty))
        except ValueError:
            print("Invalid input.")
    if shopping_list:
        try:
            total = store_obj.order(shopping_list)
            print(f"Order total: {total}")
        except products.PurchaseError as err:
            print(f"Order failed: {err}")


def execute(store_obj, choice):
    """Execute the chosen action. Returns False on Quit, True otherwise."""
    if choice == "1":
        for product in store_obj.get_all_products():
            product.show()
        return True
    if choice == "2":
        print(store_obj.get_total_quantity())
        return True
    if choice == "3":
        _do_make_order(store_obj)
        return True
    if choice == "4":
        print("Bye!")
        return False
    print("Invalid option.")
    return True


def start(store_obj):
    """Main loop: show menu and execute action until Quit."""
    while True:
        choice = menu()
        if not execute(store_obj, choice):
            break


if __name__ == "__main__":
    start(best_buy)
