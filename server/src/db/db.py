from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Get MongoDB URI from .env
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/default_db")
DB_NAME = os.getenv("DB_NAME", "default_db")

# Create a MongoDB client
client = MongoClient(MONGO_URI)
db = client[DB_NAME] # Get the database instance
print("Connected to MongoDB!")
# Access collections (optional)
users_collection = db.get_collection("users")
books_collection = db.get_collection("books")
