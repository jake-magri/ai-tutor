from werkzeug.security import generate_password_hash, check_password_hash
from db.db import users_collection  # MongoDB interaction

# Create a new user
def create_user(user_data):
    if not user_data.get("email") or not user_data.get("password"):
        raise ValueError("User data must include 'email' and 'password'")
    
    if users_collection.find_one({"email": user_data["email"]}):
        raise ValueError("User already exists")
    
    hashed_password = generate_password_hash(user_data["password"])
    user_data["password"] = hashed_password
    users_collection.insert_one(user_data)

# Find user by email
def find_user_by_email(email):
    return users_collection.find_one({"email": email})

# Authenticate user by checking password hash
def authenticate_user(email, password):
    user = users_collection.find_one({"email": email})
    if user and check_password_hash(user["password"], password):
        return user
    return None
