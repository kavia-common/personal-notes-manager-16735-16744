from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from .config import Config
from .routes.health import blp as health_blp
from .routes.users import blp as users_blp
from .routes.sessions import blp as sessions_blp
from .routes.notes import blp as notes_blp


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config.from_object(Config)

# CORS
CORS(app, resources={r"/*": {"origins": app.config.get("CORS_ORIGINS", "*")}})

# OpenAPI / Swagger configuration
app.config["API_TITLE"] = Config.API_TITLE
app.config["API_VERSION"] = Config.API_VERSION
app.config["OPENAPI_VERSION"] = Config.OPENAPI_VERSION
app.config["OPENAPI_URL_PREFIX"] = Config.OPENAPI_URL_PREFIX
app.config["OPENAPI_SWAGGER_UI_PATH"] = Config.OPENAPI_SWAGGER_UI_PATH
app.config["OPENAPI_SWAGGER_UI_URL"] = Config.OPENAPI_SWAGGER_UI_URL

api = Api(app)

# Register blueprints
api.register_blueprint(health_blp)
api.register_blueprint(users_blp)
api.register_blueprint(sessions_blp)
api.register_blueprint(notes_blp)
