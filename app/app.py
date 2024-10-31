from flask import Flask
import redis
import psycopg2
import time

app = Flask(__name__)

# Connect to Redis
redis_client = redis.Redis(host="redis", port=6379)

# Connect to PostgreSQL with retries
def connect_db():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(
                dbname="mydatabase",
                user="mydbuser",
                password="mydbpassword",
                host="db"
            )
            return conn
        except psycopg2.OperationalError:
            print("Database connection failed. Retrying in 5 seconds...")
            retries -= 1
            time.sleep(5)
    raise Exception("Failed to connect to the database after multiple retries")

# Establish connection and cursor
conn = connect_db()
cursor = conn.cursor()

# Ensure a table for tracking visits exists
cursor.execute("CREATE TABLE IF NOT EXISTS visits (count INT);")
conn.commit()

# Route for home page
@app.route("/")
def home():
    # Update Redis
    redis_client.incr("hits")

    # Update PostgreSQL
    cursor.execute("UPDATE visits SET count = count + 1 RETURNING count;")
    if cursor.rowcount == 0:
        cursor.execute("INSERT INTO visits (count) VALUES (1) RETURNING count;")
    count = cursor.fetchone()[0]
    conn.commit()
    
    return f"Hello, Docker Compose! Redis hits: {redis_client.get('hits').decode('utf-8')}, PostgreSQL hits: {count}"

if __name__ == "__main__":
    app.run(host="0.0.0.0")