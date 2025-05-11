from flask import Flask, render_template, request, redirect, session
import psycopg2
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key"

# PostgreSQL connection
conn = psycopg2.connect("dbname=your_db user=your_user password=your_password host=your_host")
cursor = conn.cursor()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/register', methods=['POST'])
def register():
    username = request.form['new_username']
    password = request.form['new_password']
    
    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        return "Registration Successful"
    except:
        return "Username already exists"

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user[0].encode('utf-8')):
        session['username'] = username
        return "Login Successful"
    else:
        return "Invalid Credentials"

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return "Logged Out"

if __name__ == '__main__':
    app.run(debug=True)
