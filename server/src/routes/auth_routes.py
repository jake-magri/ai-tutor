import bcrypt
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.db.db import users_collection

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/api/users/me", methods=["GET"])
@jwt_required()
def get_me():
    current_user = get_jwt_identity()
    user = users_collection.find_one({"email": current_user}, {"_id": 0, "password": 0})
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user), 200

@auth_routes.route("/api/users/login", methods=["POST"])
def login_user():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    user = users_collection.find_one({"email": data["email"]})

    if not user or not bcrypt.checkpw(data["password"].encode('utf-8'), user["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])

    return jsonify({
        "id_token": token,
        "user": {
            "email": user["email"],
            "username": user.get("username")
        }
    }), 200

@auth_routes.route("/api/users", methods=["POST"])
def register_user():
    data = request.get_json()

    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt())
    user_data = {
        "email": data["email"],
        "password": hashed_password,
        "username": data.get("username")
    }

    try:
        users_collection.insert_one(user_data)
    except Exception as e:
        return jsonify({"message": f"Error creating user: {str(e)}"}), 500

    return jsonify({"message": "User created successfully"}), 201
