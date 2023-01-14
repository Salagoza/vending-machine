from db import db

class Machine(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),unique=True)
    address = db.Column(db.String(150))
    stock = db.relationship('Product',backref="machine")

    def __init__(self, name,address):
        self.name = name
        self.address = address
    
    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

    
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150))
    type = db.Column(db.String(150))
    price = db.Column(db.Integer)
    machine_id = db.Column(db.Integer,db.ForeignKey('machine.id'))

    def __init__(self, name,type,price,machine_id):
        self.name = name
        self.type = type
        self.price = price
        self.machine_id = machine_id
    
    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res

    

