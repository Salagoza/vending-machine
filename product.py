from flask import Blueprint, request, jsonify
from db import db
from models import Product
from sqlalchemy.exc import SQLAlchemyError

product_blueprint = Blueprint('product', __name__)

"""
Function to create product.
"""
@product_blueprint.route("/create", methods=["POST"])
def create_product():
    name = request.form["name"]
    category = request.form["type"]
    price = request.form["price"]
    machine_id = request.form["machine_id"]
    quantity = request.form["quantity"]

    product = Product.query.filter(Product.name == name, Product.machine_id == machine_id).first()
    if product is None:
        new_product = Product(name, category, price, machine_id, quantity)
        db.session.add(new_product)
    else:
        product.quantity += quantity

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 500
    return "Added a new product to the database!", 200

"""
Function to get all products.
"""
@product_blueprint.route("/get", methods=["GET"])
def get_all_products():
    response = list(map(lambda l: l.to_dict(), Product.query.all()))
    return response, 200

"""
Function to get product by id.
"""
@product_blueprint.route("/get/<product_id>", methods=["GET"])
def get_product_by_id(product_id: int):
    product = Product.query.get(product_id)
    if product is None:
        return "No such product exists in the database!", 404
    response = product.to_dict()
    return response, 200

"""
Function to update the product information.
"""
@product_blueprint.route("/update/<product_id>", methods=["PUT"])
def update_product(product_id: int):
    product = Product.query.get(product_id)
    if product is None:
        return "No such product exists in the database!", 404
    new_name = request.form["name"] or product.name
    new_type = request.form["type"] or product.category
    new_quantity = request.form["quantity"] or product.quantity
    new_price = request.form["price"] or product.price

    if int(new_quantity) < 1:
        return "The quantity must be greater than 1!", 400

    product.name = new_name
    product.category = new_type
    product.quantity = new_quantity
    product.price = new_price

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 500
    return "Updated the product information!", 200

"""
Function to delete product.
"""
@product_blueprint.route("/delete", methods=["DELETE"])
def delete_product():
    name = request.form["name"]
    machine_id = request.form["machine_id"]
    quantity = int(request.form["quantity"])
    product = Product.query.filter(Product.name == name, Product.machine_id == machine_id).first()
    if product is None:
        return "No such product exists in the database", 404

    if product.quantity > quantity:
        product.quantity -= quantity
    else:
        db.session.delete(product)

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 500
    return "Delete product from stock!", 200
