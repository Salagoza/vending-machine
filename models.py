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
                "last_update": product.last_update,
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
    last_update = db.Column(db.String(150), nullable=False)

    def __init__(
        self,
        name: str,
        category: str,
        price: int,
        machine_id: int,
        quantity: int,
        last_update: str,
    ):
        """Construct the product."""
        self.name = name
        self.category = category
        self.price = price
        self.machine_id = machine_id
        self.quantity = quantity
        self.last_update = last_update

    def to_dict(self) -> dict:
        """Map the object to a dict."""
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res


class Timeline(db.Model):
    """Model for Timeline."""

    id = db.Column(db.Integer, primary_key=True)
    machine_id = db.Column(db.Integer, nullable=False)
    stock_log = db.relationship("ProductLog", backref="timeline", cascade="all,delete")
    time = db.Column(db.String(150), nullable=False)

    def __init__(self, time: str, machine_id: int):
        """Construct the product timeline."""
        self.time = time
        self.machine_id = machine_id

    def to_dict(self) -> dict:
        """Convert machine object to a dict."""
        timeline_dict = {
            "id": self.id,
            "machine_id": self.machine_id,
            "time": self.time,
            "stock": [],
        }
        for product in self.stock_log:
            product_dict = {
                "id": product.id,
                "name": product.name,
                "type": product.category,
                "price": product.price,
                "quantity": product.quantity,
                "last_update": product.last_update,
            }
            timeline_dict["stock"].append(product_dict)
        return timeline_dict


class ProductLog(db.Model):
    """Model for ProductLog."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    timeline_id = db.Column(db.Integer, db.ForeignKey(Timeline.id))
    machine_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(150), nullable=False)
    last_update = db.Column(db.String(150), nullable=False)

    def __init__(
        self,
        name: str,
        timeline_id: int,
        machine_id: int,
        quantity: str,
        price: int,
        category: str,
        last_update: str,
    ):
        """Construct the product timeline."""
        self.name = name
        self.timeline_id = timeline_id
        self.machine_id = machine_id
        self.quantity = quantity
        self.price = price
        self.category = category
        self.last_update = last_update

    def to_dict(self) -> dict:
        """Map the object to a dict."""
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
