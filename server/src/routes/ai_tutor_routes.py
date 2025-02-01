# routes/ai_routes.py
from flask import Blueprint, request, jsonify
from src.models.ai_tutor import AITutor  # Ensure this path matches your project structure

ai_routes = Blueprint("ask_tutor", __name__)
tutor = AITutor()  # Uses the API key from the environment variable

@ai_routes.route("/api/ask", methods=["POST"])
def ask_tutor():
    data = request.get_json()
    user_input = data.get("prompt")
    
    if not user_input:
        return jsonify({"message": "No prompt provided"}), 400
    
    response = tutor.start_conversation(user_input)
    return jsonify({"response": response}), 200
