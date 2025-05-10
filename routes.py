from flask import Blueprint, request, jsonify
from app import get_db_connection  # Import the db connection function

routes = Blueprint('routes', __name__)

@routes.route("/get-users", methods=["GET"])
def get_users():
    try:
        # Connect to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Query to get all users
        cur.execute("SELECT user_id, name, email FROM users")
        rows = cur.fetchall()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        # Return users as JSON
        users = [{"user_id": row[0], "name": row[1], "email": row[2]} for row in rows]
        return jsonify(users)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/get-user/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        # Connect to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Query to get a specific user by ID
        cur.execute("SELECT user_id, name, email FROM users WHERE user_id = %s", (user_id,))
        row = cur.fetchone()
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        if row is None:
            return jsonify({"error": "User not found"}), 404
        
        user = {"user_id": row[0], "name": row[1], "email": row[2]}
        return jsonify(user)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/add-user", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        # Connect to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Insert a new user into the users table
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING user_id",
            (data["name"], data["email"])
        )
        new_id = cur.fetchone()[0]
        
        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"user_id": new_id, "name": data["name"], "email": data["email"]}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/update-user/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    try:
        # Connect to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        
        if not user:
            cur.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        # Update user details
        cur.execute(
            "UPDATE users SET name = %s, email = %s WHERE user_id = %s",
            (data.get("name", user[1]), data.get("email", user[2]), user_id)
        )
        
        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@routes.route("/patch-user/<int:user_id>", methods=["PATCH"])
def patch_user(user_id):
    data = request.get_json()
    try:
        # Connect to PostgreSQL
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if user exists
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user = cur.fetchone()
        
        if not user:
            cur.close()
            conn.close()
            return jsonify({"error": "User not found"}), 404
        
        # Update user details
        cur.execute(
            "UPDATE users SET name = %s, email = %s WHERE user_id = %s",
            (data.get("name", user[1]), data.get("email", user[2]), user_id)
        )
        
        # Commit the changes and close the connection
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({"message": "User patched"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
