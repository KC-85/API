from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.models import resources
from utils.security_utils import SecurityEnhancements

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """ Registers a new user """
    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    # ✅ Validate input
    try:
        username = SecurityEnhancements.validate_input(username)
        password = SecurityEnhancements.validate_input(password)
    except ValueError:
        return jsonify({"error": "Invalid characters in input"}), 400

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if any(user["username"] == username for user in resources["users"]):
        return jsonify({"error": "User already exists"}), 409
    
    # Hash password securely
    hashed_password = SecurityEnhancements.secure_hash(password)

    new_user = {"id": len(resources["users"]) + 1, "username": username, "role": "user"}
    resources["users"].append(new_user)
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """ Authenticates a user and returns a JWT token """
    data = request.get_json()
    username, password = data.get("username"), data.get("password")

    # ✅ Validate input
    try:
        username = SecurityEnhancements.validate_input(username)
        password = SecurityEnhancements.validate_input(password)
    except ValueError:
        return jsonify({"error": "Invalid characters in input"}), 400

    user = next((user for user in resources["users"] if user["username"] == username), None)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)
