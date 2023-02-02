from flask import Blueprint, Response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import Machine

machine_blueprint = Blueprint("machine", __name__)


@machine_blueprint.route("/create", methods=["POST"])
def create_machine() -> tuple[Response, int]:
    """Create vending machine."""
    name = request.form["name"]
    address = request.form["address"]
    new_machine = Machine(name, address)
    try:
        db.session.add(new_machine)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()

        return jsonify({"message": "Something went wrong!"}), 500
    return jsonify({"message": "Added a new machine to the database!"}), 200


@machine_blueprint.route("/get", methods=["GET"])
def get_all_machines() -> Response:
    """Get all vending machines."""
    machines = Machine.query.all()
    response = {"machines": []}
    for machine in machines:
        data = create_machine_response(machine)
        response["machines"].append(data)
    return jsonify(response)


@machine_blueprint.route("/get/<machine_id>")
def get_machine_by_id(
    machine_id: int,
) -> tuple[Response, int]:
    """Get machine by id."""
    machine = Machine.query.get(machine_id)
    if machine is None:
        return jsonify({"message": "No such machine exists in the database!"}), 404
    response = create_machine_response(machine)
    return jsonify(response), 200


def create_machine_response(machine: Machine) -> dict:
    """Convert machine object to a dict."""
    machine_dict = {
        "id": machine.id,
        "address": machine.address,
        "name": machine.name,
        "stock": [],
    }
    for product in machine.stock:
        product_dict = {
            "id": product.id,
            "name": product.name,
            "type": product.category,
            "price": product.price,
            "machine_id": machine.id,
            "quantity": product.quantity,
        }
        machine_dict["stock"].append(product_dict)
    return machine_dict


@machine_blueprint.route("/update/<machine_id>", methods=["PUT"])
def update_machine(machine_id: int) -> tuple[Response, int]:
    """Update the vending machine name or address."""
    machine = Machine.query.get(machine_id)
    if machine is None:
        return jsonify("No such machine exists in the database!"), 404

    new_name = request.form["name"] or machine.name
    new_address = request.form["address"] or machine.address
    machine.name = new_name
    machine.address = new_address

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify("Something went wrong!"), 500
    return jsonify("Updated the vending machine information!"), 200


@machine_blueprint.route("/delete/<machine_id>", methods=["DELETE"])
def delete_machine(machine_id: int) -> tuple[Response, int]:
    """Delete vending machine."""
    machine = Machine.query.get(machine_id)

    if machine is None:
        return jsonify({"message": "No such machine exists in the database!"}), 404
    try:
        db.session.delete(machine)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"message": "Something went wrong!"}), 500
    return jsonify({"message": "Delete machine successfully!"}), 200
