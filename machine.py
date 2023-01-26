from flask import Blueprint, request
from db import db
from models import Machine
from sqlalchemy.exc import SQLAlchemyError

machine_blueprint = Blueprint('machine', __name__)

"""
Function to create vending machine.
"""
@machine_blueprint.route("/create", methods=["POST"])
def create_machine():
    name = request.form["name"]
    address = request.form["address"]
    new_machine = Machine(name, address)
    try:
        db.session.add(new_machine)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 500
    return "Added a new machine to the database!", 200


"""
Function to get all vending machines.
"""
@machine_blueprint.route("/get", methods=["GET"])
def get_all_machines():
    machines = Machine.query.all()
    response = {"machines": []}
    for machine in machines:
        data = create_machine_response(machine)
        response["machines"].append(data)
    return response, 200

"""
Function to get machine by id.
"""
@machine_blueprint.route("/get/<machine_id>")
def get_machine_by_id(machine_id: int):
    machine = Machine.query.get(machine_id)
    if machine is None:
        return "No such machine exists in the database!", 404
    response = create_machine_response(machine)
    return response, 200

"""
Function to convert machine object to a dict.
"""
def create_machine_response(machine: Machine):
    machine_dict = {
        "id": machine.id,
        "address": machine.address,
        "name": machine.name,
        "stock": []}
    for product in machine.stock:
        product_dict = {
            "id": product.id,
            "name": product.name,
            "type": product.category,
            "price": product.price,
            "machine_id": machine.id,
            "quantity": product.quantity}
        machine_dict["stock"].append(product_dict)
    return machine_dict

"""
Function to update the vending machine name or address.
"""
@machine_blueprint.route("/update/<machine_id>", methods=["PUT"])
def update_machine(machine_id: int):
    machine = Machine.query.get(machine_id)
    if machine is None:
        return "No such machine exists in the database!", 404

    new_name = request.form["name"] or machine.name
    new_address = request.form["address"] or machine.address
    machine.name = new_name
    machine.address = new_address

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 500
    return "Updated the vending machine information!", 200

"""
Function to delete vending machine.
"""
@machine_blueprint.route("/delete/<machine_id>", methods=["DELETE"])
def delete_machine(machine_id: int):
    machine = Machine.query.get(machine_id)

    if machine is None:
        return "No such machine exists in the database!", 404

    try:
        db.session.delete(machine)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 500
    return "Delete machine successfully!", 200


