from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from routes.user_routes import user_routes
from dotenv import load_dotenv
import os
from routes.book_routes import book_routes
from routes.auth_routes import auth_routes
from routes.ai_tutor_routes import ask_tutor



# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Configure Flask app directly from environment variables
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")

jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

# Register routes
app.register_blueprint(user_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(book_routes)
app.register_blueprint(ask_tutor)
@app.route('/')
def home():
    return jsonify(message="Hello from Flask!")

if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, port=port)
