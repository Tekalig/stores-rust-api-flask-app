import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("item", __name__, description="Operation on items")


# retrieve all items
@blp.route("/items")
class ItemList(MethodView):
    # get all items
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()


# item route with the same endpoints but different method
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # get specific item by item id
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(http_status_code=400, message="Item isn't Found!", )

    # update specific item by item id
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(http_status_code=400, message="Item isn't Found!", )

    # delete specific item by item id
    @blp.response(200, ItemSchema)
    def delete(self, item_id):
        try:
            del_item = items[item_id]
            del items[item_id]
            return del_item
        except KeyError:
            abort(http_status_code=400, message="Item isn't Found!", )


# Create a new store
@blp.route("/item")
class NewItem(MethodView):
    # add new item to specific store
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        if item_data["store_id"] not in stores:
            abort(http_status_code=400, message="Store isn't Found!", )

        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(http_status_code=400, message="Item already exists", )

        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201