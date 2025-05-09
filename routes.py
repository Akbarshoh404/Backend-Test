from flask import Blueprint, request, jsonify
from data import database

routes = Blueprint('routes', __name__)

@routes.route("/get-users", methods=["GET"])
def get_users():
    return jsonify(database)

@routes.route("/get-user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = next((user for user in database if user["user_id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    extra = request.args.get("extra")
    if extra:
        user["extra"] = extra

    return jsonify(user)

@routes.route("/add-user", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    new_id = max(user["user_id"] for user in database) + 1
    new_user = {
        "user_id": new_id,
        "name": data["name"],
        "email": data["email"]
    }
    database.append(new_user)
    return jsonify(new_user), 201

@routes.route("/update-user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    user = next((user for user in database if user["user_id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    return jsonify(user)

@routes.route("/patch-user/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    data = request.get_json()
    user = next((user for user in database if user["user_id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if "name" in data:
        user["name"] = data["name"]
    if "email" in data:
        user["email"] = data["email"]
    return jsonify(user)
