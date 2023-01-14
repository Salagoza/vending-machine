from flask import Blueprint,request
from sqlalchemy.sql import text
from db import db
from models import Machine

machine = Blueprint('machine',__name__)

"""
Function to create the vending machine.
"""
@machine.route("/create",methods=["POST"])
def create():
    name = request.form["name"]
    address = request.form["address"]
    new_machine = Machine(name,address)
    db.session.add(new_machine)
    db.session.commit()
    return "Added new machine to the database!"

"""
Function to get all the vending machine.
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

@machine.route("/delete/<id>",methods=["DELETE"])
def delete(id):
    machine = Machine.query.get(id)
    db.session.delete(machine)
    db.session.commit()
    return "Delete machine successfully"