from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.db.db import users_collection

book_routes = Blueprint("book_routes", __name__)

@book_routes.route("/api/users/books", methods=["PUT"])
@jwt_required()
def save_book():
    current_user_email = get_jwt_identity()
    book_data = request.get_json()

    if not book_data or "bookId" not in book_data:
        return jsonify({"error": "Book data with a valid ID is required"}), 400

    users_collection.update_one(
        {"email": current_user_email},
        {"$addToSet": {"savedBooks": book_data}}
    )

    return jsonify({"message": "Book saved successfully"}), 200

@book_routes.route("/api/users/books/<book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    current_user_email = get_jwt_identity()

    result = users_collection.update_one(
        {"email": current_user_email},
        {"$pull": {"savedBooks": {"bookId": book_id}}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Book not found or already removed"}), 404
    
    updated_user = users_collection.find_one({"email": current_user_email}, {"_id": 0, "password": 0})

    return jsonify(updated_user), 200