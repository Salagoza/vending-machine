from flask import Flask
from flask.testing import FlaskClient

from models import Machine


def test_create_machine_200(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    with app.app_context():
        assert Machine.query.count() == 1
        assert Machine.query.first().name == "Machine1"


def test_create_machine_500(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    response = client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    with app.app_context():
        assert response.status_code == 500


def test_get_all_machine(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    client.post("/api/machine/create", data={"name": "Machine2", "address": "IC Bld."})
    response = client.get("/api/machine/get")
    with app.app_context():
        assert response.status_code == 200
        assert Machine.query.count() == 2


def test_get_machine_by_id_200(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    response = client.get("/api/machine/get/1")
    assert response.status_code == 200


def test_get_machine_by_id_404(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    response = client.get("/api/machine/get/2")
    assert response.status_code == 404


def test_update_machine_200(client: FlaskClient, app: Flask):
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


def test_update_machine_404(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    response = client.put(
        "/api/machine/update/2", data={"name": "Machine2", "address": "Ic Building"}
    )
    with app.app_context():
        assert response.status_code == 404


def test_delete_machine_200(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    client.delete("/api/machine/delete/1")

    with app.app_context():
        assert Machine.query.count() == 0


def test_delete_machine_404(client: FlaskClient, app: Flask):
    client.post(
        "/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"}
    )
    response = client.delete("/api/machine/delete/2")

    with app.app_context():
        assert response.status_code == 404
