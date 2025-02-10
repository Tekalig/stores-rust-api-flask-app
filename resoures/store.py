import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint

from db import stores

blp = Blueprint("store", __name__, description="Operation on stores")


# retrieve all stores
@blp.route("/stores")
class StoreList(MethodView):
    # get all stores
    def get(self):
        return {"stores": list(stores.values())}


# store route with the same endpoints but different method
@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    # get specific store by store id
    def get(self, store_id):
        try:
            return stores[store_id]
        except KeyError:
            abort(http_status_code=400, message="Store isn't Found!", )

    # delete specific store by store id
    def delete(self, store_id):
        try:
            del stores[store_id]
            return {"message": "Store deleted successfully"}
        except KeyError:
            abort(http_status_code=400, message="Store isn't Found!", )

    # update specific store by store id
    def put(self, store_id):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(http_status_code=400, message="Bad request, name should be include.", )

        try:
            store = stores[store_id]
            store |= store_data

            return store
        except KeyError:
            abort(http_status_code=400, message="Store isn't Found!", )


# Create a new store
@blp.route("/store")
class NewStore(MethodView):
    # add new store
    def post(self):
        store_data = request.get_json()
        if "name" not in store_data:
            abort(http_status_code=400, message="Bad request, Ensure name field include", )

        for store in stores.values():
            print(store)
            if store_data["name"] == store["name"]:
                abort(http_status_code=400, message="Store already exists", )

        store_id = uuid.uuid4().hex
        store = {**store_data, "id": store_id}
        stores[store_id] = store
        return store, 201
