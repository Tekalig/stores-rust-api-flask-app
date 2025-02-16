from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from config.db import db
from models import TagModel, StoreModel
from schemas import TagSchema

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