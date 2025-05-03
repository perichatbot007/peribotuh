# app.py
from flask import Flask, request, render_template, jsonify
from chatbot import Chatbot
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
bot = Chatbot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_input = data.get("message", "")
    response = bot.get_response(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
