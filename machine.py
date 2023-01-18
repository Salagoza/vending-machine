from flask import Blueprint,request
from db import db
from models import Machine
from sqlalchemy.exc import SQLAlchemyError

machine = Blueprint('machine',__name__)

"""
Function to create vending machine.
"""
@machine.route("/create",methods=["POST"])
def create():
    name = request.form["name"]
    address = request.form["address"]
    new_machine = Machine(name,address)
    try:
        db.session.add(new_machine)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!",404
    return "Added new machine to the database!",200
    
"""
Function to get all vending machines.
"""
@machine.route("/get",methods=["GET"])
def get():
    machines = Machine.query.all()
    result = {"machines" : []}
    for machine in machines:
        m = {}
        m["id"] = machine.id
        m["address"] = machine.address
        m["name"] = machine.name
        m["stock"] = []
        for product in machine.stock:
            p = {}
            p["id"] = product.id
            p["name"] = product.name
            p["type"] = product.type
            p["price"] = product.price
            p["machine_id"] = product.machine_id
            p["quantity"] = product.quantity
            m["stock"].append(p)
        result["machines"].append(m)
    return result

"""
Function to update the vending machine name or adress.
"""
@machine.route("/update/<id>",methods=["PUT"])
def update(id):    
    machine = Machine.query.get(id)
    new_name = request.form["name"] or machine.name
    new_address = request.form["address"] or machine.address
    machine.name = new_name
    machine.address = new_address
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 404
    return "Updated the vending machine information!",200

"""
Function to delete vending machine.
"""
@machine.route("/delete/<id>",methods=["DELETE"])
def delete(id):    
    machine = Machine.query.get(id)
    db.session.delete(machine)
    
    try: 
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!",404
    return "Delete machine successfully!",200