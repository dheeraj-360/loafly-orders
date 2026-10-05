import logging

logger = logging.getLogger(__name__)

# print(logger)


def clean_price(text):
    cleaned = text.strip().replace(",", "")
    if cleaned == "":
        raise ValueError("price is missing")
    return float(cleaned)


def apply_discount(price, percent):
    return price - price * percent / 100


def transform_orders(orders):
    valid_orders = []
    for order in orders:
        cleaned_items = []
        for name, raw_price in order.items:
            try:
                price = clean_price(raw_price)
                cleaned_items.append((name, price))
            except ValueError:
                logger.warning(f"Order {order.order_id}: skipping '{name}', bad price '{raw_price}'")
            finally:
                logger.debug(f"Order {order.order_id}: checked price for '{name}'")
        order.items = cleaned_items
        if not order.items:
            logger.warning(f"Order {order.order_id}: no valid items, skipping whole order")
            continue
        valid_orders.append(order)
    return valid_orders