from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import config
from app.routes import resources_bp
from app.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/*":{"origins":
    app.config["CORS_ORIGINS"]}})

    # Initialize JWT
    JWTManager(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(resources_bp, url_prefix='/resources')

    return app
