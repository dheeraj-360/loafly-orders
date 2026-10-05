class Order:
    def __init__(self, order_id, customer):
        self.order_id = order_id
        self.customer = customer
        self.items = []

    def add_item(self, name, price):
        self.items.append((name, price))

    def total(self):
        return sum(price for name, price in self.items)
    def __repr__(self):
        return f"Order({self.order_id}, {self.customer}, {len(self.items)} items)"


''' test
order = Order("501","Kabir")
order.add_item('Crossiant',110)
order.add_item('cheetos',46)
print(order.total())'''