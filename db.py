import psycopg2
import os

def get_db_connection():
    connection = psycopg2.connect(
        host=os.getenv('DB_HOST', 'postgres.railway.internal'),
        port=os.getenv('DB_PORT', '5432'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'JGPhLkbufBXvVHSTIfvfxXUFbXxIPzqn'),
        dbname=os.getenv('DB_NAME', 'railway')
    )
    return connection