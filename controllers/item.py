from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from config.db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("item", __name__, description="Operation on items")


# retrieve all items
@blp.route("/items")
class ItemList(MethodView):
    # get all items
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()


# item route with the same endpoints but different method
@blp.route("/item/<string:item_id>")
class Item(MethodView):
    # get specific item by item id
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    # update specific item by item id
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        try:
            if item:
                item.name = item_data["name"]
                item.price = item_data["price"]
            else:
                item = ItemModel(id=item_id, **item_data)

            db.session.add(item)
            db.session.commit()
            return item
        except IntegrityError:
            abort(400, message="Insertion Error occurred while inserting duplicate row items.")


    # delete specific item by item id
    @blp.response(200, ItemSchema)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)

        deleted_item = item
        db.session.delete(item)
        db.session.commit()
        return {"message":"Item deleted successfully", "deleted_item": deleted_item}


# Create a new store
@blp.route("/item")
class NewItem(MethodView):
    # add new item to specific store
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Insertion Error occurred while inserting duplicate row items.")
        except SQLAlchemyError:
            abort(500, message="Insertion Error occurred while inserting items.")
        return item, 201