from db import db


class Machine(db.Model):
    """Model for vending machine."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)
    address = db.Column(db.String(150), nullable=False)
    stock = db.relationship("Product", backref="machine", cascade="all,delete")

    def __init__(self, name: str, address: str):
        """Construct the vending machine."""
        self.name = name
        self.address = address

    def to_dict(self) -> dict:
        """Convert machine object to a dict."""
        machine_dict = {
            "id": self.id,
            "address": self.address,
            "name": self.name,
            "stock": [],
        }
        for product in self.stock:
            product_dict = {
                "id": product.id,
                "name": product.name,
                "type": product.category,
                "price": product.price,
                "machine_id": self.id,
                "quantity": product.quantity,
            }
            machine_dict["stock"].append(product_dict)
        return machine_dict


class Product(db.Model):
    """Model for vending product."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    machine_id = db.Column(db.Integer, db.ForeignKey(Machine.id))
    quantity = db.Column(db.Integer)

    def __init__(
        self, name: str, category: str, price: int, machine_id: int, quantity: int
    ):
        """Construct the product."""
        self.name = name
        self.category = category
        self.price = price
        self.machine_id = machine_id
        self.quantity = quantity

    def to_dict(self) -> dict:
        """Map the object to a dict."""
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
