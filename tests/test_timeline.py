from flask import Flask
from flask.testing import FlaskClient

import constants
from models import ProductLog, Timeline


def test_create_product(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "7-Eleven"},
    )
    client.post(
        constants.create_product_endpoint,
        data={
            "name": "Lipton",
            "price": 20,
            "type": "beverage",
            "machine_id": 1,
            "quantity": 1,
        },
    )
    with app.app_context():
        assert Timeline.query.count() == 2


def test_get_timeline_by_machine_id(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Co-working space"},
    )
    client.post(
        constants.create_product_endpoint,
        data={
            "name": "Lipton",
            "price": 20,
            "type": "beverage",
            "machine_id": 1,
            "quantity": 1,
        },
    )
    response = client.get(constants.get_timeline_endpoint + "/1")
    with app.app_context():
        assert response.status_code == 200
        assert Timeline.query.count() == 2


def test_get_product_timeline_by_product_name(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Apple Store"},
    )
    client.post(
        constants.create_product_endpoint,
        data={
            "name": "Lipton",
            "price": 20,
            "type": "beverage",
            "machine_id": 1,
            "quantity": 1,
        },
    )

    client.post(
        constants.create_product_endpoint,
        data={
            "name": "Lipton",
            "price": 20,
            "type": "beverage",
            "machine_id": 1,
            "quantity": 1,
        },
    )

    client.get(
        constants.get_product_timeline_endpoint,
        data={"name": "Lays"},
    )

    with app.app_context():
        assert ProductLog.query.count() == 2
