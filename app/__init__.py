from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_limiter.storage.redis import RedisStorage
import redis
from app.config import Config
from app.routes import resources_bp
from app.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Initialize JWT
    JWTManager(app)

    # ✅ Add Rate Limiting with Redis (Persistent Storage)
    limiter = Limiter(
        get_remote_address,
        app=app,
        storage_uri="redis://localhost:6379"  # Connects to Redis running locally
    )

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(resources_bp, url_prefix='/resources')

    # Default route to prevent 404 on "/"
    @app.route('/')
    @limiter.limit("8 per minute")  # Apply a custom rate limit to the home route
    def home():
        return {"message": "Welcome to API in a Flask!"}

    return app
