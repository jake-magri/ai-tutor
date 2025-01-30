from db import db  # Import the existing database connection

# Define collections
users_collection = db.users

# Find a user by email
def find_user_by_email(email):
    return users_collection.find_one({"email": email})


# Create a new user
def create_user(user_data):
    if not user_data.get("email") or not user_data.get("password"):
        raise ValueError("User data must include 'email' and 'password'")
    
    users_collection.insert_one(user_data)
