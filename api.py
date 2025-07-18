from flask import Flask, request, jsonify
from .auth import hash_password, is_admin
from .database import get_user_by_username, create_user

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = get_user_by_username(data["username"])
    if user and user[1] == hash_password(data["password"]):
        return jsonify({"message": "Login successful", "token": "fake-jwt-token"})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    password_hash = hash_password(data["password"])
    create_user(data["username"], password_hash)
    return jsonify({"message": "User created"})

@app.route("/admin", methods=["POST"])
def admin_action():
    data = request.json
    if is_admin(data.get("password", "")):
        return jsonify({"message": "Admin access granted", "debug": "You can run admin tasks now"})
    return jsonify({"error": "Unauthorized"}), 403
