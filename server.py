import os  # Imports the `os` module for interacting with the operating system, such as environment variables.

import psycopg2  # Imports `psycopg2`, a library used to interact with PostgreSQL databases.

import bcrypt  # Imports `bcrypt`, a library used for hashing passwords securely.

from flask import Flask, request, jsonify  # Imports necessary Flask modules for creating a web application.

app = Flask(__name__)  # Creates a Flask application instance.

# Connect to PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "your_pgadmin_connection_string")  # Gets the database connection string from environment variables, using a default if not found.
conn = psycopg2.connect(DATABASE_URL)  # Establishes a connection to the PostgreSQL database using the given connection string.
cur = conn.cursor()  # Creates a cursor for executing SQL commands.

@app.route('/register', methods=['POST'])  # Defines a route `/register` that handles POST requests.
def register():  # Defines the `register` function to handle user registration requests.
    username = request.form['username']  # Retrieves the `username` from the submitted form data.
    password = request.form['password']  # Retrieves the `password` from the submitted form data.

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Hashes the password using bcrypt for security.

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))  # Inserts the new user into the database.
        conn.commit()  # Commits the transaction to save changes.
        return jsonify({"message": "Registration successful!"})  # Returns a success response in JSON format.
    except:
        return jsonify({"message": "Username already exists!"})  # Returns an error response if the username is already taken.

if __name__ == '__main__':  # Ensures this script runs only when executed directly, not when imported.
    app.run(debug=True)  # Starts the Flask application in debug mode to help with troubleshooting.
