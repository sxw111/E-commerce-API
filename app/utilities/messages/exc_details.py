def http_404_product_id_details(id: int) -> str:
    return f"Product with id `{id}` does not exist!"


def http_404_brand_id_details(id: int) -> str:
    return f"Brand with id `{id}` does not exist!"


def http_404_category_id_details(id: int) -> str:
    return f"Category with id `{id}` does not exist!"


def http_404_no_products_available_details() -> str:
    return "No products available!"


def http_400_product_name_details(product_name: str) -> str:
    return f"Product named `{product_name}` already exists!"


def http_400_username_details(username: str) -> str:
    return f"User with username `{username}` arleady exist!"


def http_400_email_details(email: str) -> str:
    return f"User with email `{email}` arleady exist!"


def http_400_signup_credentials_details() -> str:
    return "Signup failed!"


def http_404_id_details(id: int) -> str:
    return f"User with id `{id}` does not exist!"


def http_404_cart_item_id_details(id: int) -> str:
    return f"Cart item with id `{id}` does not exist!"


def http_404_cart_is_empty_details() -> str:
    return "Cart is empty, add items!"


def http_403_access_denied_details() -> str:
    return "You do not have permission to perform this action!"


def http_400_product_quantity_details() -> str:
    return "There is not enough stock available to fulfill your request! Sorry ><"
