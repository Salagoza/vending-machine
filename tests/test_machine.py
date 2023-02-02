from flask import Flask
from flask.testing import FlaskClient

from models import Machine


def test_create_machine(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    with app.app_context():
        assert Machine.query.count() == 1
        assert Machine.query.first().name == "Machine1"


def test_get_all_machine(client: FlaskClient):
    response = client.get("/api/machine/get")
    assert response.status_code == 200


def test_get_machine_by_id(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    response = client.get("/api/machine/get/1")
    assert response.status_code == 200


def test_update_machine(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    client.put(
        "/api/machine/update/1", data={"name": "Machine2", "address": "Ic Building"}
    )
    with app.app_context():
        assert Machine.query.count() == 1
        assert Machine.query.first().name == "Machine2"
        assert Machine.query.first().address == "Ic Building"


def test_delete_machine(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    client.delete("/api/machine/delete/1")

    with app.app_context():
        assert Machine.query.count() == 0
