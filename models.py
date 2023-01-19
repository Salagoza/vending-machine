from db import db
from sqlalchemy import event

class Machine(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),unique=True)
    address = db.Column(db.String(150),nullable=False)
    stock = db.relationship('Product',backref="machine",cascade="all,delete")

    def __init__(self, name,address):
        self.name = name
        self.address = address

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    type = db.Column(db.String(150),nullable=False)
    price = db.Column(db.Integer,nullable=False)
    machine_id = db.Column(db.Integer,db.ForeignKey(Machine.id))
    quantity = db.Column(db.Integer)

    def __init__(self, name,type,price,machine_id,quantity):
        self.name = name
        self.type = type
        self.price = price
        self.machine_id = machine_id
        self.quantity = quantity
    
    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

@event.listens_for(Machine.__table__, 'after_create')
def create_machines(*args, **kwargs):
    db.session.add(Machine(name='Machine 1', address='IC Bld. Canteen Floor.2'))
    db.session.add(Machine(name='Machine 2', address='Aditayathorn Bld. Canteen G.Floor'))
    #db.session.add(Machine(name='Machine 3', address='IC Bld. 1502 Com Sci Lab'))
    
    db.session.commit()

@event.listens_for(Product.__table__, 'after_create')
def create_products(*args, **kwargs):
    db.session.add(Product(name='Pringle', type="Snack",price=20,machine_id=1,quantity=15))
    #db.session.add(Product(name='Lay', type="Snack",price=15,machine_id=1,quantity=8))
    db.session.add(Product(name='Coke', type="Beverage",price=20,machine_id=1,quantity=6))
    db.session.add(Product(name='Sprite', type="Beverage",price=20,machine_id=1,quantity=10))

    db.session.add(Product(name='Haribo',type="Snack",price=10,machine_id=2,quantity=4))
    #db.session.add(Product(name='Oreo',type="Snack",price=5,machine_id=2,quantity=10))
    db.session.add(Product(name='Ichitan Lemon',type="Beverage",price=20,machine_id=2,quantity=15))

    # db.session.add(Product(name='Taro',type="Snack",price=20,machine_id=3,quantity=8))
    # db.session.add(Product(name='Snack Jack',type="Snack",price=30,machine_id=3,quantity=3))
    # db.session.add(Product(name='Lemon Schweppes',type="Beverage",price=10,machine_id=3,quantity=9))
    # db.session.add(Product(name='M150',type="Beverage",price=15,machine_id=3,quantity=5))
    # db.session.add(Product(name='Signha Water',type="Beverage",price=10,machine_id=3,quantity=12))
    
    db.session.commit()
    

