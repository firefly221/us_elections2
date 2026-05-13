import sqlite3

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash

from .db import get_db


api = Blueprint("api", __name__, url_prefix="/api")



def get_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return None
    return data


def voter_to_json(voter):
    return {
        "id": voter["id"],
        "email": voter["email"],
        "name": voter["name"],
        "is_admin": bool(voter["is_admin"]),
        "voted": bool(voter["voted"]),
        "candidate_id": voter["candidate_id"],
    }


@api.get("/health")
def health():
    return jsonify({"status": "ok"})


@api.post("/auth/register")
def register():
    data = get_json()
    if data is None:
        return jsonify({"error": "json_required"}), 400

    email = str(data.get("email", "")).strip().lower()
    name = str(data.get("name", "")).strip()
    password = str(data.get("password", ""))

    if not name:
        return jsonify({"error": "name_required"}), 400
    if "@" not in email:
        return jsonify({"error": "invalid_email"}), 400
    if len(password) < 8:
        return jsonify({"error": "password_too_short"}), 400
    if password != data.get("confirm_password"):
        return jsonify({"error": "passwords_do_not_match"}), 400

    db = get_db()
    voters_count = db.execute("SELECT COUNT(*) FROM voters").fetchone()[0]
    is_admin = 1 if voters_count == 0 else 0

    try:
        db.execute(
            "INSERT INTO voters (email, password_hash, name, is_admin) VALUES (?, ?, ?, ?)",
            (email, generate_password_hash(password), name, is_admin),
        )
        db.commit()
    except sqlite3.IntegrityError:
        return jsonify({"error": "email_already_registered"}), 409

    voter = db.execute("SELECT * FROM voters WHERE email = ?", (email,)).fetchone()
    return jsonify({"voter": voter_to_json(voter)}), 201