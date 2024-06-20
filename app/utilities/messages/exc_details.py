def http_404_product_id_details(id: int) -> str:
    return f"Product with id `{id}` does not exist!"


def http_404_brand_id_details(id: int) -> str:
    return f"Brand with id `{id}` does not exist!"


def http_404_category_id_details(id: int) -> str:
    return f"Category with id `{id}` does not exist!"


def http_404_no_products_available_details() -> str:
    return f"No products available!"


def http_400_product_name_details(product_name: str) -> str:
    return f"Product named `{product_name}` already exists!"


# use!!!
def http_400_username_details(username: str) -> str:
    return f"User with username `{username}` arleady exist!"


# use!!!
def http_400_email_details(email: str) -> str:
    return f"User with email `{email}` arleady exist!"


def http_400_signup_credentials_details() -> str:
    return "Signup failed! Recheck all your credentials!"
