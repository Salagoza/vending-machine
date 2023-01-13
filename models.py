from db import db

class Machine(db.Model):
    machine_id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),unique=True)
    address = db.Column(db.String(150))

    def __init__(self, name,address):
        self.name = name
        self.address = address
    
    def to_dict(self):
        res = {}
        for field in self.__table__.columns.keys():
            if hasattr(self, field):
                res[field] = getattr(self, field)
        return res
