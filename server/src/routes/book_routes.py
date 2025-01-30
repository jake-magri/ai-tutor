from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db.db import users_collection

book_routes = Blueprint("book_routes", __name__)

# Save a book to a user's collection
@book_routes.route("/api/users/books", methods=["PUT"])
@jwt_required()
def save_book():
    current_user_email = get_jwt_identity()
    book_data = request.get_json()

    if not book_data or "id" not in book_data:
        return jsonify({"error": "Book data with a valid ID is required"}), 400

    users_collection.update_one(
        {"email": current_user_email},
        {"$addToSet": {"saved_books": book_data}}  # Ensures no duplicate entries
    )

    return jsonify({"message": "Book saved successfully"}), 200


# Delete a saved book from a user's collection
@book_routes.route("/api/users/books/<book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    current_user_email = get_jwt_identity()

    result = users_collection.update_one(
        {"email": current_user_email},
        {"$pull": {"saved_books": {"id": book_id}}}
    )

    if result.modified_count == 0:
        return jsonify({"error": "Book not found or already removed"}), 404

    return jsonify({"message": "Book removed successfully"}), 200
