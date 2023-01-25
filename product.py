from flask import Blueprint, request, jsonify
from db import db
from models import Product
from sqlalchemy.exc import SQLAlchemyError

product = Blueprint('product', __name__)

"""
Function to create product.
"""
@product.route("/create", methods=["POST"])
def create():
    name = request.form["name"]
    type = request.form["type"]
    price = request.form["price"]
    machine_id = request.form["machine_id"]
    quantity = request.form["quantity"]
    # If the new product already exists in the machine increase the stock else create insert as a new record.
    product = Product.query.filter(Product.name == name, Product.machine_id == machine_id).first()
    if product is None:
        new_product = Product(name, type, price, machine_id, quantity)
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
@product.route("/get", methods=["GET"])
def get():
    lists = list(map(lambda l: l.to_dict(), Product.query.all()))
    return lists, 200

"""
Function to get product by id.
"""
@product.route("/get/<id>", methods=["GET"])
def get_by_id(id):
    product = Product.query.get(id)
    if product is None:
        return "No such product exists in the database!", 404
    return product.to_dict(), 200

"""
Function to update the product information.
"""
@product.route("/update/<id>", methods=["PUT"])
def update(id):
    product = Product.query.get(id)
    if product is None:
        return "No such product exists in the database!", 404

    new_name = request.form["name"] or product.name
    new_type = request.form["type"] or product.type
    new_quantity = request.form["quantity"] or product.quantity
    new_price = request.form["price"] or product.price

    if int(new_quantity) < 1:
        return "The quantity must be greater than 1!", 400

    product.name = new_name
    product.type = new_type
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
@product.route("/delete", methods=["DELETE"])
def delete():
    name = request.form["name"]
    machine_id = request.form["machine_id"]
    quantity = int(request.form["quantity"])
    product = Product.query.filter(Product.name == name, Product.machine_id == machine_id).first()
    if product is None:
        return "No such product exists in the database", 404
    # If the stock level of that product is greater than 1 decrease the stock else delete the record.
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