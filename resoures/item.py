import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import items

blp = Blueprint("item", __name__, description="Operation on items")


# retrieve all items
@blp.route("/items")
class ItemList(MethodView):
    # get all items
    def get(self):
        return {"items": list(items.values())}


# item route with the same endpoints but different method
@blp.route("item/<string:item_id>")
class Item(MethodView):
    # get specific item by item id
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(http_status_code=400, message="Item isn't Found!", )

    # update specific item by item id
    def put(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(http_status_code=400, message="Bad request, price,and name should be include.", )

        try:
            item = items[item_id]
            item |= item_data

            return item
        except KeyError:
            abort(http_status_code=400, message="Item isn't Found!", )

    # delete specific item by item id
    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted successfully"}
        except KeyError:
            abort(http_status_code=400, message="Item isn't Found!", )


# Create a new store
@blp.route("/item")
class NewItem(MethodView):
    # add new item to specific store
    def post(self):
        item_data = request.get_json()
        if "store_id" not in item_data or "price" not in item_data or "name" not in item_data:
            abort(http_status_code=400, message="Bad request, price, name, and store_id should be include.", )

        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(http_status_code=400, message="Item already exists", )

        if item_data["store_id"] not in stores:
            abort(http_status_code=400, message="Store isn't Found!", )

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201