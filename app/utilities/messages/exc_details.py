def http_404_product_id_details(id: int) -> str:
    return f"Product with id `{id}` does not exist!"


def http_404_brand_id_details(id: int) -> str:
    return f"Brand with id `{id}` does not exist!"


def http_404_category_id_details(id: int) -> str:
    return f"Category with id `{id}` does not exist!"


def http_404_no_products_available_details() -> str:
    return f"No products available!"


def http_400_name_product_arleady_exist_details(product_name: str) -> str:
    return f"A product named `{product_name}` already exists"
