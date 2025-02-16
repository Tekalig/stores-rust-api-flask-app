from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from config.db import db
from models import TagModel, StoreModel, ItemModel
from schemas import TagSchema, TagAndItemSchema

blp = Blueprint("tag", __name__, description="Operation on items")

@blp.route("/store/<string:store_id>/tag/")
class TagInStore(MethodView):
    # get all tags for specific id
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        return store.tags.all()
    
    # add new tag to specific store
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema)
    def post(self, tag_data, store_id):
        tag = TagModel(**tag_data, store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Insertion Error occurred while inserting duplicate row tags.")
        except SQLAlchemyError:
            abort(500, message="Insertion Error occurred while inserting tags.")

        return tag

@blp.route("/tag/<string:tag_id>/")
class TagList(MethodView):
    # get specific tag
    @blp.response(200, TagSchema)
    def get(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)

        return tag

    # delete specific tag
    @blp.response(202, TagSchema)
    def delete(self, tag_id):
        tag = TagModel.query.get_or_404(tag_id)
        try:
            db.session.delete(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return tag

@blp.route("/item/<string:item_id>/tag/<string:tag_id>/")
class LinkItemAndTag(MethodView):
    # link the tag with item
    @blp.response(201, TagAndItemSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(400, message="Error occurred while linking the tag with item")

        return {"message":"the tag linked successfully with item", "items":item, "tags":tag}

    # unlink the tag from item
    @blp.response(200, TagAndItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(400, message="Error occurred while unlinking the tag from item")

        return {"message":"the tag unlinked successfully from item", "items":item, "tags":tag}


