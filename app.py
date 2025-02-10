import uuid

from flask import Flask, request
from db import stores, items
app = Flask(__name__)


@app.get("/stores")
def get_store():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4.hex
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201

@app.post("/item")
def add_item():
    item_data = request.get_json()
    if item_data["store_id"] not in stores:
        return {"message": "Store isn't Found!"}, 404

    item_id = uuid.uuid4.hex
    item = {**item_data, "id":item_id}
    items[item_id] = item
    return item, 201

@app.get("/store/<string:store_id>")
def get_specific_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store isn't Found!"}, 404

@app.get("/items")
def get_items():
    return {"items":list(items.values())}

@app.get("/item/<string:item_id>")
def get_specific_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        return {"message": "Store isn't Found!"}, 404