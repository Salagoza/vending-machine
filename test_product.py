from models import Product

def test_create_product(client, app):
    client.post("/api/machine/create", data={"name": "Machine1", "address": "Tennis Court"})
    client.post("/api/product/create",
                data={"name": "Lipton", "price": 20, "type": "beverage", "machine_id": 1, "quantity": 1})
    with app.app_context():
        assert Product.query.count() == 1
        assert Product.query.first().name == "Lipton"

def test_get_all_product(client):
    response = client.get("/api/product/get")
    assert response.status_code == 200

def test_get_product_by_id(client, app):
    client.post("/api/product/create",
                data={"name": "Lipton", "price": 20, "type": "beverage", "machine_id": 1, "quantity": 1})
    response = client.get("/api/product/get/1")
    assert response.status_code == 200

def test_update_product(client, app):
    client.post("/api/product/create",
                data={"name": "Lipton", "price": 20, "type": "beverage", "machine_id": 1, "quantity": 1})
    client.put("/api/product/update/1", data={"name": "", "price": "", "type": "", "quantity": 2})
    with app.app_context():
        assert Product.query.first().name == "Lipton"
        assert Product.query.first().quantity == 2

def test_get_delete_machine(client, app):
    client.post("/api/product/create",
                data={"name": "Lipton", "price": 20, "type": "beverage", "machine_id": 1, "quantity": 10})
    client.delete("/api/product/delete", data={"name": "Lipton", "machine_id": 1, "quantity": 10})

    with app.app_context():
        assert Product.query.count() == 0
