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


# @event.listens_for(Machine.__table__, 'after_create')
# def create_machines(*args, **kwargs):
#     db.session.add(Machine(name='Machine 1', address='IC Bld. Canteen Floor.2'))
#     db.session.add(Machine(name='Machine 2', address='Aditayathorn Bld. Canteen G.Floor'))
#     db.session.add(Machine(name='Machine 3', address='IC Bld. 1502 Com Sci Lab'))
#
#     db.session.commit()
#
#
# @event.listens_for(Product.__table__, 'after_create')
# def create_products(*args, **kwargs):
#     db.session.add(Product(name='Pringle', category="Snack", price=20, machine_id=1, quantity=15))
#     db.session.add(Product(name='Lay', category="Snack", price=15, machine_id=1, quantity=8))
#     db.session.add(Product(name='Coke', category="Beverage", price=20, machine_id=1, quantity=6))
#     db.session.add(Product(name='Sprite', category="Beverage", price=20, machine_id=1, quantity=10))
#
#     db.session.add(Product(name='Haribo', category="Snack", price=10, machine_id=2, quantity=4))
#     db.session.add(Product(name='Oreo', category="Snack", price=5, machine_id=2, quantity=10))
#     db.session.add(Product(name='Ichitan Lemon', category="Beverage", price=20, machine_id=2, quantity=15))
#
#     db.session.add(Product(name='Taro', category="Snack", price=20, machine_id=3, quantity=8))
#     db.session.add(Product(name='Snack Jack', category="Snack", price=30, machine_id=3, quantity=3))
#     db.session.add(Product(name='Lemon Schweppes', category="Beverage", price=10, machine_id=3, quantity=9))
#     db.session.add(Product(name='M150', category="Beverage", price=15, machine_id=3, quantity=5))
#     db.session.add(Product(name='Signha Water', category="Beverage", price=10, machine_id=3, quantity=12))
#
#     db.session.commit()
