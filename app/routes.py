from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import resources
from app.config import limiter  # ✅ Import limiter from config, not app
from utils.security_utils import SecurityEnhancements

resources_bp = Blueprint("resources", __name__)

@resources_bp.route('/<resource_type>', methods=['GET'])
@jwt_required()
def get_resources(resource_type):
    """ Get all items for a given resource type """
    try:
        resource_type = SecurityEnhancements.validate_input(resource_type)
    except ValueError:
        return jsonify({"error": "Invalid resource type"}), 400
    
    if resource_type not in resources:
        return jsonify({"error": f"Resource '{resource_type}' not found"}), 404
    return jsonify(resources[resource_type])

@resources_bp.route('/<resource_type>', methods=['POST'])
@jwt_required()
def add_resource(resource_type):
    """ Add an item to a given resource type """
    current_user = get_jwt_identity()
    user = next((u for u in resources["users"] if u["username"] == current_user), None)
    
    if not user or user["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        resource_type = SecurityEnhancements.validate_input(resource_type)
    except ValueError:
        return jsonify({"error": "Invalid resource type"}), 400

    if resource_type not in resources:
        resources[resource_type] = []

    new_item = request.get_json()

    # ✅ Validate new item data
    try:
        for key in new_item:
            new_item[key] = SecurityEnhancements.validate_input(str(new_item[key]))
    except ValueError:
        return jsonify({"error": "Invalid input data"}), 400

    new_item["id"] = len(resources[resource_type]) + 1
    resources[resource_type].append(new_item)
    return jsonify(new_item), 201

@resources_bp.route('/<resource_type>/<int:item_id>', methods=['PUT'])
@jwt_required()
@limiter.limit("3 per minute")  # ✅ Apply rate limit to updates
def update_resource(resource_type, item_id):
    """ Update an item in a given resource type """
    current_user = get_jwt_identity()
    user = next((u for u in resources["users"] if u["username"] == current_user), None)

    if not user or user["role"] != "admin":
        return jsonify({"error": "Unauthorized – Only admins can update resources"}), 403
    
    try:
        resource_type = SecurityEnhancements.validate_input(resource_type)
    except ValueError:
        return jsonify({"error": "Invalid resource type"}), 400

    if resource_type not in resources:
        return jsonify({"error": f"Resource '{resource_type}' not found"}), 404

    resource_list = resources[resource_type]
    item = next((item for item in resource_list if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found in '{resource_type}'"}), 404

    updated_data = request.get_json()

    # ✅ Validate updated data
    try:
        for key in updated_data:
            updated_data[key] = SecurityEnhancements.validate_input(str(updated_data[key]))
    except ValueError:
        return jsonify({"error": "Invalid input data"}), 400
    
    item.update(updated_data)

    return jsonify(item), 200

@resources_bp.route('/<resource_type>/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_resource(resource_type, item_id):
    """ Delete an item from a given resource type """
    current_user = get_jwt_identity()
    user = next((u for u in resources["users"] if u["username"] == current_user), None)
    
    if not user or user["role"] != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    if resource_type not in resources:
        return jsonify({"error": f"Resource '{resource_type}' not found"}), 404

    resource_list = resources[resource_type]
    item = next((item for item in resource_list if item["id"] == item_id), None)
    if not item:
        return jsonify({"error": f"Item with ID {item_id} not found in '{resource_type}'"}), 404

    resources[resource_type] = [item for item in resource_list if item["id"] != item_id]
    return jsonify({"message": f"Item with ID {item_id} deleted from '{resource_type}'"}), 200
