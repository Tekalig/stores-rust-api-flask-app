import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import stores
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("store", __name__, description="Operation on stores")


# retrieve all stores
@blp.route("/stores")
class StoreList(MethodView):
    # get all stores
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return stores.values()


# store route with the same endpoints but different method
@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    # get specific store by store id
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(http_status_code=400, message="Store isn't Found!", )

    # update specific store by store id
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        try:
            store = stores[store_id]
            store |= store_data

            return store
        except KeyError:
            abort(http_status_code=400, message="Store isn't Found!", )

    # delete specific store by store id
    @blp.response(200, StoreSchema)
    def delete(self, store_id):
        try:
            del_store = stores[store_id]
            del stores[store_id]
            return del_store
        except KeyError:
            abort(http_status_code=400, message="Store isn't Found!", )



# Create a new store
@blp.route("/store")
class NewStore(MethodView):
    # add new store
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        for store in stores.values():
            if store_data["name"] == store["name"]:
                abort(http_status_code=400, message="Store already exists", )

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201
