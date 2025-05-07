from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
from chatbot import chat_with_groq  # Uses your existing chatbot integration

app = Flask(__name__)
CORS(app)

# Database file
DATABASE = 'users.db'

# Initialize SQLite3 database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Routes

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    confirm = data.get("confirm_password")

    if not all([name, email, password, confirm]):
        return jsonify({"error": "Please fill in all fields."}), 400
    if password != confirm:
        return jsonify({"error": "Passwords do not match."}), 400

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                       (name, email, password))
        conn.commit()
        conn.close()
        return jsonify({"message": "User created successfully."})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username or email already exists."}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("username")
    password = data.get("password")

    if not name or not password:
        return jsonify({"error": "Missing username or password."}), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE name=?", (name,))
    row = cursor.fetchone()
    conn.close()

    if not row or row[0] != password:
        return jsonify({"error": "Invalid username or password."}), 401

    return jsonify({"message": "Login successful."})

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"response": "Empty message received."}), 400
    try:
        bot_reply = chat_with_groq(user_message)
        return jsonify({"response": bot_reply})
    except Exception as e:
        import traceback
        print("[Flask Error]")
        traceback.print_exc()
        return jsonify({"response": "An error occurred on the server."}), 500

if __name__ == "__main__":
    app.run(debug=True)
