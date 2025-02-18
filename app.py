from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import google.generativeai as genai

# Initialize Flask App
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Configure Gemini API
genai.configure(api_key="AIzaSyD6iACth8URpxNzHdIkYQq2HwYoGzR08X0")  # Replace with your API Key

def get_gemini_response(user_input):
    """Communicate with Gemini AI and get a response."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(user_input)
    return response.text if response else "Sorry, I couldn't process that."

@app.route("/")
def home():
    return "Chatbot Backend Running"

# Handle incoming messages from frontend
@socketio.on("message")
def handle_message(data):
    user_message = data["message"]
    bot_response = get_gemini_response(user_message)

    emit("response", {"message": bot_response}, broadcast=True)  # Send response to frontend

if __name__ == "__main__":
    socketio.run(app, debug=True, host="127.0.0.1", port=5000)