from flask import Flask
from machine import machine
from product import product
from db import db

DB_NAME = "database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

app.register_blueprint(machine,url_prefix="/api/machine")
app.register_blueprint(product,url_prefix="/api/product")
   

with app.app_context():
    from models import Machine,Product

    db.create_all()
