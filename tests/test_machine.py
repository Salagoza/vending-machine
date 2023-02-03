from flask import Flask
from flask.testing import FlaskClient

import constants
from models import Machine


def test_create_machine_200(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "IC Bld. Floor.2"},
    )
    with app.app_context():
        assert Machine.query.count() == 1
        assert Machine.query.first().name == "Machine1"


def test_create_machine_500(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "IC Bld. Floor.3"},
    )
    response = client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "IC Bld. Floor.3"},
    )
    with app.app_context():
        assert response.status_code == 500


def test_get_all_machine(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Aditayathorn Bld. Floor.1"},
    )
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine2", "address": "Aditayathorn Bld. Floor.2"},
    )
    response = client.get("/api/machine/get")
    with app.app_context():
        assert response.status_code == 200
        assert Machine.query.count() == 2


def test_get_machine_by_id_200(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "IC Bld. 1502 Com Sci Lab"},
    )
    response = client.get("/api/machine/get/1")
    assert response.status_code == 200


def test_get_machine_by_id_404(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Tennis Court"},
    )
    response = client.get("/api/machine/get/2")
    assert response.status_code == 404


def test_update_machine_200(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Tennis Court"},
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
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "BasketBall Court"},
    )
    response = client.put(
        constants.update_machine_endpoint + "/2",
        data={"name": "Machine2", "address": "Swimming Pool"},
    )
    with app.app_context():
        assert response.status_code == 404


def test_delete_machine_200(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Badminton Court"},
    )
    client.delete(constants.delete_machine_endpoint + "/1")

    with app.app_context():
        assert Machine.query.count() == 0


def test_delete_machine_404(client: FlaskClient, app: Flask):
    client.post(
        constants.create_machine_endpoint,
        data={"name": "Machine1", "address": "Football Field"},
    )
    response = client.delete(constants.delete_machine_endpoint + "/2")

    with app.app_context():
        assert response.status_code == 404
