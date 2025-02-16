from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from config.db import db
from models import StoreModel
from schemas import StoreSchema, StoreUpdateSchema

blp = Blueprint("store", __name__, description="Operation on stores")


# retrieve all stores
@blp.route("/stores")
class StoreList(MethodView):
    # get all stores
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()


# store route with the same endpoints but different method
@blp.route("/store/<string:store_id>")
class Stores(MethodView):
    # get specific store by store id
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store

    # update specific store by store id
    @blp.arguments(StoreUpdateSchema)
    @blp.response(200, StoreSchema)
    def put(self, store_data, store_id):
        store = StoreModel.query.get(store_id)
        try:
            if store:
                store.name = store_data["name"]
            else:
                store = StoreModel(id=int(store_id), **store_data)

            db.session.add(store)
            db.session.commit()
            return store
        except IntegrityError:
            abort(400, message="Insertion Error occurred while inserting duplicate store name")


    # delete specific store by store id
    @blp.response(200, StoreSchema)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        print(store)
        deleted_store = store
        db.session.delete(store)
        db.session.commit()

        return {"message":"Store deleted successfully", "deleted_store":deleted_store}



# Create a new store
@blp.route("/store")
class NewStore(MethodView):
    # add new store
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Insertion Error occurred while inserting duplicate store name")
        except SQLAlchemyError:
            abort(500, message="Insertion Error occurred while inserting store.")
        return store, 201
