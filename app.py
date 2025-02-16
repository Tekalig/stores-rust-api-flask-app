import os

from flask import Flask
from flask_smorest import Api
from dotenv import load_dotenv

from config.db import db
import models

# import custom blueprint
from resoures.item import blp as ItemBlueprint
from resoures.store import blp as StoreBlueprint

#  Load environmental variable from .env file
load_dotenv()

# Get database connection parameters from the environment
DB_USERNAME = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Create the SQLAlchemy connection URI
postgres_db_url = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# use function to initialize the app
def create_app():
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
    app.config["SQLALCHEMY_DATABASE_URI"] = postgres_db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # initialize database
    db.init_app(app)

    # before creating or request anything create tables
    with app.app_context():
        db.create_all()

    # initialize the api
    api = Api(app)

    # use the route
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app
