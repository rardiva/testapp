import os
import psycopg2
from flask import Flask, request, session, jsonify
from flask_session import Session
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Session config (stores session data)
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:WqFsYotfkVnboVFvnDnKWSTuDqEFQMWr@postgres.railway.internal:5432/railway")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

@app.route('/register', methods=['POST'])
def register():
    new_username = request.form['new_username']
    new_password = request.form['new_password']

    # Hash the password
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (new_username, hashed_password))
        conn.commit()
        return jsonify({"message": "Registration successful!"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur.execute("SELECT password FROM users WHERE username=%s", (username,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        session['username'] = username
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials!"})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({"message": "Logged out successfully!"})

if __name__ == '__main__':
    app.run(debug=True)
