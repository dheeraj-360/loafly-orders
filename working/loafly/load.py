import time
import logging
from loafly.gateway import save_to_orders_api
from loafly.transform import apply_discount
from loafly import config 

logger = logging.getLogger(__name__)


def save_order_with_retry(order_id, total):
    attempts = 0
    while attempts < config.MAX_RETRIES:
        attempts += 1
        try:
            result = save_to_orders_api(order_id, total)
            logger.info(f"Order {order_id}: saved on attempt {attempts}, total={total}")
            return result
        except ConnectionError as e:
            logger.warning(f"Order {order_id}: attempt {attempts} failed - {e}")
            if attempts < config.MAX_RETRIES:
                time.sleep(config.RETRY_WAIT_SECONDS)
    logger.error(f"Order {order_id}: failed to save after {config.MAX_RETRIES} attempts")


def load_orders(orders):
    for order in orders:
        total = apply_discount(order.total(), config.DISCOUNT_PERCENT)
        save_order_with_retry(order.order_id, total)