from flask import Blueprint,request

machine = Blueprint('machine',__name__)

@machine.route("/")
def index():
    return "Hello from machine!"



