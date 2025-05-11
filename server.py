from flask import Flask, request, jsonify  # Import Flask framework and functions for handling HTTP requests and JSON responses.
import psycopg2  # Import PostgreSQL adapter to interact with the PostgreSQL database.
import bcrypt  # Import bcrypt for password hashing to securely store user credentials.
import os  # Import os to handle environment variables for database connection.

app = Flask(__name__)  # Initialize Flask application.

# Database connection (pgAdmin)
DATABASE_URL = os.getenv("DATABASE_URL", "your_pgadmin_connection_string")  # Get PostgreSQL connection URL from environment variables.
conn = psycopg2.connect(DATABASE_URL)  # Establish a connection to PostgreSQL using the DATABASE_URL.
cur = conn.cursor()  # Create a cursor object to execute SQL commands.

@app.route('/register', methods=['POST'])  # Define a route that listens for POST requests at /register.
def register():  # Function to register a new user.
    username = request.form['username']  # Retrieve the username submitted via the HTML form.
    password = request.form['password']  # Retrieve the password submitted via the HTML form.

    # Hash the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # Encrypt the password using bcrypt for security.

    try:
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))  # Insert username and hashed password into the users table.
        conn.commit()  # Commit the transaction to save changes to the database.
        return jsonify({"message": "Registration successful!"})  # Return a success message in JSON format.
    except:
        return jsonify({"message": "Username already exists!"})  # Return an error message if the username is already in use.

if __name__ == '__main__':  # Ensure this runs only when executed directly, not imported as a module.
    app.run(debug=True)  # Start the Flask app in debug mode for easy troubleshooting.
