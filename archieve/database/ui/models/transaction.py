from dataclasses import dataclass

@dataclass
class Transaction:
    customer_name: str
    item_name: str
    quantity: int
    price: float
    tax: float

    @property
    def amount(self):
        """Calculate total amount including tax"""
        return self.quantity * self.price * (1 + self.tax / 100)
