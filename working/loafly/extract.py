import csv
from loafly.models import Order
#import config

def extract_orders(csv_path):
    orders = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            oid = row["order_id"]
            if oid not in orders:
                orders[oid] = Order(oid, row["customer"])
            orders[oid].add_item(row["item_name"], row["item_price"])
    return list(orders.values())

# orders = extract_orders(config.INPUT_CSV_PATH)

'''test
print(len(orders))
print(orders) '''