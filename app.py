import os  # Added os import
from flask import Flask
from routes import routes  # Import the routes

app = Flask(__name__)

# Register routes
app.register_blueprint(routes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)