from flask import Blueprint,request
from sqlalchemy.sql import text
from db import db
from models import Machine
from flask import jsonify

machine = Blueprint('machine',__name__)

# @machine.route("/")
# def index():
#     return "Hello from machine"

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
            m["stock"].append(p)
        result["machines"].append(m)
    return result


"""
Function to test database.
"""
@machine.route('/')
def testdb():
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text



