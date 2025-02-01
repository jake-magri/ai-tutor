from src.db.db import users_collection  # MongoDB interaction


def create_user(user_data):
    # Ensure email and password are provided
    if not user_data.get("email") or not user_data.get("password"):
        raise ValueError("User data must include 'email' and 'password'")
    
    # Check if the user already exists
    if users_collection.find_one({"email": user_data["email"]}):
        raise ValueError("User already exists")

    users_collection.insert_one(user_data)

def find_user_by_email(email):
    # Return the user document or None if not found
    return users_collection.find_one({"email": email})
