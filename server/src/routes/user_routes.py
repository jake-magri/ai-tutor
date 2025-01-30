from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import find_user_by_email, create_user  # Use models for DB interaction
from db.db import users_collection

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/api/users", methods=["POST"])
def register_user():
    data = request.get_json()
    if find_user_by_email(data["email"]):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])
    create_user({"email": data["email"], "password": hashed_password})
    return jsonify({"message": "User created successfully"}), 201

# Login user
@user_routes.route("/api/users/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = find_user_by_email(email)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify({"token": access_token}), 200

# Get logged-in user info (requires token)
@user_routes.route("/api/users/me", methods=["GET"])
@jwt_required()
def get_me():
    current_user = get_jwt_identity()  # Get email from JWT token
    user = users_collection.find_one({"email": current_user}, {"_id": 0, "password": 0})  # Exclude sensitive fields
    return jsonify(user), 200