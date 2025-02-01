from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
from src.models.User import find_user_by_email, create_user  # Use models for DB interaction
from src.db.db import users_collection  # Import the users_collection from the database module

auth_routes = Blueprint("auth_routes", __name__)

# Get logged-in user info (requires token)
@auth_routes.route("/api/users/me", methods=["GET"])
@jwt_required()
def get_me():
    current_user = get_jwt_identity()  # Get email from JWT token
    user = users_collection.find_one({"email": current_user}, {"_id": 0, "password": 0})  # Exclude sensitive fields
    if not user:
        return jsonify({"message": "User not found"}), 404
    return jsonify(user), 200

@auth_routes.route("/api/users/login", methods=["POST"])
def login_user():
    data = request.get_json()

    # Validate input
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    user = find_user_by_email(data.get("email"))

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    # Create the access token
    token = create_access_token(identity=user["email"])

    # Return token along with additional user info (e.g., email, username)
    return jsonify({
        "access_token": token,
        "user": {
            "email": user["email"],
            "username": user.get("username")
        }
    }), 200

@auth_routes.route("/api/users", methods=["POST"])
def register_user():
    data = request.get_json()

    # Validate input
    if not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email and password are required"}), 400

    # Check if the user already exists
    if find_user_by_email(data["email"]):
        return jsonify({"message": "User already exists"}), 400

    # Hash the password and save the user
    hashed_password = generate_password_hash(data["password"])
    user_data = {
        "email": data["email"],
        "password": hashed_password,
        "username": data.get("username")  # Optional username
    }

    create_user(user_data)

    return jsonify({"message": "User created successfully"}), 201
