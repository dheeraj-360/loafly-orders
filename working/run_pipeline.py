import logging
from loafly import config
from loafly.extract import extract_orders
from loafly.transform import transform_orders
from loafly.load import load_orders


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(config.LOG_FILE_PATH),
            logging.StreamHandler()
        ]
    )


def main():
    setup_logging()
    logging.info("Pipeline started")
    orders = extract_orders(config.INPUT_CSV_PATH)
    logging.info(f"Extracted {len(orders)} orders")
    orders = transform_orders(orders)
    logging.info(f"{len(orders)} orders remain after cleaning")
    load_orders(orders)
    logging.info("Pipeline finished")


if __name__ == "__main__":
    main()