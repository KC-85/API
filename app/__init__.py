from flask import Flask
from flask_jwt_extended import JWTManager, get_jwt_identity
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from limits.storage import RedisStorage
from app.config import Config
from app.routes import resources_bp
from app.auth import auth_bp

# ✅ Define a function for per-user rate limiting
def rate_limit_key():
    try:
        return get_jwt_identity() or get_remote_address()
    except RuntimeError:
        return get_remote_address()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize JWT
    JWTManager(app)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

    # ✅ Initialize Limiter using function instead of direct call
    limiter = Limiter(
    key_func=rate_limit_key,  # Apply per-user rate limiting
    storage_uri="redis://localhost:6379",
    strategy="moving-window"
)

    # ✅ Attach Limiter to the Flask app
    limiter.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(resources_bp, url_prefix='/resources')

    # Default route to prevent 404 on "/"
    @app.route('/')
    @limiter.limit("8 per minute")  # Apply a custom rate limit to the home route
    def home():
        return {"message": "Welcome to API in a Flask!"}

    return app
