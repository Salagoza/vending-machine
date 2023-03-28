from datetime import datetime
from typing import List

from flask import Blueprint, Response, jsonify
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ProductLog, Timeline

timeline_blueprint = Blueprint("timeline", __name__)


def create_timeline(machine_id: int) -> None:
    """Create vending machine timeline."""
    from machine import get_machine_by_id

    print(machine_id)
    machine = get_machine_by_id(machine_id)[0].json
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    timeline = Timeline(current_time, machine["id"])
    try:
        db.session.add(timeline)
        db.session.commit()
        create_product_log(timeline.id, machine["stock"])
    except SQLAlchemyError:
        db.session.rollback()


def create_product_log(timeline_id: int, product: List[dict]) -> None:
    """Create product log for each timeline."""
    for p in product:
        log = ProductLog(
            p["name"],
            timeline_id,
            p["machine_id"],
            p["quantity"],
            p["price"],
            p["type"],
            p["last_update"],
        )
        db.session.add(log)
    db.session.commit()


@timeline_blueprint.route("/machine_timeline/<machine_id>", methods=["GET"])
def get_machine_timeline_by_machine_id(machine_id: int) -> tuple[Response, int]:
    """Get each vending machine timeline."""
    timelines = Timeline.query.filter(Timeline.machine_id == machine_id)
    response = {"timelines": []}
    for timeline in timelines:
        response["timelines"].append(timeline.to_dict())
    return jsonify(response), 200


@timeline_blueprint.route("/product_timeline/<product_name>", methods=["GET"])
def get_product_timeline_by_product_name(product_name: str) -> tuple[Response, int]:
    """Get the timeline for each product."""
    products = ProductLog.query.filter(ProductLog.name == product_name)
    response = list(map(lambda lam: lam.to_dict(), products))
    return jsonify(response), 200


def delete_machine_timeline_by_machine_id(machine_id: int) -> None:
    """Delete all machine timeline associate with that machine."""
    timelines = Timeline.query.filter(Timeline.machine_id == machine_id)
    for timeline in timelines:
        db.session.delete(timeline)
    db.session.commit()
