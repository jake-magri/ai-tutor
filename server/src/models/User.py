from werkzeug.security import generate_password_hash, check_password_hash
from src.db.db import users_collection  # MongoDB interaction

def create_user(user_data):
    # Ensure email and password are provided
    if not user_data.get("email") or not user_data.get("password"):
        raise ValueError("User data must include 'email' and 'password'")
    
    # Check if the user already exists
    if users_collection.find_one({"email": user_data["email"]}):
        raise ValueError("User already exists")
    
    # Hash the password and save the user
    user_data["password"] = generate_password_hash(user_data["password"])
    users_collection.insert_one(user_data)

def find_user_by_email(email):
    # Return the user document or None if not found
    return users_collection.find_one({"email": email})

def authenticate_user(email, password):
    user = find_user_by_email(email)
    if user and check_password_hash(user["password"], password):
        return user
    return None
