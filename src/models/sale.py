from datetime import datetime

class Sale:
    def __init__(self, sale_id, products, total, timestamp=None):
        self.sale_id = sale_id
        self.products = products  # Liste de dicts {"product_id", "name", "price", "quantity"}
        self.total = total
        self.timestamp = timestamp or datetime.now()

    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "products": self.products,
            "total": self.total,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        return Sale(
            sale_id=data["sale_id"],
            products=data["products"],
            total=data["total"],
            timestamp=data["timestamp"]
        )
