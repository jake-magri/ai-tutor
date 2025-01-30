from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from models.User import find_user_by_email, create_user  # Use models for DB interaction

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/api/users/login", methods=["POST"])
def login_user():
    data = request.get_json()
    user = find_user_by_email(data["email"])

    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(identity=user["email"])
    return jsonify({"access_token": token}), 200


@auth_routes.route("/api/users", methods=["POST"])
def register_user():
    data = request.get_json()

    if find_user_by_email(data["email"]):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(data["password"])
    create_user({"email": data["email"], "password": hashed_password})

    return jsonify({"message": "User created successfully"}), 201
