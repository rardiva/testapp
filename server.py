import os
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Use Railway's PostgreSQL connection string
DATABASE_URL = os.getenv("docker pull ghcr.io/railwayapp-templates/postgres-ssl:15", "${{ Postgres.DATABASE_URL }}")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cur.fetchone()

    if user:
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials!"})

if __name__ == '__main__':
    app.run(debug=True)
