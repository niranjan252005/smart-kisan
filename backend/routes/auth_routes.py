from flask import Blueprint, request, jsonify
from backend.utils.db import users
import os
from dotenv import load_dotenv
import google.oauth2.id_token
import google.auth.transport.requests

load_dotenv()

auth_bp = Blueprint("auth", __name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

# ---------------- MANUAL LOGIN -----------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})

    if user and user["password"] == data["password"]:
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Invalid credentials"})


# ---------------- SIGNUP -----------------
@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if users.find_one({"email": email}):
        return {"success": False, "message": "Email already exists"}

    users.insert_one({
        "name": name,
        "email": email,
        "password": password,
        "google_user": False
    })

    return {"success": True}


# ---------------- GOOGLE LOGIN (Correct for GIS) -----------------
@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    credential = request.json.get("credential")

    try:
        request_session = google.auth.transport.requests.Request()
        id_info = google.oauth2.id_token.verify_oauth2_token(
            credential, request_session, GOOGLE_CLIENT_ID
        )

        email = id_info["email"]
        name = id_info.get("name", "Google User")

        users.update_one(
            {"email": email},
            {"$set": {"email": email, "name": name, "google_user": True}},
            upsert=True
        )

        return {"success": True}

    except Exception as e:
        print("Google login error:", e)
        return {"success": False, "message": "Invalid Google Token"}
