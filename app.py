import uuid
from flask import Flask, request, message_flashed
from flask_smorest import abort
from db import stores, items
app = Flask(__name__)

# store endpoints
@app.get("/stores")
def get_store():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    if "name" not in store_data:
        abort(http_status_code=400, message_flashed="Bad request, Ensure name field include",)

    for store in stores:
        if store_data["name"] == store["name"]:
            abort(http_status_code=400, message="Store already exists",)

    store_id = uuid.uuid4().hex
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201


@app.get("/store/<string:store_id>")
def get_specific_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        abort(http_status_code=400, message="Store isn't Found!",)

#  Items endpoints
@app.get("/items")
def get_items():
    return {"items":list(items.values())}

@app.get("/item/<string:item_id>")
def get_specific_item(item_id):
    try:
        return items[item_id]
    except KeyError:
        abort(http_status_code=400, message="Item isn't Found!",)

@app.post("/item")
def create_item():
    item_data = request.get_json()
    if "store_id" not in item_data or "price" not in item_data or "name" not in item_data:
        abort(http_status_code=400, message="Bad request, price, name, and store_id should be include.",)

    for item in items:
        if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
            abort(http_status_code=400, message="Item already exists",)

    if item_data["store_id"] not in stores:
        abort(http_status_code=400, message="Store isn't Found!",)

    item_id = uuid.uuid4().hex
    item = {**item_data, "id":item_id}
    items[item_id] = item
    return item, 201


@app.delete("/item/<string:item_id>")
def delete_specific_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item deleted successfully"}
    except KeyError:
        abort(http_status_code=400, message="Item isn't Found!",)