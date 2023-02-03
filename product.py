from flask import Blueprint, Response, jsonify, request
from sqlalchemy.exc import SQLAlchemyError

import constants
from db import db
from models import Product

product_blueprint = Blueprint("product", __name__)


@product_blueprint.route("/create", methods=["POST"])
def create_product() -> tuple[Response, int]:
    """Create product."""
    name = request.form["name"]
    category = request.form["type"]
    price = int(request.form["price"])
    machine_id = int(request.form["machine_id"])
    quantity = int(request.form["quantity"])

    product = Product.query.filter(
        Product.name == name, Product.machine_id == machine_id
    ).first()
    if product is None:
        new_product = Product(name, category, price, machine_id, quantity)
        db.session.add(new_product)
    else:
        product.quantity += quantity

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"message": constants.MSG_500}), 500
    return jsonify({"message": constants.MSG_200}), 200


@product_blueprint.route("/get", methods=["GET"])
def get_all_products() -> tuple[Response, int]:
    """Get all products."""
    response = list(map(lambda l: l.to_dict(), Product.query.all()))
    return jsonify(response), 200


@product_blueprint.route("/get/<product_id>", methods=["GET"])
def get_product_by_id(product_id: int) -> tuple[Response, int]:
    """Get product by id."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify({"message": constants.MSG_404}), 404
    response = product.to_dict()
    return jsonify(response), 200


@product_blueprint.route("/update/<product_id>", methods=["PUT"])
def update_product(product_id: int) -> tuple[Response, int]:
    """Update the product information."""
    product = Product.query.get(product_id)
    if product is None:
        return jsonify("No such product exists in the database!"), 404
    new_name = request.form["name"] or product.name
    new_type = request.form["type"] or product.category
    new_quantity = request.form["quantity"] or product.quantity
    new_price = request.form["price"] or product.price

    if int(new_quantity) < 1:
        return jsonify({"message": constants.MSG_400}), 400

    product.name = new_name
    product.category = new_type
    product.quantity = new_quantity
    product.price = new_price

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"message": constants.MSG_500}), 500
    return jsonify({"message": constants.MSG_200}), 200


@product_blueprint.route("/delete", methods=["DELETE"])
def delete_product() -> tuple[Response, int]:
    """Delete product."""
    name = request.form["name"]
    machine_id = request.form["machine_id"]
    quantity = int(request.form["quantity"])
    product = Product.query.filter(
        Product.name == name, Product.machine_id == machine_id
    ).first()
    if product is None:
        return jsonify({"message": constants.MSG_404}), 404

    if product.quantity > quantity:
        product.quantity -= quantity
    else:
        db.session.delete(product)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return jsonify({"message": constants.MSG_500}), 500
    return jsonify({"message": constants.MSG_200}), 200
