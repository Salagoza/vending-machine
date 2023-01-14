from flask import Blueprint,request
from sqlalchemy.sql import text
from db import db
from models import Product
from flask import jsonify

product = Blueprint('product',__name__)


@product.route("/create",methods=["POST"])
def create():
    name = request.form["name"]
    type = request.form["type"]
    price = request.form["price"]
    machine_id = request.form["machine_id"]
    new_product = Product(name,type,price,machine_id)
    db.session.add(new_product)
    db.session.commit()
    return "Added new product to the database!"


@product.route("/get",methods=["GET"])
def get():
    lists = list(map(lambda l: l.to_dict(), Product.query.all()))
    return jsonify({"products": lists})
