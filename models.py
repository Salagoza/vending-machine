from db import db

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

    def __init__(self, name,type,price,machine_id):
        self.name = name
        self.type = type
        self.price = price
        self.machine_id = machine_id
        self.quantity = 1
    
    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

    

