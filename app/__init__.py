from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config, limiter  # ✅ Import limiter from config.py
from app.auth import auth_bp
from app.routes import resources_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Initialize JWT
    JWTManager(app)

    # ✅ Attach `limiter` to the app
    limiter.init_app(app)

    # ✅ Custom error handler for 429 errors
    @app.errorhandler(429)
    def ratelimit_error(e):
        return jsonify({"error": "Rate limit exceeded", "message": str(e.description)}), 429

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(resources_bp, url_prefix='/resources')

    @app.route('/')
    def home():
        return {"message": "Welcome to API in a Flask!"}, 200


    return app
