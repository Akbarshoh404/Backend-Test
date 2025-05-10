from flask import Blueprint, request, jsonify
from data import get_db_connection

routes = Blueprint('routes', __name__)

@routes.route("/get-users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    users = [{"user_id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return jsonify(users)

@routes.route("/get-user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "User not found"}), 404

    user = {"user_id": row[0], "name": row[1], "email": row[2]}
    extra = request.args.get("extra")
    if extra:
        user["extra"] = extra
    return jsonify(user)

@routes.route("/add-user", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING user_id",
        (data["name"], data["email"])
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"user_id": new_id, "name": data["name"], "email": data["email"]}), 201

@routes.route("/update-user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    cur.execute(
        "UPDATE users SET name = %s, email = %s WHERE user_id = %s",
        (data.get("name"), data.get("email"), user_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User updated"})

@routes.route("/patch-user/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    data = request.get_json()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return jsonify({"error": "User not found"}), 404

    name = data.get("name", user[1])
    email = data.get("email", user[2])

    cur.execute(
        "UPDATE users SET name = %s, email = %s WHERE user_id = %s",
        (name, email, user_id)
    )
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "User patched"})
