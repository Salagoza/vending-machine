from flask import Flask

from db import db
from machine import machine_blueprint
from product import product_blueprint

DB_NAME = "database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

app.register_blueprint(machine_blueprint, url_prefix="/api/machine")
app.register_blueprint(product_blueprint, url_prefix="/api/product")
   

with app.app_context():
    db.create_all()
