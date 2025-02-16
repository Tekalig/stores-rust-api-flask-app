from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token

from config.db import db
from models import UserModel
from schemas import UserSchema

blp = Blueprint("Users", __name__, description="Operation on users")

@blp.route("/signup/")
class UserRegister(MethodView):
    #
    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, user_data):
        user = UserModel(**user_data)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(400, message=str(e))

        return user

@blp.route("/login/")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()

        if user:
            access_token = create_access_token(user.id)
            return {"access_token":access_token}
        abort(400, message="Invalid credentials")


@blp.route("/user/<int:user_id>/")
class UserList(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)

        return user