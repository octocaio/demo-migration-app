from flask import Flask, request, jsonify
from typing import Dict, Any
import json

app = Flask(__name__)

users_db: Dict[int, Dict[str, Any]] = {}
user_id_counter = 1


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "service": "demo-migration-app"}), 200


@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id: int):
    if user_id in users_db:
        return jsonify(users_db[user_id]), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users", methods=["POST"])
def create_user():
    global user_id_counter
    data = request.get_json()

    if not data or "username" not in data or "email" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    user = {
        "id": user_id_counter,
        "username": data["username"],
        "email": data["email"],
        "active": True,
    }

    users_db[user_id_counter] = user
    user_id_counter += 1

    return jsonify(user), 201


@app.route("/users", methods=["GET"])
def list_users():
    return jsonify(list(users_db.values())), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id: int):
    if user_id in users_db:
        del users_db[user_id]
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404


@app.route("/users/<int:user_id>/profile", methods=["GET"])
def get_user_profile(user_id: int):
    if user_id not in users_db:
        return jsonify({"error": "User not found"}), 404

    user = users_db[user_id]
    profile = {
        "user_id": user["id"],
        "username": user["username"],
        "email": user["email"],
        "account_status": "active" if user["active"] else "inactive",
    }
    return jsonify(profile), 200


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
