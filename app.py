from flask import Flask

from db import db
from machine import machine_blueprint
from product import product_blueprint
from timeline import timeline_blueprint
DB_NAME = "database.db"


def create_app(database_uri: str = f"sqlite:///{DB_NAME}") -> Flask:
    """Create the application."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    db.init_app(app)

    app.register_blueprint(machine_blueprint, url_prefix="/api/machine")
    app.register_blueprint(product_blueprint, url_prefix="/api/product")
    app.register_blueprint(timeline_blueprint, url_prefix="/api/timeline")

    with app.app_context():
        db.create_all()

    return app
