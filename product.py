from flask import Blueprint,request
from db import db
from models import Product
from flask import jsonify
from sqlalchemy.exc import SQLAlchemyError


product = Blueprint('product',__name__)

"""
Function to create product.
"""
@product.route("/create",methods=["POST"])
def create():
    name = request.form["name"]
    type = request.form["type"]
    price = request.form["price"]
    machine_id = request.form["machine_id"]
    # If the new product already exists in the machine increase the stock else create insert as a new record.
    product = Product.query.filter(Product.name==name,Product.machine_id==machine_id).first()
    if (product is None):
        new_product = Product(name,type,price,machine_id)
        db.session.add(new_product)
    else:
        product.quantity += 1

    try: 
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 404
    return "Added new product to the database!",200

"""
Function to get all products.
"""
@product.route("/get",methods=["GET"])
def get():
    lists = list(map(lambda l: l.to_dict(), Product.query.all()))
    return jsonify({"products": lists})

"""
Function to update the product information.
"""
@product.route("/update/<id>",methods=["PUT"])
def update(id):
    product = Product.query.get(id)
    new_name = request.form["name"] or product.name
    new_type = request.form["type"] or product.type
    new_quantity = request.form["quantity"] or product.quantity
    new_price = request.form["price"] or product.price

    if int(new_quantity) < 1:
        return "The quantity must be greater than 1!",400

    product.name = new_name
    product.type = new_type
    product.quantity = new_quantity
    product.price = new_price

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!", 404
    return "Updated the product information", 200

"""
Function to delete product.
"""
@product.route("/delete",methods=["DELETE"])
def delete():
    name = request.form["name"]
    machine_id = request.form["machine_id"]
    product = Product.query.filter(Product.name==name,Product.machine_id==machine_id).first()
    # If the stock level of that product is greater than 1 decrease the stock else delete the record.
    if (product.quantity != 1):
        product.quantity -= 1
    else:
        db.session.delete(product)
    try: 
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        return "Something went wrong!",404
    return "Delete product from stock!",200