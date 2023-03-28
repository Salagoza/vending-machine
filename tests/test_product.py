from flask import Flask
from flask.testing import FlaskClient

import constants
from models import Product


def test_create_product(client: FlaskClient, app: Flask):
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
    with app.app_context():
        assert Product.query.count() == 1
        assert Product.query.first().name == "Lipton"


def test_create_product_already_exists(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Seven 11"},
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
    with app.app_context():
        assert Product.query.count() == 1
        assert Product.query.first().name == "Lipton"
        assert Product.query.first().quantity == 2


def test_get_all_product(client: FlaskClient, app: Flask):
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
            "name": "Ichitan Lemon",
            "price": 20,
            "type": "beverage",
            "machine_id": 2,
            "quantity": 1,
        },
    )

    response = client.get("/api/product/get")
    with app.app_context():
        assert response.status_code == 200
        assert Product.query.count() == 2


def test_get_product_by_id_200(client: FlaskClient, app: Flask):
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
    response = client.get("/api/product/get/1")
    assert response.status_code == 200


def test_get_product_by_id_404(client: FlaskClient, app: Flask):
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
    response = client.get("/api/product/get/2")
    assert response.status_code == 404


def test_update_product_200(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "IC Bld. Floor.4"},
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
    response = client.put(
        constants.update_product_endpoint + "/1",
        data={"name": "", "price": "", "type": "", "quantity": 2},
    )
    with app.app_context():
        assert response.status_code == 200
        assert Product.query.first().name == "Lipton"
        assert Product.query.first().quantity == 2


def test_update_product_400(client: FlaskClient, app: Flask):
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
    response = client.put(
        constants.update_product_endpoint + "/1",
        data={"name": "", "price": "", "type": "", "quantity": 0},
    )
    with app.app_context():
        assert response.status_code == 400


def test_update_product_404(client: FlaskClient, app: Flask):
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
    response = client.put(
        constants.update_product_endpoint + "/2",
        data={"name": "", "price": "", "type": "", "quantity": 2},
    )
    with app.app_context():
        assert response.status_code == 404


def test_get_delete_product_200(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "IC Bld. Floor.2"},
    )

    client.post(
        constants.create_product_endpoint,
        data={
            "name": "Lipton",
            "price": 20,
            "type": "beverage",
            "machine_id": 1,
            "quantity": 10,
        },
    )
    response = client.delete(
        constants.delete_product_endpoint,
        data={"name": "Lipton", "machine_id": 1, "quantity": 10},
    )

    with app.app_context():
        assert response.status_code == 200
        assert Product.query.count() == 0


def test_get_delete_product_partial_200(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "IC Bld. Floor.3"},
    )

    client.post(
        constants.create_product_endpoint,
        data={
            "name": "Lipton",
            "price": 20,
            "type": "beverage",
            "machine_id": 1,
            "quantity": 10,
        },
    )
    response = client.delete(
        constants.delete_product_endpoint,
        data={"name": "Lipton", "machine_id": 1, "quantity": 5},
    )

    with app.app_context():
        assert response.status_code == 200
        assert Product.query.count() == 1


def test_delete_product_404(client: FlaskClient, app: Flask):
    client.post(
        constants.create_product_endpoint,
        data={
            "name": "Lipton",
            "price": 20,
            "type": "beverage",
            "machine_id": 1,
            "quantity": 10,
        },
    )
    response = client.delete(
        constants.delete_product_endpoint,
        data={"name": "Lipton", "machine_id": 2, "quantity": 10},
    )

    with app.app_context():
        assert response.status_code == 404
