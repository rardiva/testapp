import os
import psycopg2
import bcrypt
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "your_pgadmin_connection_string")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return jsonify({"message": "Registration successful!"})
    except:
        return jsonify({"message": "Username already exists!"})

if __name__ == '__main__':
    app.run(debug=True)
