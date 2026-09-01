from flask import Blueprint, request, jsonify

from app.database.supabase import supabase


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")
    name = data.get("name")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    try:

        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "name": name,
                    "role": "inspector"
                }
            }
        })

        return jsonify({
            "message": "Registration successful",
            "user": response.user.model_dump() if response.user else None
        }), 201

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "error": "Email and password are required"
        }), 400

    try:

        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        return jsonify({
            "message": "Login successful",
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "user": response.user.model_dump()
        }), 200

    except Exception as e:

        return jsonify({
            "error": "Invalid email or password"
        }), 401