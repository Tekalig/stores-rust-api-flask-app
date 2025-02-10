from flask import Flask
from flask_smorest import Api

# import custom blueprint
from resoures.item import blp as ItemBlueprint
from resoures.store import blp as StoreBlueprint

# initialize flask app
app = Flask(__name__)

# config the flask app
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["API_TITLE"] = "stores rust api"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

# initialize the api
api = Api(app)

# use the route
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
