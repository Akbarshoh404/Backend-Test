from flask import Flask
import psycopg2
import os
from routes import routes

app = Flask(__name__)

# Database connection function
def get_db_connection():
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres.railway.internal'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'JGPhLkbufBXvVHSTIfvfxXUFbXxIPzqn'),
        dbname=os.getenv('DB_NAME', 'railway')
    )
    return connection

# Register routes
app.register_blueprint(routes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
