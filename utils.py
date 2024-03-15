# userapp/utils.py

def calculate_total_price(cart_items):
    total_price = 0
    for item in cart_items:
        total_price += item.product.sale_price
    return total_price
