from flask import Flask, request, jsonify
import psycopg2
import bcrypt
import os

app = Flask(__name__)

# Database Connection (Replace with your NeonDB connection string)
DATABASE_URL = "postgresql://neondb_owner:npg_Ey2u5weIvskq@ep-ancient-cell-a4u0dvvp-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require"
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password.decode('utf-8')))
        conn.commit()
        return jsonify({"message": "Registration successful!"})
    except:
        return jsonify({"message": "Username already exists!"})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    cur.execute("SELECT password FROM users WHERE username = %s", (username,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        return jsonify({"message": "Login successful!"})
    else:
        return jsonify({"message": "Invalid credentials!"})

if __name__ == '__main__':
    app.run(debug=True)
