from flask import Blueprint,request
from sqlalchemy.sql import text
from db import db
from models import Product
from flask import jsonify

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
        db.session.commit()
    else:
        product.quantity += 1
        db.session.commit()
    return "Added new product to the database!"

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
    db.session.commit()

    return "Updated the product information"

    
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
        db.session.commit()
    else:
        db.session.delete(product)
        db.session.commit()
    return "Delete product from stock!"