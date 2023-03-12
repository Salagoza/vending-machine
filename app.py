from flask import Flask
from flask_swagger_ui import get_swaggerui_blueprint

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
    SWAGGER_URL = "/api/swagger"
    API_URL = "/static/swagger.json"
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Vending Machine API"}
    )

    db.init_app(app)

    app.register_blueprint(machine_blueprint, url_prefix="/api/machine")
    app.register_blueprint(product_blueprint, url_prefix="/api/product")
    app.register_blueprint(timeline_blueprint, url_prefix="/api/timeline")
    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    with app.app_context():
        db.create_all()

    return app
