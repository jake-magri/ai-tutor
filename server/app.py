from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os
from src.routes.book_routes import book_routes
from src.routes.auth_routes import auth_routes
from src.routes.ai_tutor_routes import ai_routes



# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Configure Flask app directly from environment variables
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")

jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Register routes
app.register_blueprint(auth_routes)
app.register_blueprint(book_routes)
app.register_blueprint(ai_routes)
@app.route('/')
def home():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
