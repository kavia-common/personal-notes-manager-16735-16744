import os
from datetime import timedelta


class Config:
    """Base configuration for the Flask app."""
    # PUBLIC_INTERFACE
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "change-this-in-production")
    API_TITLE = "Notes Backend API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/docs"
    OPENAPI_SWAGGER_UI_PATH = ""
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SESSION_COOKIE_NAME = os.getenv("SESSION_COOKIE_NAME", "notes_session")
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
