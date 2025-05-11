from flask import Flask, request, render_template
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQL
conn = psycopg2.connect("dbname=TB_APP user=postgres password=100postgres100 host=localhost")
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Store the credentials in PostgreSQL
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()

    return f"Account created for {username}!"

if __name__ == '__main__':
    app.run(debug=True)
