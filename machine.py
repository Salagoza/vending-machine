from flask import Blueprint, Response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

import constants
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

        return jsonify({"message": constants.MSG_500}), 500
    return jsonify({"message": constants.MSG_200}), 200


@machine_blueprint.route("/get", methods=["GET"])
def get_all_machines() -> Response:
    """Get all vending machines."""
    machines = Machine.query.all()
    response = {"machines": []}
    for machine in machines:
        data = machine.to_dict()
        response["machines"].append(data)
    return jsonify(response)


@machine_blueprint.route("/get/<machine_id>")
def get_machine_by_id(machine_id: int) -> tuple[Response, int]:
    """Get machine by id."""
    machine = Machine.query.get(machine_id)
    if machine is None:
        return jsonify({"message": constants.MSG_404}), 404
    response = machine.to_dict()
    return jsonify(response), 200


@machine_blueprint.route("/update/<machine_id>", methods=["PUT"])
def update_machine(machine_id: int) -> tuple[Response, int]:
    """Update the vending machine name or address."""
    machine = Machine.query.get(machine_id)
    if machine is None:
        return jsonify({"message": constants.MSG_404}), 404

    new_name = request.form["name"] or machine.name
    new_address = request.form["address"] or machine.address
    machine.name = new_name
    machine.address = new_address

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"message": constants.MSG_500}), 500
    return jsonify({"message": constants.MSG_200}), 200


@machine_blueprint.route("/delete/<machine_id>", methods=["DELETE"])
def delete_machine(machine_id: int) -> tuple[Response, int]:
    """Delete vending machine."""
    machine = Machine.query.get(machine_id)

    if machine is None:
        return jsonify({"message": constants.MSG_404}), 404
    try:
        db.session.delete(machine)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"message": constants.MSG_500}), 500
    return jsonify({"message": constants.MSG_200}), 200
