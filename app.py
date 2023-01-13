from flask import Flask
from machine import machine
from db import db

DB_NAME = "database.db"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

app.register_blueprint(machine,url_prefix="/api/machine")
   

with app.app_context():
    from models import Machine  # noqa: F401

    db.create_all()

